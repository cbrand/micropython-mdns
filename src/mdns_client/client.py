import gc
import socket
import time
from collections import namedtuple
from select import select

import uasyncio

from mdns_client.constants import CLASS_IN, LOCAL_MDNS_SUFFIX, MAX_PACKET_SIZE, MDNS_ADDR, MDNS_PORT, TYPE_A
from mdns_client.parser import parse_packet
from mdns_client.structs import DNSQuestion, DNSQuestionWrapper, DNSRecord, DNSResponse
from mdns_client.util import a_record_rdata_to_string, dotted_ip_to_bytes, set_after_timeout


class Callback(namedtuple("Callback", ["id", "callback", "remove_if", "timeout", "created_ticks"])):
    id: int
    callback: "Callable[[DNSResponse], Awaitable[None]]"
    remove_if: "Optional[Callable[[DNSResponse], Awaitable[bool]]]"
    timeout: "Optional[float]"
    created_ticks: int

    @property
    def timedout(self) -> bool:
        if self.timeout is None:
            return False

        return self.created_ticks + int(self.timeout * 1000) < time.ticks_ms()


class Client:
    def __init__(self, local_addr: str, debug: bool = False):
        self.socket: "Optional[socket.socket]" = None
        self.local_addr = local_addr
        self.debug = debug
        self.print_packets = debug
        self.stopped = True
        self.callbacks: "Dict[int, Callback]" = {}
        self.callback_fd_count: int = 0
        self.mdns_timeout = 2.0

    def add_callback(
        self,
        callback: "Callable[[DNSResponse], Awaitable[None]]",
        remove_if: "Optional[Callable[[DNSResponse], Awaitable[bool]]]" = None,
        timeout: "Optional[int]" = None,
    ) -> Callback:
        callback_config = Callback(
            id=self.callback_fd_count,
            callback=callback,
            remove_if=remove_if,
            timeout=timeout,
            created_ticks=time.ticks_ms(),
        )
        self.callback_fd_count += 1
        self.dprint("Adding callback with id {}".format(callback_config.id))
        self.callbacks[callback_config.id] = callback_config
        if self.stopped:
            self.dprint("Added consumer on stopped mdns client. Starting it now.")
            loop = uasyncio.get_event_loop()
            loop.create_task(self.start())
        return callback_config

    def add_membership(self, sock=None) -> None:
        if sock is None:
            sock = self.socket
        member_info = dotted_ip_to_bytes(MDNS_ADDR) + dotted_ip_to_bytes(self.local_addr)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, member_info)

    def _make_socket(self) -> socket.socket:
        self.dprint("Creating socket for address %s" % (self.local_addr))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.add_membership(sock)
        sock.setblocking(False)
        self.dprint("Socket creation finished")
        return sock

    async def start(self) -> None:
        if self.stopped:
            self.stopped = False
            await self.consume()

    def _init_socket(self) -> None:
        self._close_socket()
        self.socket = self._make_socket()
        self.socket.bind((MDNS_ADDR, MDNS_PORT))
        self.dprint("Bind finished ready to use MDNS query data")

    def stop(self) -> None:
        self.stopped = True
        self._close_socket()

    def _close_socket(self) -> None:
        if self.socket is not None:
            self.socket.close()
        self.socket = None

    async def consume(self) -> None:
        self.dprint("Starting mdns client consume loop.")
        self._init_socket()
        while not self.stopped:
            await self.process_waiting_data()
            await uasyncio.sleep_ms(100)

    async def process_waiting_data(self) -> None:
        while not self.stopped:
            await uasyncio.sleep_ms(0)
            readers, _, _ = select([self.socket], [], [], 0)
            if not readers:
                break

            try:
                buffer, addr = self.socket.recvfrom(MAX_PACKET_SIZE)
            except MemoryError:
                # This seems to happen here without SPIRAM sometimes.
                self.dprint(
                    "Receiving data failed with MemoryError, replacing socket"
                )
                self._init_socket()
                continue

            if addr[0] == self.local_addr:
                continue

            try:
                await self.process_packet(buffer)
            except Exception as e:
                self.dprint("Issue processing packet: {}".format(e))
            finally:
                gc.collect()

    async def process_packet(self, buffer: bytes) -> None:
        parsed_packet = parse_packet(buffer)
        if len(self.callbacks) == 0:
            if self.print_packets:
                print(parsed_packet)
        else:
            loop = uasyncio.get_event_loop()
            for callback in self.callbacks.values():
                loop.create_task(callback.callback(parsed_packet))
                if callback.timedout:
                    self.remove_if_present(callback)
                elif callback.remove_if is not None:
                    loop.create_task(self.remove_if_check(callback, parsed_packet))

    async def remove_if_check(self, callback: Callback, message: DNSResponse) -> None:
        if await callback.remove_if(message):
            return self.remove_if_present(callback)

    def remove_if_present(self, callback: Callback) -> None:
        self.remove_id(callback.id)

    def remove_id(self, callback_id: int) -> bool:
        deleted = False
        if callback_id in self.callbacks:
            self.dprint("Removing callback with id {}".format(callback_id))
            del self.callbacks[callback_id]
            deleted = True

        if len(self.callbacks) == 0 and not self.print_packets:
            self.dprint("Stopping consumption pipeline as no listeners exist")
            self.stop()

        return deleted

    async def send_question(self, *questions: DNSQuestion) -> None:
        question_wrapper = DNSQuestionWrapper(questions=questions)
        self._send_bytes(question_wrapper.to_bytes())

    async def send_response(self, response: DNSResponse) -> None:
        self._send_bytes(response.to_bytes())

    def _send_bytes(self, payload: bytes) -> None:
        if self.socket is None:
            self._init_socket()
        for _ in range(2):
            try:
                self.socket.sendto(payload, (MDNS_ADDR, MDNS_PORT))
                break
            except OSError as exc:
                # This sendto function sometimes returns an OSError with EBADF
                # as errno. To avoid a failure here, reinitialize the socket
                # and try again.
                self.dprint("Sending data failed with OSError(%s), replacing socket" % exc.args[0])
                self._init_socket()

    async def getaddrinfo(
        self,
        host: "Union[str, bytes, bytearray]",
        port: "Union[str, int, None]",
        family: int = 0,
        type: int = 0,
        proto: int = 0,
        flags: int = 0,
    ) -> "List[Tuple[int, int, int, str, Tuple[str, int]]]":
        hostcheck = host
        while hostcheck.endswith("."):
            hostcheck = hostcheck[:-1]
        if hostcheck.endswith(LOCAL_MDNS_SUFFIX) and family in (0, socket.AF_INET):
            host, resolved_ip = await self.mdns_getaddr(host)
            return [(socket.AF_INET, type or socket.SOCK_STREAM, proto, host, (resolved_ip, port))]
        else:
            self.dprint("Resolving dns request host {} and port {}".format(host, port))
            return socket.getaddrinfo(host, port, family, type, proto, flags)

    async def mdns_getaddr(self, host: str) -> Tuple[str, str]:
        host = host.lower()
        self.dprint("Resolving mdns request host {}".format(host))
        response = self.scan_for_response(TYPE_A, host, self.mdns_timeout)
        await self.send_question(DNSQuestion(host, TYPE_A, CLASS_IN))
        record = await response
        if record is None:
            # The original socket implementation returns -202 on the ESP32 as an error code
            raise OSError(-202)

        return record.name, a_record_rdata_to_string(record.rdata)

    async def scan_for_response(self, expected_type: int, name: str, timeout: float = 1.5) -> "Optional[DNSRecord]":
        def matching_record(dns_response: DNSResponse) -> "Optional[DNSRecord]":
            for record in dns_response.records:
                if record.record_type == expected_type and record.name == name:
                    return record

        result = {"data": None, "event": uasyncio.Event()}

        async def scan_response(dns_response: DNSResponse) -> None:
            record = matching_record(dns_response)
            if record is None:
                return None
            result["data"] = record
            result["event"].set()

        loop = uasyncio.get_event_loop()
        loop.create_task(set_after_timeout(result["event"], timeout))

        async def is_match(dns_response: DNSResponse) -> bool:
            return matching_record(dns_response) is not None

        self.add_callback(scan_response, is_match, timeout)
        await result["event"].wait()
        return result["data"]

    def dprint(self, message: str) -> None:
        if self.debug:
            print("MDNS: {}".format(message))
