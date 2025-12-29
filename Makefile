.DEFAULT_GOAL := build-compile

build-compile: build compile
TTY_PORT?=/dev/ttyUSB0
PWD?=$(shell pwd)
DNS_VOLUME_NAME?=mdns-build-volume
NEWEST_MICROPYTHON_VERSION?=1.27

erase:
	esptool.py --chip esp32 --port ${TTY_PORT} erase_flash

flash:
	esptool.py --chip esp32 --port ${TTY_PORT} write_flash -z 0x1000 firmware.bin

copy-main:
	ampy -p ${TTY_PORT} put main.py /main.py

copy: copy-main

create-data-volume:
	docker volume create ${DNS_VOLUME_NAME} || true

compile-micropython-1-24: compile-micropython-esp32-1-24 compile-micropython-rp2-1-24

compile-micropython-esp32-1-24:
	MICROPYTHON_VERSION=1.24 MICROPYTHON_PORT=esp32 ./build-and-copy-firmware.sh

compile-micropython-rp2-1-24:
	MICROPYTHON_VERSION=1.24 MICROPYTHON_PORT=rp2 ./build-and-copy-firmware.sh

compile-micropython-1-25: compile-micropython-esp32-1-25 compile-micropython-rp2-1-25

compile-micropython-esp32-1-25:
	MICROPYTHON_VERSION=1.25 MICROPYTHON_PORT=esp32 ./build-and-copy-firmware.sh

compile-micropython-rp2-1-25:
	MICROPYTHON_VERSION=1.25 MICROPYTHON_PORT=rp2 ./build-and-copy-firmware.sh

compile-micropython-1-26: compile-micropython-esp32-1-26 compile-micropython-rp2-1-26

compile-micropython-esp32-1-26:
	MICROPYTHON_VERSION=1.26 MICROPYTHON_PORT=esp32 ./build-and-copy-firmware.sh

compile-micropython-rp2-1-26:
	MICROPYTHON_VERSION=1.26 MICROPYTHON_PORT=rp2 ./build-and-copy-firmware.sh

compile-micropython-1-27: compile-micropython-esp32-1-27 compile-micropython-rp2-1-27

compile-micropython-esp32-1-27:
	MICROPYTHON_VERSION=1.27 MICROPYTHON_PORT=esp32 ./build-and-copy-firmware.sh

compile-micropython-rp2-1-27:
	MICROPYTHON_VERSION=1.27 MICROPYTHON_PORT=rp2 ./build-and-copy-firmware.sh

compile-newest: compile-micropython-esp32-1-27
	docker cp helper:/data/firmware.mp.${NEWEST_MICROPYTHON_VERSION}.esp32.bin ./firmware.bin
	docker rm helper

compile: compile-micropython-1-24 compile-micropython-1-25 compile-micropython-1-26 compile-micropython-1-27

install: erase compile-newest flash copy-main


micropython-build-shell: compile-micropython-1-26
	docker run --rm -t esp32-mdns-client:micropython.1.26.esp32 bash


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
