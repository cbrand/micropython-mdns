from micropython import const

MAX_PACKET_SIZE = const(1700)

MDNS_ADDR = "224.0.0.251"
MDNS_PORT = const(5353)
DNS_TTL = const(2 * 60)

FLAGS_QR_MASK = const(0x8000)
FLAGS_QR_QUERY = const(0x0000)
FLAGS_QR_RESPONSE = const(0x8000)
FLAGS_QR_AUTHORITATIVE = const(0x0400)

FLAGS_AA = const(0x0400)

CLASS_IN = const(1)
CLASS_ANY = const(255)
CLASS_MASK = const(0x7FFF)
CLASS_UNIQUE = const(0x8000)

TYPE_A = const(1)
TYPE_NS = const(2)
TYPE_CNAME = const(5)
TYPE_SOA = const(6)
TYPE_WKS = const(11)
TYPE_PTR = const(12)
TYPE_MX = const(15)
TYPE_TXT = const(16)
TYPE_AAAA = const(28)
TYPE_SRV = const(33)
TYPE_ANY = const(255)

DEFAULT_TTL = const(120)
REPEAT_TYPE_FLAG = const(0xC0)

LOCAL_MDNS_SUFFIX = ".local"
