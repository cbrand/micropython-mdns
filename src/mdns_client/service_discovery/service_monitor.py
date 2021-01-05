from ..structs import ServiceProtocol


class ServiceMonitor:
    def service_added(self, service: ServiceProtocol) -> None:
        raise NotImplementedError()

    def service_updated(self, service: ServiceProtocol) -> None:
        raise NotImplementedError()

    def service_removed(self, service: ServiceProtocol) -> None:
        raise NotImplementedError()
