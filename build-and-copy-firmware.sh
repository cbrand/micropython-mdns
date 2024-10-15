#!/bin/sh

export MICROPYTHON_VERSION="${MICROPYTHON_VERSION:-1.12}"
export DNS_VOLUME_NAME="${DNS_VOLUME_NAME:-mdns-build-volume}"
export MICROPYTHON_PORT="${MICROPYTHON_PORT:-esp32}"
export BOARD=${BOARD:-MDNS}

docker build -t esp32-mdns-client:micropython.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT} -f Dockerfile.micropython.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT} .
docker run --rm -v "${DNS_VOLUME_NAME}:/opt/copy" -t esp32-mdns-client:micropython.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT} cp build-${BOARD}/firmware.bin /opt/copy/firmware.mp.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT}.bin
docker create -v ${DNS_VOLUME_NAME}:/data --name helper busybox true
docker cp helper:/data/firmware.mp.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT}.bin ./firmware.mp.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT}.bin
docker rm helper
