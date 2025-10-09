#!/bin/sh

export MICROPYTHON_VERSION="${MICROPYTHON_VERSION:-1.24}"
export MICROPYTHON_PORT="${MICROPYTHON_PORT:-esp32}"

docker build -t esp32-mdns-client:micropython.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT} -f Dockerfile.micropython.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT} .
docker run --rm -v "$(pwd):/tmp/mdns-build" -i -t esp32-mdns-client:micropython.${MICROPYTHON_VERSION}.${MICROPYTHON_PORT}
