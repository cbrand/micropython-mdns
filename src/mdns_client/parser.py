import struct
from collections import namedtuple

from .structs import DNSQuestion, DNSRecord, DNSResponse
from .util import might_have_repeatable_payload

MDNSPacketHeader = namedtuple(
    "MDNSPacketHeader",
    ["transaction_id", "message_type", "num_questions", "num_answers", "num_authorities", "num_additional"],
)


def parse_packet(buffer: bytes, addr: str) -> "Optional[DNSResponse]":
    packet_parser = PacketParser(buffer, addr)
    return packet_parser.parse()


class PacketParser:
    def __init__(self, buffer: bytes, addr: str) -> None:
        self.buffer = buffer
        self.addr = addr
        self.index = 0
        self.header = MDNSPacketHeader(*self._unpack("!HHHHHH", 6))
        self.index = 12

    def parse(self) -> "Optional[DNSResponse]":
        questions = self.parse_questions()
        answers = self.parse_answers()
        authorities = self.parse_authorities()
        additionals = self.parse_additionals()
        return DNSResponse(
            self.addr,
            self.header.transaction_id,
            self.header.message_type,
            questions,
            answers,
            authorities,
            additionals,
        )

    def parse_questions(self) -> "List[DNSQuestion]":
        return [self.parse_question() for _ in range(self.header.num_questions)]

    def parse_question(self) -> DNSQuestion:
        record_name = self._parse_record_name()
        type_query, query_class = self._unpack("!HH", 4)
        return DNSQuestion(record_name, type_query, query_class)

    def parse_records(self, num_records: int) -> "List[DNSRecord]":
        return [self.parse_record() for _ in range(num_records)]

    def parse_record(self) -> DNSRecord:
        record_name = self._parse_record_name()
        record_type, query_class, time_to_live = self._unpack("!HHL", 8)
        if might_have_repeatable_payload(record_type):
            record_entry = self._parse_repeatable_record_entry()
        else:
            record_entry = self._parse_record_entry()
        return DNSRecord(record_name, record_type, query_class, time_to_live, record_entry)

    def parse_answers(self) -> "List[DNSRecord]":
        return self.parse_records(self.header.num_answers)

    def parse_authorities(self) -> "List[DNSRecord]":
        return self.parse_records(self.header.num_authorities)

    def parse_additionals(self) -> List[DNSRecord]:
        return self.parse_records(self.header.num_additional)

    def _parse_record_name(self) -> str:
        payload = ""
        if self.buffer[self.index] & 0xC0 == 0xC0:
            return self._parse_record_name_offset()

        while self.buffer[self.index] != 0x00:
            if len(payload) > 0:
                payload += "."

            payload += self._parse_string()
        self.index += 1
        return payload

    def _parse_string(self) -> str:
        payload = self._parse_bytes()
        return payload.decode("utf-8")

    def _parse_record_name_offset(self) -> str:
        offset_tuple = self._unpack("!H", 2)
        offset = offset_tuple[0] ^ (0xC0 << 8)
        real_index = self.index
        self.index = offset
        record_name = self._parse_record_name()
        self.index = real_index
        return record_name

    def _parse_bytes(self) -> bytes:
        size = self.buffer[self.index]
        if size & 0xC0 == 0xC0:
            return self._parse_repeat_bytes()

        self.index += 1
        return self._parse_bytes_of(int(size))

    def _parse_repeat_bytes(self) -> bytes:
        offset_tuple = self._unpack("!H", 2)
        offset = offset_tuple[0] ^ (0xC0 << 8)
        real_index = self.index
        self.index = offset
        record_name = self._parse_bytes()
        self.index = real_index
        return record_name

    def _parse_repeatable_record_entry(self) -> bytes:
        if self.buffer[self.index] & 0xC0 == 0xC0:
            return self._parse_repeat_bytes()
        else:
            return self._parse_record_entry()

    def _parse_record_entry(self) -> bytes:
        size_tuple = self._unpack("!H", 2)
        return self._parse_bytes_of(size_tuple[0])

    def _parse_bytes_of(self, length: int) -> bytes:
        index = self.index
        end_index = index + length
        data = self.buffer[index:end_index]
        self.index = end_index
        return data

    def _unpack(self, format: str, length: int) -> "Tuple[Any]":
        unpacked = struct.unpack_from(format, self.buffer, self.index)
        self.index += length
        return unpacked
