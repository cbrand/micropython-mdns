# Micropython MDNS

[![PyPi](https://img.shields.io/pypi/v/micropython-mdns) ![MIT licensed](https://img.shields.io/pypi/l/micropython-mdns)](https://pypi.org/project/micropython-mdns/)

![Image showing service discovery](https://raw.githubusercontent.com/cbrand/micropython-mdns/main/images/service-discovery.gif)

A pure Python implementation of [MDNS](https://tools.ietf.org/html/rfc6762) and the [Service Discovery](https://tools.ietf.org/html/rfc6763) protocol over MDNS
for [MicroPython](https://micropython.org/).

## Intended Audience

You should not use this library if you "just" require MDNS A record lookup and Host annoucement if there is already baked in support in your MicroPython distribution.
This is for example the case with the default ESP32 MicroPython distribution since v1.12. This will be in all cases more resource efficient.

If you, however, require additional functionality like Service Discovery and Annoucement, you should use this library. It supports all functionality of existing
basic MDNS implementations plus these features. You will not loose any functionality.

## Installation

The library is available on PyPi and can be installed via upip.

```python
import upip
upip.install("micropython-mdns")
```

Alternatively you can also use the new [`mip`](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip) package manager:

```python
import mip
mip.install("github:cbrand/micropython-mdns")
```

For using this library, native C type implementations of MDNS which use the MDNS service port need to be disabled. For example, this project has been developed
on the ESP32 which MicroPython implementation per default has a basic MDNS implementation available. This does only support local A record lookups and A record
responding of its own host address.

The [releases page](https://github.com/cbrand/micropython-mdns/releases) on this project publishes a firmware.mp.1.23.esp32.bin for MicroPython 1.23 with MDNS disabled and the mdns python module included in each release for easy usage. Other Micropython versions are also supported. Other boards are supported and you are welcome to add additional Dockerfiles in a PR which build the module compatible for other boards.
All versions can also be built when having docker locally installed by running in the console the build command:

```bash
make build
```

Individually it is also possible to build the desired version via:

```bash
make compile-micropython-1-15
make compile-micropython-1-16
make compile-micropython-1-17
make compile-micropython-1-18
make compile-micropython-1-19
make compile-micropython-1-20
make compile-micropython-1-21
make compile-micropython-1-22
make compile-micropython-1-23
make compile-micropython-1-24
```

Refer to the [`config`](https://github.com/cbrand/micropython-mdns/tree/main/config/boards) directory to see the configuration files when baking this into your own MicroPython ESP32 build.

### Raspberry Pi Pico

For Raspberry Pi Pico support see the corresponding Dockerfile on how to compile it in linux [`Dockerfile.micropython.1.23.rp2`](https://github.com/cbrand/micropython-mdns/tree/main/Dockerfile.micropython.1.23.rp2). The following command will build a docker container that can be used to create a new micropython firmware with the in-built mDNS disabled:

    dockerbuild -f Dockerfile.micropython.<version>.rp2 -t micropython-nodns:<version> .

and the following command will perform the compilation and provide the resulting firmware as "build\firmware.uf2":

    docker run -v .\build:/opt/app/micropython/ports/rp2/build-RPI_PICO_W micropython-nodns:<version>

(The directory "build" should not exist when this is run or there could be conflict with authorization for the docker daemon; if the docker daemon is free to create the directory, this will work better. Change <version> the version of Micropython you wish to build, and adjust the path separator in ".\build" for your system.)

### Other Implementations

Other MicroPython implementations might not require any changes inside of the firmware.

## Usage

The library requires [`uasyncio`](https://docs.micropython.org/en/latest/library/uasyncio.html) to function. All handling is done asynchronously.

Examples on how to utilize the libraries can be found in the [`examples`](https://github.com/cbrand/micropython-mdns/tree/main/examples) folder.

## Reference

A basic API reference for the public API is inside of the [REFERENCE.md](https://github.com/cbrand/micropython-mdns/blob/main/REFERENCE.md).

## Caveats

- Depending on your MicroPython implementation, you must disable MDNS in the firmware.
  - For ESP32 use the Dockerfile for the specific Micropython version in the root directory.
  - For RPI Pico Micropython beginning with version 1.32 is supported since version 1.5.0 where you can see how to do it in the Dockerfile in the root directory.
- Currently no support for IPv6 is implemented.
- Depending how chatty the network is, service responders and discovery might require a lot of memory. If the memory is filled by the buffer of the underlying socket, [the socket is closed and reopened](https://github.com/cbrand/micropython-mdns/blob/d3dd54f809629ca41c525f5dec86963a6d75e903/src/mdns_client/client.py#L100) which looses data. It, however, seems to work fine enough in tests on an ESP32 without external memory. Depending on the project size, a module with external RAM might be advisable.

## License

The library is published under the [MIT](https://github.com/cbrand/micropython-mdns/blob/main/LICENSE) license.
