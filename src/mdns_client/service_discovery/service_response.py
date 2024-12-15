import time

from mdns_client.constants import CLASS_IN, TYPE_SRV
from mdns_client.structs import DNSQuestion, SRVMixin


class ServiceResponse(SRVMixin):
    def __init__(self, name: str, priority: int = 0, weight: int = 0, port: int = 0, target: str = ""):
        self.name = name
        self.priority = priority
        self.weight = weight
        self.port = port
        self.target = target
        self.ips = set()
        self.txt_records = None
        self.invalid_at = None
        self.refreshed_at = None
        self.ttl = None

    def __repr__(self) -> str:
        if self.txt_records is None:
            txt_records = ""
        else:
            txt_records = " txt={}".format(self.txt_records)
        return "<ServiceResponse name={} priority={} weight={} target={} port={} ips={}{}>".format(
            self.name, self.priority, self.weight, self.target, self.port, self.ips, txt_records
        )

    def __hash__(self) -> int:
        result = 0
        for attribute in ["port", "target"]:
            result = result ^ hash(getattr(self, attribute))
        return result

    def __eq__(self, other: "ServiceResponse") -> bool:
        if not isinstance(other, ServiceResponse):
            return False

        for attribute in ["name", "priority", "weight", "port", "ttl"]:
            if getattr(self, attribute) != getattr(other, attribute):
                return False

        return True

    @property
    def ttl_ms(self) -> "Optional[int]":
        if self.ttl is None:
            return None

        return self.ttl * 1000

    def should_refresh_at(self, timing: int) -> bool:
        if self.invalid_at is None or self.ttl is None:
            return False

        if timing >= self.invalid_at:
            return True

        difference = self.invalid_at - timing
        ttl_suggests_refresh = difference < self.ttl_ms / 2

        if not ttl_suggests_refresh or self.refreshed_at is None:
            return ttl_suggests_refresh

        difference = timing - self.refreshed_at
        # Refresh every 120 seconds if it is not expired
        return not self.expired_at(timing) and difference > 120 * 1000

    def expired_at(self, timing: int) -> bool:
        if self.invalid_at is None:
            return False

        return timing >= self.invalid_at

    async def refresh_with(self, client: "Client") -> None:
        self.refreshed_at = time.ticks_ms()
        if client.stopped:
            return
        await client.send_question(DNSQuestion(self.name, TYPE_SRV, CLASS_IN))
