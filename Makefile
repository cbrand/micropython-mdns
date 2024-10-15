.DEFAULT_GOAL := build-compile

build-compile: build compile
TTY_PORT?=/dev/ttyUSB0
PWD?=$(shell pwd)
DNS_VOLUME_NAME?=mdns-build-volume
NEWEST_MICROPYTHON_VERSION?=1.23

erase:
	esptool.py --chip esp32 --port ${TTY_PORT} erase_flash

flash:
	esptool.py --chip esp32 --port ${TTY_PORT} write_flash -z 0x1000 firmware.bin

copy-main:
	ampy -p ${TTY_PORT} put main.py /main.py

copy: copy-main

create-data-volume:
	docker volume create ${DNS_VOLUME_NAME}

compile-micropython-1-15: create-data-volume
	MICROPYTHON_VERSION=1.15 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh

compile-micropython-1-16: create-data-volume
	MICROPYTHON_VERSION=1.16 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh
	

compile-micropython-1-17: create-data-volume
	MICROPYTHON_VERSION=1.17 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh

compile-micropython-1-18: create-data-volume
	MICROPYTHON_VERSION=1.18 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh

compile-micropython-1-19: create-data-volume
	MICROPYTHON_VERSION=1.19 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh

compile-micropython-1-20: create-data-volume
	MICROPYTHON_VERSION=1.20 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh

compile-micropython-1-21: create-data-volume
	MICROPYTHON_VERSION=1.21 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh

compile-micropython-1-22: create-data-volume
	MICROPYTHON_VERSION=1.22 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh

compile-micropython-1-23: create-data-volume
	MICROPYTHON_VERSION=1.23 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} ./build-and-copy-firmware.sh
	MICROPYTHON_VERSION=1.23 DNS_VOLUME_NAME=${DNS_VOLUME_NAME} MICROPYTHON_PORT=rp2 MICROPYTHON_EXTENSION=uf2 BOARD=RPI_PICO_W ./build-and-copy-firmware.sh

compile-newest: compile-micropython-1-23
	docker run --rm -v "${DNS_VOLUME_NAME}:/opt/copy" -t esp32-mdns-client:micropython.${NEWEST_MICROPYTHON_VERSION} cp build-MDNS/firmware.bin /opt/copy/firmware.esp32.bin
	docker create -v ${DNS_VOLUME_NAME}:/data --name helper busybox true
	docker cp helper:/data/firmware.bin ./firmware.bin
	docker rm helper

compile: compile-micropython-1-15 compile-micropython-1-16 compile-micropython-1-17 compile-micropython-1-18 compile-micropython-1-19 compile-micropython-1-20 compile-micropython-1-21 compile-micropython-1-22 compile-micropython-1-23

install: erase compile flash copy-certs copy-main


micropython-build-shell: compile-micropython-1-23
	docker run --rm -t esp32-mdns-client:micropython.1.23.esp32 bash


compile-and-flash: compile-newest flash

compile-and-shell: compile-and-flash shell

shell:
	picocom ${TTY_PORT} -b115200

build-and-upload: build upload

mip-json:
	python generate-package-json.py

build: mip-json
	rm -rf src/dist/*.tar.gz*
	cd src && python setup.py sdist

upload:
	twine upload src/dist/*.tar.gz

generatecligif:
	docker run --rm -t -u $$(id -u) -v $(CURDIR):/data asciinema/asciicast2gif -w 116 -h 20 images/service-discovery.rec images/service-discovery.gif
