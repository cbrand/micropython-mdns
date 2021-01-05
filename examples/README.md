# Micropython MDNS #

## Examples ##

For easier utilization a couple of examples are listed in this directory.

They all have been tested on an ESP32 utilizing MicroPython compiled by running `make compile` in the root directory.

You require docker to build the Firmware.

The default firmware can not be used, as it has MDNS enabled and blocks the MDNS port.


<table>
<thead>
<tr><th>Name</th><th>Description</th></tr>
</thead>
<tbody>
<tr><td><a href="request_a_record.py"><img src="https://img.shields.io/badge/request__a__record.py-A%20DNS%20record%20lookup-blue"></a></td><td>DNS lookup via the getaddrinfo() call. It supports querying both MDNS and regular DNS queries.</td></tr>
<tr><td><a href="service_discovery_constant.py"><img src="https://img.shields.io/badge/service__discovery__constant.py-Continuous%20service%20discovery-blue"></a></td><td>MDNS Service discovery. Supports continuous notifications of updates, additions and removals of services in the network.</td></tr>
<tr><td><a href="service_discovery_once.py"><img src="https://img.shields.io/badge/service__discovery__once.py-One%20time%20discovery-blue"></a></td><td>MDNS Service discovery one time requests the current state with a configureable timeout.</td></tr>
<tr><td><a href="service_responder.py"><img src="https://img.shields.io/badge/service__responder.py-MDNS%20service%20announcement-blue"></a></td><td>Support of MDNS service and A record annoucement for publishing own services to the local network.</td></tr>
</tbody>
</table>
