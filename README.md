# Micropython MDNS #

[![PyPi](https://img.shields.io/pypi/v/micropython-mdns) ![MIT licensed](https://img.shields.io/pypi/l/micropython-mdns)](https://pypi.org/project/micropython-mdns/)

![Image showing service discovery](images/service-discovery.gif)

A pure Python implementation of [MDNS](https://tools.ietf.org/html/rfc6762) and the [Service Discovery](https://tools.ietf.org/html/rfc6763) protocol over MDNS 
for [MicroPython](https://micropython.org/).

## Installation ##

The library is available on PyPi and can be installed via upip.

```python
import upip
upip.install("micropython-mdns")
```

For using this library, native C type implementations of MDNS which use the MDNS service port need to be disabled. For example, this project has been developed
on the ESP32 which MicroPython implementation per default has a basic MDNS implementation available. This does only support local A record lookups and A record
responding of its own host address. 

The [releases page](https://github.com/cbrand/micropython-mdns/releases) on this project publishes a firmware.bin which is MicroPython 1.13 with MDNS disabled in each release for easy usage. It can also be built when
having docker locally installed by running in the console the build command:

```bash
make build
```

Refer to the [`config`](config) directory to see the configuration files when baking this into your own MicroPython ESP32 build.

Other MicroPython implementations might not require any changes inside of the firmware.

## Usage ##

The library requires [`uasyncio`](https://docs.micropython.org/en/latest/library/uasyncio.html) to function. All handling is done asynchronously.

Examples on how to utilize the libraries can be found in the [`examples`](https://github.com/cbrand/micropython-mdns/tree/main/examples) folder.

## Reference ##

A basic API reference for the public API is inside of the [REFERENCE.md](https://github.com/cbrand/micropython-mdns/blob/main/REFERENCE.md).

## Caveats ##

- Depending on your MicroPython implementation, you must disable MDNS in the firmware.
- Currently no support for IPv6 is implemented.
- Depending how chatty the network is, service responders and discovery might require a lot of memory. If the memory is filled by the buffer of the underlying socket, [the socket is closed and reopened](https://github.com/cbrand/micropython-mdns/blob/d3dd54f809629ca41c525f5dec86963a6d75e903/src/mdns_client/client.py#L100) which looses data. It, however, seems to work fine enough in tests on an ESP32 without external memory. Depending on the project size, a module with external RAM might be advisable.

## License ##

The library is published under the [MIT](LICENSE) license.
