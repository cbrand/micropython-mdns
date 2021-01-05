"""
This example runs a constant service discovery for google chromecast services.
It prints them out if they are added, changed or removed.

As this method stores local state, like service records for refreshing the state
it requires more memory than the one time discovery. However, depending on your use
case it might be better to use this instead of the one time query.
"""

import network
import uasyncio

from mdns_client import Client
from mdns_client.service_discovery import ServiceResponse
from mdns_client.service_discovery.txt_discovery import TXTServiceDiscovery

wlan = network.WLAN(network.STA_IF)
wlan.connect("<SSID>", "<Password>")
while not wlan.isconnected():
    import time

    time.sleep(1.0)

own_ip_address = wlan.ifconfig()[0]

loop = uasyncio.get_event_loop()
client = Client(own_ip_address)
discovery = TXTServiceDiscovery(client)


class ServiceMonitor:
    def service_added(self, service: ServiceResponse) -> None:
        print("Service added: {}".format(service))

    def service_updated(self, service: ServiceResponse) -> None:
        print("Service updated: {}".format(service))

    def service_removed(self, service: ServiceResponse) -> None:
        print("Service removed: {}".format(service))


async def discover():
    discovery.add_service_monitor(ServiceMonitor())
    await discovery.query("_googlecast", "_tcp")

    await uasyncio.sleep(20)


loop.run_until_complete(discover())
print(discovery.current("_googlecast", "_tcp"))
