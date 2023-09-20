#!/bin/sh

docker build -t esp32-mdns-client:micropython.${MICROPYTHON_VERSION} -f Dockerfile.micropython.${MICROPYTHON_VERSION} .
docker run --rm -v "${DNS_VOLUME_NAME}:/opt/copy" -t esp32-mdns-client:micropython.${MICROPYTHON_VERSION} cp build-MDNS/firmware.bin /opt/copy/firmware.mp.${MICROPYTHON_VERSION}.bin
docker create -v ${DNS_VOLUME_NAME}:/data --name helper busybox true
docker cp helper:/data/firmware.mp.${MICROPYTHON_VERSION}.bin ./firmware.mp.${MICROPYTHON_VERSION}.bin
docker rm helper
