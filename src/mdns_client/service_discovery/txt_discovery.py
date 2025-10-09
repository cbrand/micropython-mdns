from mdns_client.constants import TYPE_A, TYPE_PTR, TYPE_SRV, TYPE_TXT
from mdns_client.service_discovery.discovery import ServiceDiscovery
from mdns_client.structs import DNSRecord, DNSResponse
from mdns_client.util import bytes_to_name_list

TYPE_KEYS = (TYPE_PTR, TYPE_SRV, TYPE_A, TYPE_TXT)


def sort_record_by_type(response: DNSResponse) -> int:
    if response.record_type in TYPE_KEYS:
        return TYPE_KEYS.index(response.record_type)
    return -1


class TXTServiceDiscovery(ServiceDiscovery):
    def _on_record(self, record: DNSRecord) -> None:
        super()._on_record(record)
        if record.record_type == TYPE_TXT:
            self._on_txt_record(record)

    def _records_of(self, response: DNSResponse) -> "Iterable[DNSRecord]":
        return sorted(super()._records_of(response), key=sort_record_by_type)

    def _on_txt_record(self, record: DNSRecord) -> None:
        record_name = record.name.lower()
        if record_name not in self._records_by_target:
            return

        target = self._records_by_target[record_name]
        txt_records = bytes_to_name_list(record.rdata)
        txt_entries = {}
        for txt_record in txt_records:
            if "=" in txt_record:
                key, value = txt_record.split("=", 1)
                txt_entries.setdefault(key, []).append(value)

        for target_item in target:
            target_item.txt_records = txt_entries
