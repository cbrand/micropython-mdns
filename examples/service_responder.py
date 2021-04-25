"""
This example implements the service responder. Allowing to publish services with TXT record information
for the own local ip. For this, it requires a host name (if none is given an
micropython-{6 hexadecimal digits}) is generated. To randomize the name you can utilize
responder.generate_random_postfix().

It allows for advanced MDNS discovery for your MicroPython driven project.
"""

import network
import uasyncio

from mdns_client import Client
from mdns_client.responder import Responder

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("<SSID>", "<Password>")
while not wlan.isconnected():
    import time

    time.sleep(1.0)

own_ip_address = wlan.ifconfig()[0]

loop = uasyncio.get_event_loop()
client = Client(own_ip_address)
responder = Responder(
    client,
    own_ip=lambda: own_ip_address,
    host=lambda: "my-awesome-microcontroller-{}".format(responder.generate_random_postfix()),
)


def announce_service():
    responder.advertise("_myawesomeservice", "_tcp", port=12345, data={"some": "metadata", "for": ["my", "service"]})


announce_service()
loop.run_forever()
