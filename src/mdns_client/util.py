from mdns_client.constants import TYPE_CNAME, TYPE_MX, TYPE_NS, TYPE_PTR, TYPE_SOA, TYPE_SRV


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
    n = [i.encode("UTF8") if isinstance(i, str) else i for i in n]
    return n


def string_packed_len(string: "List[bytes]") -> int:
    return sum(len(i) + 1 for i in string) + 1


def pack_string(buffer: bytes, string: "List[bytes]") -> bytes:
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
        output_index += part_length + 1
    buffer[output_index] = 0


def might_have_repeatable_payload(record_type: int) -> bool:
    return record_type in (TYPE_NS, TYPE_CNAME, TYPE_PTR, TYPE_SOA, TYPE_MX, TYPE_SRV)
