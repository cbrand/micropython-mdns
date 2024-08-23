import struct
from collections import namedtuple

from mdns_client.constants import REPEAT_TYPE_FLAG, TYPE_CNAME, TYPE_NS, TYPE_PTR, TYPE_SOA, TYPE_SRV
from mdns_client.structs import DNSQuestion, DNSRecord, DNSResponse
from mdns_client.util import end_index_of_name

MDNSPacketHeader = namedtuple(
    "MDNSPacketHeader",
    ["transaction_id", "message_type", "num_questions", "num_answers", "num_authorities", "num_additional"],
)


def parse_packet(buffer: bytes) -> "Optional[DNSResponse]":
    packet_parser = PacketParser(buffer)
    return packet_parser.parse()


class PacketParser:
    def __init__(self, buffer: bytes) -> None:
        self.buffer = buffer
        self.index = 0
        self.header = MDNSPacketHeader(*self._unpack("!HHHHHH", 6))
        self.index = 12

    def parse(self) -> "Optional[DNSResponse]":
        questions = self.parse_questions()
        answers = self.parse_answers()
        authorities = self.parse_authorities()
        additionals = self.parse_additionals()
        return DNSResponse(
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
        record_name = self._parse_record_name().lower()
        type_query, query_class = self._unpack("!HH", 4)
        return DNSQuestion(record_name, type_query, query_class)

    def parse_records(self, num_records: int) -> "List[DNSRecord]":
        return [self.parse_record() for _ in range(num_records)]

    def parse_record(self) -> DNSRecord:
        record_name = self._parse_record_name()
        record_type, query_class, time_to_live = self._unpack("!HHL", 8)
        record_entry = self._parse_record_entry()
        if record_type in (TYPE_PTR, TYPE_NS, TYPE_CNAME):
            # The payload is a string and might be compacted. Unpacking the name payload.
            record_entry = self._expand_name(record_entry)
        elif record_type == TYPE_SRV:
            record_entry = self._parse_srv_entry(record_entry)
        elif record_type == TYPE_SOA:
            record_entry = self._parse_soa_entry(record_entry)
        return DNSRecord(record_name, record_type, query_class, time_to_live, record_entry)

    def _parse_srv_entry(self, record_entry: bytes) -> bytes:
        # The first 6 bytes are metadata, everything afterwards is a name which might need expansion.
        expanded_name = self._expand_name(record_entry[6:])
        return record_entry[:6] + expanded_name

    def _parse_soa_entry(self, record_entry: bytes) -> bytes:
        # Two names are encoded which need to eventually be expanded.
        # All information afterwards does not require expansion
        mname_end_index = end_index_of_name(record_entry, 0)
        mname = self._expand_name(record_entry[0:mname_end_index])
        rname_end_index = end_index_of_name(record_entry, mname_end_index)
        rname = self._expand_name(record_entry[mname_end_index:rname_end_index])
        return mname + rname + record_entry[rname_end_index:]

    def _parse_mx_entry(self, record_entry: bytes) -> bytes:
        # First 16 byte are preference flag, afterwards the domain name
        # is specified
        expanded_name = self._expand_name(record_entry[16:])
        return record_entry[16:] + expanded_name

    def _expand_name(self, string_bytes: bytes) -> bytes:
        payload = b""
        index = 0
        while index < len(string_bytes):
            length = string_bytes[index]
            if length & REPEAT_TYPE_FLAG == REPEAT_TYPE_FLAG:
                original_index = self.index
                length_tuple = struct.unpack_from("!H", string_bytes, index)
                self.index = length_tuple[0] ^ (REPEAT_TYPE_FLAG << 8)
                byte_entry = self._parse_name()
                self.index = original_index
                index += 2
            else:
                index += 1
                end_index = index + length
                byte_entry = string_bytes[index:end_index]
                length_byte = struct.pack("!B", len(byte_entry))
                byte_entry = length_byte + byte_entry
                index = end_index

            payload += byte_entry
        return payload

    def parse_answers(self) -> "List[DNSRecord]":
        return self.parse_records(self.header.num_answers)

    def parse_authorities(self) -> "List[DNSRecord]":
        return self.parse_records(self.header.num_authorities)

    def parse_additionals(self) -> List[DNSRecord]:
        return self.parse_records(self.header.num_additional)

    def _parse_record_name(self) -> str:
        fqdn_name = []
        name_bytes = self._parse_name()
        index = 0
        while name_bytes[index] != 0x00:
            size = name_bytes[index]
            index += 1
            end_index = index + size
            fqdn_name.append(name_bytes[index:end_index].decode())
            index = end_index
        return ".".join(fqdn_name)

    def _parse_name(self) -> bytes:
        payload = b""
        while True:
            size = self.buffer[self.index]
            if size == 0x00:
                payload += bytes((0x00,))
                self.index += 1
                break
            if size & REPEAT_TYPE_FLAG == REPEAT_TYPE_FLAG:
                payload += self._parse_repeat_name()
                break
            else:
                payload += self._parse_bytes()
        return payload

    def _parse_repeat_name(self) -> bytes:
        offset_tuple = self._unpack("!H", 2)
        offset = offset_tuple[0] ^ (REPEAT_TYPE_FLAG << 8)
        real_index = self.index
        self.index = offset
        record_name = self._parse_name()
        self.index = real_index
        return record_name

    def _parse_bytes(self) -> bytes:
        size = self.buffer[self.index]
        self.index += 1
        return bytes((size,)) + self._parse_bytes_of(int(size))

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
