# Micropython MDNS #

## Examples ##

For easier utilization a couple of examples are listed in this directory.

They all have been tested on an ESP32 utilizing MicroPython compiled by running `make compile` in the root directory.

You require docker to build the Firmware.

The default firmware can not be used, as it has MDNS enabled and blocks the MDNS port.


### Resolve an A record ###
<a href="request_a_record.py"><img src="https://img.shields.io/badge/request__a__record.py-A%20DNS%20record%20lookup-blue"></a>

DNS lookup via the getaddrinfo() call. It supports querying both MDNS and regular DNS queries.

### Continuous MDNS service discovery ###

<a href="service_discovery_constant.py"><img src="https://img.shields.io/badge/service__discovery__constant.py-Continuous%20service%20discovery-blue"></a>

MDNS Service discovery. Supports continuous notifications of updates, additions and removals of services in the network.


### One time MDNS service discovery ###

<a href="service_discovery_once.py"><img src="https://img.shields.io/badge/service__discovery__once.py-One%20time%20discovery-blue"></a>

MDNS Service discovery one time requests the current state with a configureable timeout.

### MDNS Service Responder / Annoucement ###

<a href="service_responder.py"><img src="https://img.shields.io/badge/service__responder.py-MDNS%20service%20announcement-blue"></a>

MDNS service record annoucement for publishing own services to the local network with Metadata being published via a TXT record.
