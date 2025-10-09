from collections import namedtuple
import gc
import time

import uasyncio

from mdns_client.client import Client
from mdns_client.constants import CLASS_IN, TYPE_A, TYPE_PTR, TYPE_SRV
from mdns_client.service_discovery.service_response import ServiceResponse
from mdns_client.structs import DNSQuestion, DNSRecord, DNSResponse, ServiceProtocol, SRVRecord
from mdns_client.util import a_record_rdata_to_string, bytes_to_name_list, name_list_to_name


record_buffer = namedtuple("RecordBuffer", ["record", "invalid_at"])


class ServiceChange:
    def __init__(self) -> None:
        self.added = set()
        self.removed = set()
        self.updated = set()

    @property
    def has_update(self) -> bool:
        return len(self.added) or len(self.removed) or len(self.updated)


class ServiceDiscovery:
    def __init__(
        self,
        client: Client,
        debug: bool = False,
        a_records_buffer_size: int = 10,
        a_records_buffer_timeout_ms: int = 500,
        dns_sd_discovery: bool = False,
    ) -> None:
        self.client = client
        self.monitored_services = {}
        self.started = False
        self._records_by_target = {}
        self._a_records_by_target_buffer = set()
        self._a_records_buffer_size = a_records_buffer_size
        self._a_records_buffer_timeout_ms = a_records_buffer_timeout_ms

        self._enqueued_service_records = set()
        self._enqueued_target_records = set()
        self._service_monitors = set()
        self._current_change = ServiceChange()
        self._dns_sd_discovery = dns_sd_discovery
        self.timeout = 2.0
        self.debug = debug

    def start_if_necessary(self) -> None:
        if self.started:
            return

        self.start()

    def add_service_monitor(self, service_monitor: "ServiceMonitor") -> None:
        self._service_monitors.add(service_monitor)

    def remove_service_monitor(self, service_monitor: "ServiceMonitor") -> None:
        self._service_monitors.remove(service_monitor)

    def start(self) -> None:
        if self.started:
            raise RuntimeError("Already started")
        self.started = True
        self.dprint("Start discovery module")

        loop = uasyncio.get_event_loop()
        loop.create_task(self._change_loop())
        callback = self.client.add_callback(self._on_response)
        self.callback_id = callback.id

    async def _change_loop(self) -> None:
        while self.started and not self.client.stopped:
            await self._tick()
            await uasyncio.sleep(self.timeout)

    async def _tick(self) -> None:
        now = time.ticks_ms()
        if self.client.stopped:
            return

        for services in self.monitored_services.values():
            to_remove = set()
            for service in services.values():
                if service.expired_at(now):
                    self.dprint(
                        "Service {} expired at {} ticks (Current: {} ticks)".format(
                            service.name, service.invalid_at, now
                        )
                    )
                    to_remove.add(service)
                elif service.should_refresh_at(now):
                    self.dprint(
                        (
                            "Service {} will be refreshed via MDNS with expiry at {} ticks "
                            "and TTL {} (Current: {} ticks)"
                        ).format(service.name, service.invalid_at, service.ttl, now)
                    )
                    await service.refresh_with(self.client)

            for to_remove_item in to_remove:
                self._remove_item(to_remove_item)

        if self._current_change.has_update:
            self._propagate_current_change()
            self._current_change = ServiceChange()

        self._clean_up_buffer()
        gc.collect()

    def _propagate_current_change(self):
        for service_monitor in self._service_monitors:
            for added in self._current_change.added:
                service_monitor.service_added(added)
            for updated in self._current_change.updated:
                service_monitor.service_updated(updated)
            for removed in self._current_change.removed:
                service_monitor.service_removed(removed)

    def stop(self) -> None:
        if not self.started:
            return

        self.client.remove_id(self.callback_id)
        self.monitored_services.clear()
        self._records_by_target.clear()
        self._a_records_by_target_buffer.clear()
        self._service_monitors.clear()
        self._enqueued_service_records.clear()
        self._enqueued_target_records.clear()
        self._current_change = ServiceChange()
        self.started = False

    async def query(self, protocol: str, service: str) -> None:
        self.start_if_necessary()
        service_protocol = ServiceProtocol(protocol, service)
        self._register_monitored_service(service_protocol)
        loop = uasyncio.get_event_loop()
        loop.create_task(self._request_once(service_protocol))

    def stop_watching(self, protocol: str, service: str) -> None:
        self._remove_from_monitor(ServiceProtocol(protocol, service))

    def current(self, protocol: str, service: str) -> "Iterable[ServiceResponse]":
        service_protocol = ServiceProtocol(protocol, service)
        return tuple(self.monitored_services.get(service_protocol, {}).values())

    async def query_once(self, protocol: str, service: str, timeout: float = None) -> "Iterable[ServiceResponse]":
        timeout = self.timeout if timeout is None else timeout
        started_before = self.started
        client_started_before = not self.client.stopped
        self.start_if_necessary()
        service_protocol = ServiceProtocol(protocol, service)
        existed = service_protocol in self.monitored_services
        monitored_services = self._register_monitored_service(service_protocol)
        await self.query(protocol, service)

        await uasyncio.sleep(timeout)
        result = tuple(monitored_services)
        if not existed:
            self._remove_from_monitor(service_protocol)

        if not started_before:
            self.stop()

        if not client_started_before:
            self.client.stop()
        return result

    def _register_monitored_service(self, service_protocol: ServiceProtocol) -> dict:
        if service_protocol not in self.monitored_services:
            self.dprint("Monitoring service protocol: {}".format(service_protocol))
        return self.monitored_services.setdefault(service_protocol, dict())

    def _remove_from_monitor(self, service_protocol: ServiceProtocol) -> None:
        if service_protocol not in self.monitored_services:
            return

        self.dprint("Removing service protocol from monitoring: {}".format(service_protocol))
        for monitored_service in self.monitored_services[service_protocol]:
            self._remove_item(monitored_service)

    def _remove_item(self, service: ServiceResponse) -> None:
        self._remove_item_from_target(service.target, service)
        self._remove_item_from_target(service.name, service)

        service_dict = self.monitored_services.get(service.protocol, None)
        if service in service_dict:
            self._current_change.removed.add(service)
            del service_dict[service]

    def _remove_item_from_target(self, target: str, service: ServiceResponse) -> None:
        target = target.lower()
        res = self._records_by_target.get(target, None)
        if res:
            if service in res:
                res.remove(service)
            if len(res) == 0:
                del self._records_by_target[target]

    async def _request_once(self, service_protocol: ServiceProtocol) -> None:
        if self._dns_sd_discovery:
            await self._run_service_discovery_request()
        await self.client.send_question(DNSQuestion(service_protocol.to_name(), TYPE_PTR, CLASS_IN))

    async def _run_service_discovery_request(self) -> None:
        await self.client.send_question(DNSQuestion("_services._dns_sd._udp.local", TYPE_PTR, CLASS_IN))

    async def _on_response(self, response: DNSResponse) -> None:
        for message in self._records_of(response):
            self._on_record(message)

        questions = []
        for service_record in self._enqueued_service_records:
            questions.append(DNSQuestion(service_record, TYPE_SRV, CLASS_IN))
        for host_resolve in self._enqueued_target_records:
            questions.append(DNSQuestion(host_resolve, TYPE_A, CLASS_IN))
        if len(questions):
            await self.client.send_question(*questions)

        gc.collect()

    def _records_of(self, response: DNSResponse) -> "Iterable[DNSRecord]":
        return response.records

    def _on_record(self, record: DNSRecord) -> None:
        if record.record_type == TYPE_PTR:
            self._on_ptr_record(record)
        elif record.record_type == TYPE_SRV:
            self._on_srv_record(record)
        elif record.record_type == TYPE_A:
            self._on_a_record(record)

    def _on_ptr_record(self, record: DNSRecord) -> None:
        pointer_data = bytes_to_name_list(record.rdata)
        if len(pointer_data) < 4:
            return

        service_protocol = ServiceProtocol(pointer_data[-3], pointer_data[-2])
        if service_protocol in self.monitored_services:
            self._enqueue_srv_for(name_list_to_name(pointer_data))

    def _enqueue_srv_for(self, srv_name: str) -> None:
        self._enqueued_service_records.add(srv_name.lower())

    def _on_srv_record(self, record: DNSRecord) -> None:
        if record.name in self._enqueued_service_records:
            self._enqueued_service_records.remove(record.name.lower())

        srv_name_items = record.name.split(".")
        if len(srv_name_items) < 4:
            return

        service_protocol = ServiceProtocol(srv_name_items[-3], srv_name_items[-2])
        if service_protocol not in self.monitored_services:
            return

        srv_record = SRVRecord.from_dns_record(record)
        response = ServiceResponse(
            record.name, srv_record.priority, srv_record.weight, srv_record.port, srv_record.target
        )
        response.invalid_at = record.invalid_at
        response.ttl = record.time_to_live
        if response not in self.monitored_services[service_protocol]:
            self.dprint("Found new service {}".format(srv_record.name))
            self.monitored_services[service_protocol][response] = response
            self._current_change.added.add(response)
        else:
            self.dprint("Got SRV message for existing service {}".format(srv_record.name))
            old_response = self.monitored_services[service_protocol][response]

            if old_response != response:
                for attribute in ["name", "priority", "weight", "port", "ttl"]:
                    setattr(old_response, attribute, getattr(response, attribute))
                self.dprint("Updating changed service {}".format(srv_record.name))
                old_response.ips.clear()
                self._current_change.updated.add(old_response)
            old_response.refreshed_at = None
            old_response.invalid_at = response.invalid_at

        self._records_by_target.setdefault(response.name.lower(), set()).add(response)
        self._records_by_target.setdefault(response.target.lower(), set()).add(response)
        self._enqueued_target_records.add(srv_record.target)

        for item in self._a_records_by_target_buffer:
            if item.record.name.lower() in self._records_by_target:
                self._on_a_record(item.record)
                self._a_records_by_target_buffer.remove(item)

    def _on_a_record(self, record: DNSRecord) -> None:
        record_name = record.name.lower()

        if record_name in self._enqueued_target_records:
            self._enqueued_target_records.remove(record_name)

        if record_name not in self._records_by_target:
            self._add_to_a_record_buffer(record)
            return

        for item in self._records_by_target[record_name]:
            ip_address = a_record_rdata_to_string(record.rdata)
            if ip_address not in item.ips:
                self.dprint("Updating ip addresses for service {} by adding {}".format(item.name, ip_address))
                item.ips.add(a_record_rdata_to_string(record.rdata))
                if item not in self._current_change.added:
                    self._current_change.updated.add(item)

            record_invalidation = record.invalid_at
            item.invalid_at = min(item.invalid_at or record_invalidation, record_invalidation)
            item.ttl = min(item.ttl or record.time_to_live, record.time_to_live)

    def dprint(self, message: str) -> None:
        if self.debug:
            print("MDNS Discovery: {}".format(message))

    def _add_to_a_record_buffer(self, record: DNSRecord) -> None:
        self.dprint("Adding A record which was not in active discovery to buffer {}".format(record))
        self._a_records_by_target_buffer.add(record_buffer(record, time.ticks_ms() + self._a_records_buffer_timeout_ms))
        self._ensure_no_buffer_overflow()

    def _clean_up_buffer(self) -> None:
        if len(self._a_records_by_target_buffer) == 0:
            return
        self._a_records_by_target_buffer = set(
            filter(lambda record_buffer: record_buffer.invalid_at > time.ticks_ms(), self._a_records_by_target_buffer)
        )

    def _ensure_no_buffer_overflow(self) -> None:
        if len(self._a_records_by_target_buffer) >= self._a_records_buffer_size:
            records_buffer_ordered = sorted(
                self._a_records_by_target_buffer, key=lambda record_buffer: record_buffer.invalid_at
            )
            records_buffer_ordered = records_buffer_ordered[: self._a_records_buffer_size]
            self._a_records_by_target_buffer = set(records_buffer_ordered)
