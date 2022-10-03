import struct

import uasyncio

from mdns_client.constants import REPEAT_TYPE_FLAG, TYPE_CNAME, TYPE_MX, TYPE_NS, TYPE_PTR, TYPE_SOA, TYPE_SRV


def dotted_ip_to_bytes(ip: str) -> bytes:
    """
    Convert a dotted IPv4 address string into four bytes, with
    some sanity checks
    """
    ip_ints = [int(i) for i in ip.split(".")]
    if len(ip_ints) != 4 or any(i < 0 or i > 255 for i in ip_ints):
        raise ValueError
    return bytes(ip_ints)


def bytes_to_dotted_ip(a: "Iterable[int]") -> str:
    """
    Convert four bytes into a dotted IPv4 address string, without any
    sanity checks
    """
    return ".".join(str(i) for i in a)


def check_name(n: str) -> "List[bytes]":
    """
    Ensure that a name is in the form of a list of encoded blocks of
    bytes, typically starting as a qualified domain name
    """
    if isinstance(n, str):
        n = n.split(".")
        if n[-1] == "":
            n = n[:-1]
    n = [i.encode("UTF-8") if isinstance(i, str) else i for i in n]
    return n


def string_packed_len(byte_list: "List[bytes]") -> int:
    return sum(len(i) + 1 for i in byte_list) + 1


def name_to_bytes(name: str) -> bytes:
    name_bytes = check_name(name)
    buffer = bytearray(string_packed_len(name_bytes))
    pack_name(buffer, name_bytes)
    return buffer


def pack_name(buffer: bytes, string: "List[bytes]") -> None:
    """
    Pack a string into the start of the buffer
    We don't support writing with name compression, BIWIOMS
    """
    output_index = 0
    for part in string:
        part_length = len(part)
        buffer[output_index] = part_length
        after_size_next_index = output_index + 1
        end_of_pack_name_index = after_size_next_index + part_length
        buffer[after_size_next_index:end_of_pack_name_index] = part
        output_index = end_of_pack_name_index
    buffer[output_index] = 0


def string_to_bytes(item: str) -> bytes:
    buffer = bytearray(len(item) + 1)
    buffer[0] = len(item)
    buffer[1:] = item.encode("utf-8")
    return buffer


def might_have_repeatable_payload(record_type: int) -> bool:
    return record_type in (TYPE_NS, TYPE_CNAME, TYPE_PTR, TYPE_SOA, TYPE_MX, TYPE_SRV)


def byte_count_of_lists(*list_of_lists: "Iterable[bytes]") -> int:
    return sum(sum(len(item) for item in byte_list) for byte_list in list_of_lists)


def fill_buffer(buffer: bytes, item: bytes, offset: int) -> int:
    end_offset = offset + len(item)
    buffer[offset:end_offset] = item
    return end_offset


def end_index_of_name(buffer: bytes, offset: int) -> int:
    """
    Expects the offset to be in the beginning of a name and
    scans through the buffer. It returns the last index of the
    string representation.
    """
    while offset < len(buffer):
        string_part_length = buffer[offset]
        if string_part_length & REPEAT_TYPE_FLAG == REPEAT_TYPE_FLAG:
            # Repeat type flags are always at the end. Meaning the reference
            # should be dereferenced and then the name is completed
            return offset + 2
        elif string_part_length == 0x00:
            return offset + 1
        offset += string_part_length

    raise IndexError("Could not idenitfy end of index")


def bytes_to_name(data: bytes) -> str:
    item = bytes_to_name_list(data)
    return name_list_to_name(item)


def name_list_to_name(data: "List[str]") -> str:
    return ".".join(data)


def bytes_to_name_list(data: bytes) -> "List[str]":
    index = 0
    item = []
    data_length = len(data)
    while index < data_length:
        length_byte = data[index]
        if length_byte == 0x00:
            break

        index += 1
        end_index = index + length_byte
        data_item = data[index:end_index]
        item.append(data_item.decode("utf-8"))
        index = end_index
    return item


def a_record_rdata_to_string(rdata: bytes) -> str:
    ip_numbers = struct.unpack("!BBBB", rdata)
    return ".".join(str(ip_number) for ip_number in ip_numbers)


async def set_after_timeout(event: uasyncio.Event, timeout: float):
    await uasyncio.sleep(timeout)
    event.set()


def txt_data_to_bytes(txt_data: "Dict[str, Union[str, List[str]]]") -> bytes:
    payload = b""
    for key, values in txt_data.items():
        if isinstance(values, str):
            values = [values]
        for value in values:
            if value is None:
                value = ""
            payload += string_to_bytes("{}={}".format(key, value))
    return payload
