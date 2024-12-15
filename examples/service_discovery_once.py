"""
This example shows a one time discovery of available google cast services in the network.
This is probably the most efficient way to discover services, as it doesn't store any additional
local state after the query is done and should be used if memory is an issue in your application.
"""

import network
import uasyncio

from mdns_client import Client
from mdns_client.service_discovery.txt_discovery import TXTServiceDiscovery

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("<SSID>", "<Password>")
while not wlan.isconnected():
    import time

    time.sleep(1.0)

own_ip_address = wlan.ifconfig()[0]

loop = uasyncio.get_event_loop()
client = Client(own_ip_address)
discovery = TXTServiceDiscovery(client)


async def discover_once():
    print(await discovery.query_once("_googlecast", "_tcp", timeout=1.0))


loop.run_until_complete(discover_once())
