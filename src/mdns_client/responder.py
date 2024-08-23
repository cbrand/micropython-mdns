import random
from collections import namedtuple

import uasyncio

from mdns_client.client import Client
from mdns_client.constants import (
    CLASS_IN,
    DEFAULT_TTL,
    FLAGS_QR_AUTHORITATIVE,
    FLAGS_QR_RESPONSE,
    TYPE_A,
    TYPE_PTR,
    TYPE_SRV,
    TYPE_TXT,
)
from mdns_client.structs import DNSQuestion, DNSRecord, DNSResponse, ServiceProtocol, SRVRecord
from mdns_client.util import dotted_ip_to_bytes, name_to_bytes, txt_data_to_bytes

Advertisement = namedtuple("Advertisement", ["port", "data", "host"])
MDNS_SERVICE_DISCOVERY = "_services._dns-sd._udp.local"


def generate_random_postfix() -> str:
    return str(random.randint(0x800000, 0xFFFFFF))[2:]


class Responder:
    def __init__(
        self,
        client: Client,
        own_ip: "Union[None, str, Callable[[], str]]",
        host: "Union[None, str, Callable[[], str]]" = None,
        debug: bool = False,
    ) -> None:
        self._client = client
        self.callback_id = None
        self.host_resolver = host
        self.own_ip_resolver = own_ip
        self._advertisements = {}
        self.debug = debug

    @property
    def stopped(self) -> bool:
        return self.callback_id is None

    @property
    def own_ip(self) -> "Optional[str]":
        if callable(self.own_ip_resolver):
            return self.own_ip_resolver()
        return self.own_ip_resolver

    @property
    def host(self) -> "Optional[str]":
        host_resolver = self.host_resolver
        if callable(host_resolver):
            host_resolver = host_resolver()

        if host_resolver is None:
            # setting once a host name
            postfix = self.generate_random_postfix()
            self.host_resolver = host_resolver = "micropython-{}".format(postfix)

        return host_resolver

    def generate_random_postfix(self) -> str:
        return generate_random_postfix()

    @property
    def host_fqdn(self) -> Optional[str]:
        host = self.host
        if host is None:
            return None

        return ".".join((host, "local")).lower()

    def advertise(
        self,
        protocol: str,
        service: str,
        port: int,
        data: "Optional[Dict[str, Union[List[str], str]]]" = None,
        service_host_name: "Optional[str]" = None,
    ) -> None:
        service_protocol = ServiceProtocol(protocol, service)
        self._advertisements[service_protocol.to_name()] = Advertisement(port, data, service_host_name)
        if self.stopped:
            self.start()

    def withdraw(self, protocol: str, service: str) -> None:
        service_protocol = ServiceProtocol(protocol, service)
        name = service_protocol.to_name()
        if name in self._advertisements:
            del self._advertisements[name]

    def start(self) -> None:
        if not self.stopped:
            return

        callback = self._client.add_callback(self._on_response)
        self.callback_id = callback.id

    def stop(self) -> None:
        if self.stopped:
            return

        self._client.remove_id(self.callback_id)
        self.callback_id = None

    async def _on_response(self, response: DNSResponse) -> None:
        if not response.is_request:
            return

        for question in response.questions:
            self._on_question(question)

    def _on_question(self, question: DNSQuestion) -> None:
        if question.type == TYPE_PTR:
            self._on_ptr_question(question)
        elif question.type == TYPE_SRV:
            self._on_srv_question(question)
        elif question.type == TYPE_A:
            self._on_a_question(question)
        elif question.type == TYPE_TXT:
            self._on_txt_question(question)

    def _on_ptr_question(self, question: DNSQuestion) -> None:
        query = question.query
        if query == MDNS_SERVICE_DISCOVERY:
            self._send_service_discovery_ptrs()
            return

        if query not in self._advertisements:
            return

        self._dprint("Responding to DNS PTR question for {}".format(query))
        ptr_record = self._ptr_record_for(query)
        if ptr_record is None:
            return
        answers = [ptr_record]
        additional = [self._srv_record_for(query), self._txt_record_for(query), self._a_record()]
        self._send_response(answers, additional)

    def _send_service_discovery_ptrs(self) -> None:
        answers = []
        for service in self._advertisements.keys():
            answers.append(DNSRecord(MDNS_SERVICE_DISCOVERY, TYPE_PTR, CLASS_IN, DEFAULT_TTL, name_to_bytes(service)))
        self._dprint("Answering service record query with services {}".format(",".join(self._advertisements.keys())))
        self._send_response(answers)

    def _on_srv_question(self, question: DNSQuestion) -> None:
        query = question.query
        service = self._get_service_of(query)
        if service is None:
            return

        self._dprint("Responding to DNS SRV question for {}".format(query))
        srv_answers = [self._srv_record_for(service)]
        additional = [self._a_record(), self._txt_record_for(service)]
        self._send_response(srv_answers, additional)

    def _on_a_question(self, question: DNSQuestion) -> None:
        if question.query != self.host_fqdn:
            return

        a_record = self._a_record()
        if a_record is None:
            return

        self._dprint("Responding to DNS A question for {}".format(question.query))
        self._send_response([a_record])

    def _on_txt_question(self, question: DNSQuestion) -> None:
        query = question.query
        service = self._get_service_of(query)
        if service is None:
            return

        txt_record = self._txt_record_for(service)
        if txt_record is None:
            return

        self._dprint("Responding to DNS TXT question for {}".format(query))
        srv_answers = [txt_record]
        self._send_response(srv_answers)

    def _get_service_of(self, query: str) -> "Optional[str]":
        query_parts = query.split(".")
        if len(query_parts) != 4 or query_parts[-1] != "local":
            return

        service = ".".join(query_parts[-3:])
        if service not in self._advertisements:
            return None
        advertisment = self._advertisements[service]
        if query_parts[0] not in (self.host, advertisment.host):
            return None

        return service

    def _ptr_record_for(self, query: str) -> "Optional[DNSRecord]":
        ptr_target = self._service_name_of(query)
        if ptr_target is None:
            return None
        # For some reason the PTR is shortened and the last two bytes are removed
        ptr_target_bytes = name_to_bytes(ptr_target)
        return DNSRecord(query, TYPE_PTR, CLASS_IN, DEFAULT_TTL, ptr_target_bytes)

    def _srv_record_for(self, query: str) -> "Optional[DNSRecord]":
        advertisment = self._advertisements.get(query, None)
        host_fqdn = self.host_fqdn
        if advertisment is None or host_fqdn is None:
            return None
        srv_name = self._service_name_of(query)
        assert srv_name is not None

        srv_record = SRVRecord(srv_name, 0, 0, advertisment.port, host_fqdn)
        return DNSRecord(srv_name, TYPE_SRV, CLASS_IN, DEFAULT_TTL, srv_record.to_bytes())

    def _txt_record_for(self, service: str) -> "Optional[DNSRecord]":
        advertisment = self._advertisements.get(service, None)
        host = self.host
        if advertisment is None or host is None:
            return None

        txt_data = advertisment.data or {}

        fqdn_name = self._service_name_of(service)
        assert fqdn_name is not None
        txt_payload = txt_data_to_bytes(txt_data)

        return DNSRecord(fqdn_name, TYPE_TXT, CLASS_IN, DEFAULT_TTL, txt_payload)

    def _service_name_of(self, service: str) -> "Optional[str]":
        advertisment = self._advertisements.get(service, None)
        host = self.host
        if advertisment is None:
            return None
        host = advertisment.host or host
        fqdn_name = ".".join((host, service))
        return fqdn_name.lower()

    def _a_record(self) -> "Optional[DNSRecord]":
        host_fqdn = self.host_fqdn
        ip_address = self.own_ip
        if host_fqdn is None or ip_address is None:
            return None

        return DNSRecord(host_fqdn, TYPE_A, CLASS_IN, DEFAULT_TTL, dotted_ip_to_bytes(ip_address))

    def _send_response(
        self, answers: "List[DNSRecord]", additional: "Optional[List[Union[DNSRecord, None]]]" = None
    ) -> None:
        if additional is None:
            additional = []
        additional = [item for item in additional if item is not None]

        msg_type = FLAGS_QR_RESPONSE | FLAGS_QR_AUTHORITATIVE
        response = DNSResponse(0x00, msg_type, questions=[], answers=answers, authorities=[], additional=additional)
        loop = uasyncio.get_event_loop()
        loop.create_task(self._client.send_response(response))

    def _dprint(self, message: str) -> None:
        if self.debug:
            print("MDNS Responder: {}".format(message))
