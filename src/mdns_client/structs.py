from collections import namedtuple
from struct import pack_into

from .constants import CLASS_MASK, CLASS_UNIQUE, FLAGS_QR_QUERY
from .util import check_name, pack_string, string_packed_len


class DNSEntry:
    def __init__(self, name: str, type_: int, class_: int) -> None:
        self.key = name.lower()
        self.name = name
        self.type = type_
        self.class_ = class_ & CLASS_MASK
        self.unique = (class_ & CLASS_UNIQUE) != 0


class DNSQuestion(namedtuple("DNSQuestion", ["query", "type", "query_class"])):
    @property
    def checked_query(self) -> "List[bytes]":
        return check_name(self.query)

    def to_bytes(self) -> memoryview:
        checked_query = self.checked_query
        query_len = string_packed_len(checked_query)
        buffer = bytearray(query_len + 4)
        pack_string(buffer, self.checked_query)
        pack_into("!HH", buffer, query_len, self.type, self.query_class)
        return memoryview(buffer)


class DNSQuestionWrapper(namedtuple("DNSQuestionWrapper", ["questions"])):
    questions: "List[DNSQuestion]"

    def to_bytes(self) -> memoryview:
        question_bytes = [question.to_bytes() for question in self.questions]
        buffer = bytearray(sum(len(qb) for qb in question_bytes) + 12)
        buffer[:12] = FLAGS_QR_QUERY.to_bytes(12, "big")
        buffer[4:6] = len(self.questions).to_bytes(2, "big")
        index = 12
        for question_bytes_item in question_bytes:
            end = index + len(question_bytes_item)
            buffer[index:end] = question_bytes_item
            index = end
        return memoryview(buffer)


class DNSRecord(namedtuple("DNSRecord", ["name", "record_type", "query_class", "time_to_live", "rdata"])):
    name: str
    record_type: int
    query_class: int
    time_to_live: int
    rdata: bytes


class DNSResponse(
    namedtuple(
        "DNSResponse", ["addr", "transaction_id", "message_type", "questions", "answers", "authorities", "additional"]
    )
):
    addr: str
    transaction_id: int
    message_type: int
    questions: "List[DNSQuestion]"
    answers: "List[DNSRecord]"
    authorities: "List[DNSRecord]"
    additional: "List[DNSRecord]"
