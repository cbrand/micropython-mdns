.DEFAULT_GOAL := build-compile

build-compile: build compile

erase:
	python3 ./venv/bin/esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash


flash:
	python3 ./venv/bin/esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 firmware.bin

copy-main:
	./venv/bin/ampy -p /dev/ttyUSB0 put main.py /main.py

copy: copy-main

compile:
	docker build -t esp32-mdns-client .
	docker run --rm -i -v "$$(pwd):/opt/copy" -t esp32-mdns-client cp build-MDNS/firmware.bin /opt/copy/firmware.bin

install: erase compile flash copy-certs copy-main


micropython-build-shell: compile
	docker run --rm -i -t esp32-mdns-client bash


compile-and-flash: compile flash

compile-and-shell: compile-and-flash shell

shell:
	picocom /dev/ttyUSB0 -b115200

build-and-upload: build upload

build:
	rm -rf src/dist/*.tar.gz*
	cd src && python setup.py sdist

upload:
	twine upload src/dist/*.tar.gz

generatecligif:
	docker run --rm -i -t -u $$(id -u) -v $(CURDIR):/data asciinema/asciicast2gif -w 116 -h 20 images/service-discovery.rec images/service-discovery.gif
