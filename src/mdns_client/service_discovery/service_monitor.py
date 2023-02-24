from mdns_client.service_discovery.service_response import ServiceResponse


class ServiceMonitor:
    def service_added(self, service: ServiceResponse) -> None:
        raise NotImplementedError()

    def service_updated(self, service: ServiceResponse) -> None:
        raise NotImplementedError()

    def service_removed(self, service: ServiceResponse) -> None:
        raise NotImplementedError()
