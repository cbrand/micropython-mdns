import time
from collections import namedtuple
from struct import pack_into, unpack_from

from mdns_client.constants import FLAGS_QR_QUERY, FLAGS_QR_RESPONSE
from mdns_client.util import (
    byte_count_of_lists,
    bytes_to_name,
    check_name,
    fill_buffer,
    name_to_bytes,
    pack_name,
    string_packed_len,
)


class DNSQuestion(namedtuple("DNSQuestion", ["query", "type", "query_class"])):
    @property
    def checked_query(self) -> "List[bytes]":
        return check_name(self.query)

    def to_bytes(self) -> bytes:
        checked_query = self.checked_query
        query_len = string_packed_len(checked_query)
        buffer = bytearray(query_len + 4)
        pack_name(buffer, self.checked_query)
        pack_into("!HH", buffer, query_len, self.type, self.query_class)
        return buffer


class DNSQuestionWrapper(namedtuple("DNSQuestionWrapper", ["questions"])):
    questions: "List[DNSQuestion]"

    def to_bytes(self) -> bytes:
        question_bytes = [question.to_bytes() for question in self.questions]
        buffer = bytearray(sum(len(qb) for qb in question_bytes) + 12)
        buffer[:12] = FLAGS_QR_QUERY.to_bytes(12, "big")
        buffer[4:6] = len(self.questions).to_bytes(2, "big")
        index = 12
        for question_bytes_item in question_bytes:
            end = index + len(question_bytes_item)
            buffer[index:end] = question_bytes_item
            index = end
        return buffer


class DNSRecord(namedtuple("DNSRecord", ["name", "record_type", "query_class", "time_to_live", "rdata"])):
    name: str
    record_type: int
    query_class: int
    time_to_live: int
    rdata: bytes

    @property
    def checked_name(self) -> "List[bytes]":
        return check_name(self.name)

    def to_bytes(self) -> bytes:
        checked_name = self.checked_name
        # Require a null bit in the end of the string
        query_len = string_packed_len(checked_name)
        header_length = query_len + 10
        rdata_length = len(self.rdata)
        buffer = bytearray(header_length + rdata_length)
        pack_name(buffer, checked_name)
        index = query_len
        pack_into("!HHLH", buffer, index, self.record_type, self.query_class, self.time_to_live, rdata_length)
        index += 10
        end_index = index + rdata_length
        buffer[index:end_index] = self.rdata
        return buffer

    @property
    def invalid_at(self) -> int:
        return time.ticks_ms() + self.time_to_live * 1000


class DNSResponse(
    namedtuple("DNSResponse", ["transaction_id", "message_type", "questions", "answers", "authorities", "additional"])
):
    transaction_id: int
    message_type: int
    questions: "List[DNSQuestion]"
    answers: "List[DNSRecord]"
    authorities: "List[DNSRecord]"
    additional: "List[DNSRecord]"

    @property
    def is_response(self) -> bool:
        return self.message_type & FLAGS_QR_RESPONSE == FLAGS_QR_RESPONSE

    @property
    def is_request(self) -> bool:
        return not self.is_response

    @property
    def records(self) -> "Iterable[DNSRecord]":
        yield from self.answers
        yield from self.authorities
        yield from self.additional

    def to_bytes(self) -> bytes:
        question_bytes = [question.to_bytes() for question in self.questions]
        answer_bytes = [answer.to_bytes() for answer in self.answers]
        authorities_bytes = [authority.to_bytes() for authority in self.authorities]
        additional_bytes = [additional.to_bytes() for additional in self.additional]
        payload_length = byte_count_of_lists(question_bytes, answer_bytes, authorities_bytes, additional_bytes)
        buffer = bytearray(12 + payload_length)
        pack_into(
            "!HHHHHH",
            buffer,
            0,
            self.transaction_id,
            self.message_type,
            len(question_bytes),
            len(answer_bytes),
            len(authorities_bytes),
            len(additional_bytes),
        )
        index = 12
        for question_byte_list in question_bytes:
            index = fill_buffer(buffer, question_byte_list, index)
        for answer_byte_list in answer_bytes:
            index = fill_buffer(buffer, answer_byte_list, index)
        for authority_byte_list in authorities_bytes:
            index = fill_buffer(buffer, authority_byte_list, index)
        for additional_byte_list in additional_bytes:
            index = fill_buffer(buffer, additional_byte_list, index)
        return buffer


class ServiceProtocol(namedtuple("ServiceProtocol", ["protocol", "service"])):
    @property
    def domain(self) -> str:
        return "local"

    def to_name(self) -> str:
        return "{}.{}.{}".format(self.protocol, self.service, self.domain).lower()


ServiceResponse = namedtuple("ServiceResponse", ["priority", "weight", "port", "target"])


class SRVMixin:
    name: str

    @property
    def protocol(self) -> ServiceProtocol:
        service_name_data = self.name.split(".")
        return ServiceProtocol(service_name_data[-3], service_name_data[-2])


class SRVRecord(namedtuple("SRVRecord", ["name", "priority", "weight", "port", "target"]), SRVMixin):
    @classmethod
    def from_dns_record(cls, dns_record: DNSRecord) -> "SRVRecord":
        name = dns_record.name
        priority, weight, port = unpack_from("!HHH", dns_record.rdata, 0)
        target = bytes_to_name(dns_record.rdata[6:]).lower()
        return SRVRecord(name, priority, weight, port, target)

    def to_bytes(self) -> bytes:
        target_name = name_to_bytes(self.target)
        buffer = bytearray(6 + len(target_name))
        pack_into("!HHH", buffer, 0, self.priority, self.weight, self.port)
        buffer[6:] = target_name
        return buffer
