# API Reference

The API consists of various classes. The main logic is automatically
spinned up inside of a [`uasyncio` task](https://docs.micropython.org/en/latest/library/uasyncio.html#uasyncio.create_task)
which is started and stopped when required.

The document doesn't outline all classes and functionality in the library.
Instead, it outlines the API which can be seen as **stable** and intended for public use.

## `mdns_client.Client`

[![Link to the mdns_client.Client code](https://img.shields.io/badge/mdns__client-Client-orange)](src/mdns_client/client.py#30)

The client includes the basic logic for requesting and sending MDNS packages. It has a pluggable system to react on MDNS Record changes on the network.

All functionality in this library is based on this client.

```python
import uasyncio
import network

from mdns_client import Client

loop = uasyncio.get_event_loop()
wlan = network.WLAN(network.STA_IF)
client = Client(wlan.ifconfig()[0])

print(loop.run_until_complete(client.getaddrinfo("the-other-device.local", 80)))
```

**Reference**

```python
Client.__init__(local_addr: str, debug: bool = False)
```

Initializes the client. It requires the local ip address for subscribing
to multicast messages.

If debug is enabled, the client will issue debug message via the
print() statement.

```python
Client.add_callback(
    callback: "Callable[[DNSResponse], Awaitable[None]]",
    remove_if: "Optional[Callable[[DNSResponse], Awaitable[bool]]]" = None,
    timeout: "Optional[int]" = None
) -> Callback
```

Registers a callback function which gets executed every time
an MDNS message has been received and deserialized into a [DNSResponse](#DNSResponse) object.

Optionally, a function can be passed in which gets executed to verify if
the callback should be deleted.

If a timeout is given, the callback will be removed after the specified
time has passed.

Returns the registered callback object which has an `id` which can be used
to manually deregister the response from the client.

```python
Client.remove_id(callback_id: int) -> bool
```

Removes a registered callback with the given id.

Returns True if the deletion was done and false, if no callback with the
passed id has been found.

```python
async Client.send_question(*questions: DNSQuestion) -> None
async Client.send_response(response: DNSResponse) -> None
```

Sends a DNS resolution question or response into the local network. This is mainly
used by other parts of the library but is considered as public, if
an extension of the library is required.

```python
async Client.getaddrinfo(
    host: "Union[str, bytes, bytearray]",
    port: "Union[str, int, None]",
    family: int = 0,
    type: int = 0,
    proto: int = 0,
    flags: int = 0,
) -> "List[Tuple[int, int, int, str, Tuple[str, int]]]"
```

This implements the same interface as exists in the standard library
on [socket objects for DNS resolution](https://docs.micropython.org/en/latest/library/usocket.html#usocket.getaddrinfo).
The function supports both resolutions of local MDNS and normal
DNS queries. Addresses which are prefixed with `.local` are resolved
via MDNS, all others get sent to the configured `DNS` server via
the [`socket.getaddrinfo`](https://docs.micropython.org/en/latest/library/usocket.html#usocket.getaddrinfo) function.

```python
host_name = str
ip_v4_address = str
async Client.mdns_getaddr(self, host: str) -> Tuple[host_name, ip_v4_address]
```

Resolves a pure MDNS A record requests. It returnes
the record name as the first entry and the ipv4 address as the second
tuple entry.

## `mdns_client.responder.Responder`

[![Link to the mdns_client.responder.Responder code](https://img.shields.io/badge/mdns__client.responder-Responder-orange)](src/mdns_client/responer.py#29)

This class is used for supporting service annoucements for own services
supported by the application running on this Microcontroller.

```python
import uasyncio
import network

from mdns_client import Client
from mdns_client.responder import Responder, generate_random_postfix

loop = uasyncio.get_event_loop()
wlan = network.WLAN(network.STA_IF)
local_ip = wlan.ifconfig()[0]
client = Client(local_ip)
postfix = generate_random_postfix()
responder = Responder(client, own_ip=local_ip, host=lambda: "my-device-{}".format(postfix))
responder.advertise("_my_awesome_protocol", "_tcp", port=12345)
```

**Reference**

```python
Responder.__init__(
    client: Client,
    own_ip: "Union[None, str, Callable[[], str]]",
    host: "Union[None, str, Callable[[], str]]" = None,
    debug: bool = False,
) -> None
```

The responder is initialized with a client object. It requires
a callback or fixed value identifying the local ip.

Additionally, a hostname can be passed into the constructor which identifies the name how the responder advertises itself. If none is passed,
`micropython-{six digit hexadecimal value}` is generated.

The `debug` flag can be set to `True` if debug messages should be printed
via the `print()` command.

```python
Responder.advertise(
    protocol: str,
    service: str,
    port: int,
    data: "Optional[Dict[str, Union[List[str], str]]]" = None,
    service_host_name: "Optional[str]" = None
) -> None
```

Advertises the specified protocol/service to be available on the given port.

Optionally, data can be passed, which is published as a `TXT` record to provide further instructions to third parties on how to handle the service. . If you want to update the `TXT` data, you can call the function again, which will overwrite the previous setting if you pass the same `protocol`/`service` combination to it.

In very special cases, you might want to set your own service hostname different from the hostname in the A record of the controller. This is where `service_host_name` can be used to generate a dedicated hostname for the advertised service, such as `myservicehostname._myawesomeservice._tcp.local`.

```python
Responder.withdraw(protocol: str, service: str) -> None
```

Removes the service annoucement support of the passed `protocol`/`service` tuple.

## `mdns_client.service_discovery.ServiceDiscovery`

[![Link to the mdns_client.service_discovery.ServiceDiscovery code](https://img.shields.io/badge/mdns__client.service__discovery-ServiceDiscovery-orange)](src/mdns_client/service_discovery/discovery.py#24)
[![Link to the mdns_client.service_discovery.txt_discovery.TxtServiceDiscovery code](https://img.shields.io/badge/mdns__client.service__discovery.txt__discovery-TXTServiceDiscovery-orange)](src/mdns_client/service_discovery/txt_discovery.py#15)

Also [`mdns_client.service_discovery.txt_discovery.TXTServiceDiscovery`](src/mdns_client/service_discovery/txt_discovery.py#15)
provides the same interface.

The `ServiceDiscovery` class and the `TXTServiceDiscovery` class provide possibilities for service discovery on the local network. They implement the same public interface. If the `TXTServiceDiscovery` is used, it will additional populate all records with any metadata which is passed via TXT records for the services.

```python
import uasyncio
import network

from mdns_client import Client
from mdns_client.service_discovery import ServiceDiscovery

loop = uasyncio.get_event_loop()
wlan = network.WLAN(network.STA_IF)
local_ip = wlan.ifconfig()[0]
client = Client(local_ip)
discovery = ServiceDiscovery(client)
loop.run_until_complete(discovery.query_once("_googlecast", "_tcp", timeout=1.0))
```

**Reference**

```python
ServiceDiscovery.__init__(client: Client, debug: bool = False)
```

Initializes the service discovery handler. Requires the `Client` object.

if `debug` is set to `True` messages helping debugging the component will be sent via the `print` statement.

```python
ServiceDiscovery.add_service_monitor(service_monitor: "ServiceMonitor") -> None
```

Adds a specific service monitor to the discovery handler. Each time a service is updated, added or removed and marked as relevant it will be sent to the serivce monitor till it has been unregistered via `remove_service_monitor`.

The `ServiceMonitor` must implement these functions:

```python
class ServiceMonitor:
    def service_added(self, service: ServiceResponse) -> None:
        pass
    def service_updated(self, service: ServiceResponse) -> None:
        pass
    def service_removed(self, service: ServiceResponse) -> None:
        pass
```

```python
ServiceDiscovery.remove_service_monitor(service_monitor: "ServiceMonitor") -> None
```

Removes the specified service monitor from the discovery logic. If the service monitor hasn't been registered before, raises a `KeyError`.

```python
async ServiceDiscovery.query(protocol: str, service: str) -> None
```

Marks the specified `protocol`/`service` as to be resolved. Once it is added to the query, the records are being taken in. Also issues a query for
resolving the services which are currently available on the connected network.

```python
async ServiceDiscovery.query_once(protocol: str, service: str, timeout: float = None) -> "Iterable[ServiceResponse]"
```
***Note:** Despite the call being named `query_once()`, it starts asyncio tasks which keep running -- and querying -- after the call returned. To actually stop respective background tasks, `client.stop()` needs to be called.*

Asks the service discovery to resolve the `protocol`/`service` combination once. After the passed `timeout` (or a default one) has passed return all services which have been identified in between.

If the `protocol`/`service` combination hasn't already been enqueued before (via a `query` call), it will afterwards remove the query request. Because of this behavior, the call is on the long run more memory efficient than constantly scanning the network for service records via the `query` function.

```python
ServiceDiscovery.current(protocol: str, service: str) -> "Iterable[ServiceResponse]"
```

Returns the currently known services which provide the passed `protocol`/`service` on the network. It doesn't itself do any network calls and checks the state from the local cache. Thus, it should be used in combination with the `query` function.

## Structs

### `mdns_client.struct.DNSResponse`

[![Link to the mdns_client.struct.DNSResponse code](https://img.shields.io/badge/mdns__client.structs-DNSResponse-orange)](src/mdns_client/structs.py#78)

The DNSResponse is a namedtuple representing a received or to be sent MDNS-Response.

```python
class DNSResponse:
    transaction_id: int
    message_type: int
    questions: "List[DNSQuestion]"
    answers: "List[DNSRecord]"
    authorities: "List[DNSRecord]"
    additional: "List[DNSRecord]"
    is_response: bool
    is_request: bool
    records: "Iterable[DNSRecord]"
```

**Reference**

```python
DNSResponse.to_bytes() -> bytes
```

Returns a representation of the DNSResponse in bytes as they are sent
inside of a UDP package.

### `mdns_client.struct.DNSRecord`

[![Link to the mdns_client.struct.DNSRecord code](https://img.shields.io/badge/mdns__client.structs-DNSRecord-orange)](src/mdns_client/structs.py#47)

The DNSRecord namedtuple represents an individual record which has been
received or will be sent via a DNSResponse.

```python
class DNSRecord:
    name: str
    record_type: int
    query_class: int
    time_to_live: int
    rdata: bytes
    invalid_at: int  # The time (in machine.ticks_ms) when the record is invalid
```

**Reference**

```python
DNSRecord.to_bytes() -> bytes
```

Returns a representation of the `DNSRecord` in bytes as they are sent
inside of a UDP package within a `DNSResponse`.

### `mdns_client.struct.DNSQuestion`

[![Link to the mdns_client.struct.DNSQuestion code](https://img.shields.io/badge/mdns__client.structs-DNSQuestion-orange)](src/mdns_client/structs.py#17)

The DNSQuestion represents a request being sent via MDNS to resolve a
specific domain record of a specified type.

```python
class DNSQuestion:
    query: str
    type: int
    query_class: int
```

The `type` can be resolved via the [`constants.py`](src/mdns_client/constants.py#L21-L31) file.
Also the `query_class` types are [there](src/mdns_client/constants.py#L16-L19). However, currently only the
`CLASS_IN` is used.

**Reference**

```python
DNSQuestion.to_bytes() -> bytes
```

Returns a representation of the `DNSQuestion` in bytes as they are sent
inside of a UDP package within a `DNSResponse`.

### `mdns_client.service_discovery.ServiceResponse`

[![Link to the mdns_client.struct.DNSQuestion code](https://img.shields.io/badge/mdns__client.service__discovery.service__response-ServiceResponse-orange)](src/mdns_client/service_discovery/service_response.py#7)

The `ServiceResponse` includes information of a service which is available on the local network and has been discovered via the `ServiceDiscovery` class or one of its subclasses.

```python
class ServiceResponse:
    name: str
    priority: int
    weight: int
    port: int
    ips: Set[str]
    txt_records: Optional[Dict[str, List[str]]]

    invalid_at: Optional[int]
    # time.ticks_ms when the service is no longer valid
    # according to the passed time to live

    ttl: Optional[int]
    # The time the service response can be considered as
    # valid when it was received from the MDNS responder.
```

**Reference**

```python
ServiceResponse.expired_at(timing: int) -> bool
```

Returns if the service response is expired at the specified time.
The timing should be the time according to [`time.ticks_ms()`](https://docs.micropython.org/en/latest/library/utime.html#utime.ticks_ms).
