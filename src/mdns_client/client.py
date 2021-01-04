import socket
from collections import namedtuple
from select import select

import uasyncio

from .constants import MAX_PACKET_SIZE, MDNS_ADDR, MDNS_PORT
from .parser import parse_packet
from .structs import DNSQuestion, DNSQuestionWrapper, DNSResponse
from .util import dotted_ip_to_bytes


class Callback(namedtuple("Callback", ["callback", "remove_if"])):
    id: int
    callback: "Callable[[DNSResponse], Awaitable[None]]"
    remove_if: "Optional[Callable[[DNSResponse], Awaitable[bool]]]"


class MDNSClient:
    def __init__(self, local_addr: str, debug: bool = False):
        self.socket: "Optional[socket.socket]" = None
        self.local_addr = local_addr
        self.debug = debug
        self.stopped = False
        self.callbacks: "Dict[int, Callback]" = {}
        self.callback_fd_count: int = 0

    def add_callback(
        self,
        callback: "Callable[[DNSResponse], Awaitable[None]]",
        remove_if: "Optional[Callable[[DNSResponse], Awaitable[bool]]]" = None,
    ) -> None:
        callback_config = Callback(id=self.callback_fd_count, callback=callback, remove_if=remove_if)
        self.callback_fd_count += 1
        self.dprint("Adding callback with id {}".format(callback_config.id))
        self.callbacks[callback_config.id] = callback_config

    def _make_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        member_info = dotted_ip_to_bytes(MDNS_ADDR) + dotted_ip_to_bytes(self.local_addr)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, member_info)
        sock.setblocking(False)
        return sock

    async def start(self) -> None:
        if self.socket is not None:
            self.socket.close()
        self.socket = self._make_socket()
        self.socket.bind(("", MDNS_PORT))
        await self.consume()

    def stop(self) -> None:
        self.stopped = True

    async def consume(self) -> None:
        while not self.stopped:
            await self.process_waiting_data()
            await uasyncio.sleep_ms(100)

    async def process_waiting_data(self) -> None:
        while True:
            readers, _, _ = select([self.socket], [], [], 0)
            if not readers:
                break

            buffer, addr = self.socket.recvfrom(MAX_PACKET_SIZE)
            if addr[0] == self.local_addr:
                continue

            try:
                await self.process_packet(buffer)
            except Exception as e:
                self.dprint("Issue processing packet: {}".format(e))

    async def process_packet(self, buffer: bytes) -> None:
        parsed_packet = parse_packet(buffer)
        if len(self.callbacks) == 0:
            print(parsed_packet)
        else:
            loop = uasyncio.get_event_loop()
            for callback in self.callbacks.values():
                loop.create_task(callback.callback(parsed_packet))
                if callback.remove_if is not None:
                    loop.create_task(self.remove_if_check(callback, parsed_packet))

    async def remove_if_check(self, callback: Callback, message: DNSResponse) -> None:
        if callback.id in self.callbacks and await callback.remove_if(message):
            self.dprint("Removing callback with id {}".format(callback.id))
            del self.callbacks[callback.id]

    async def send_question(self, *questions: DNSQuestion) -> None:
        assert isinstance(self.socket, socket.socket), "Socket must be set"
        question_wrapper = DNSQuestionWrapper(questions=questions)
        self.socket.sendto(question_wrapper.to_bytes(), (MDNS_ADDR, MDNS_PORT))

    def dprint(self, message: str) -> None:
        if self.debug:
            print("MDNS: {}".format(message))
