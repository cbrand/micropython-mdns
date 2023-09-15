.DEFAULT_GOAL := build-compile

build-compile: build compile

erase:
	python3 ./venv/bin/esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash


flash:
	python3 ./venv/bin/esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware.bin

copy-main:
	./venv/bin/ampy -p /dev/ttyUSB0 put main.py /main.py

copy: copy-main

compile-micropython-1-13:
	docker build -t esp32-mdns-client:micropython.1.13 -f Dockerfile.micropython.1.13 .
	docker run --rm -v "$$(pwd):/opt/copy" -t esp32-mdns-client:micropython.1.13 cp build-MDNS/firmware.bin /opt/copy/firmware.mp.1.13.bin

compile-micropython-1-15:
	docker build -t esp32-mdns-client:micropython.1.15 -f Dockerfile.micropython.1.15 .
	docker run --rm -v "$$(pwd):/opt/copy" -t esp32-mdns-client:micropython.1.15 cp build-MDNS/firmware.bin /opt/copy/firmware.mp.1.15.bin

compile-micropython-1-16:
	docker build -t esp32-mdns-client:micropython.1.16 -f Dockerfile.micropython.1.16 .
	docker run --rm -v "$$(pwd):/opt/copy" -t esp32-mdns-client:micropython.1.16 cp build-MDNS/firmware.bin /opt/copy/firmware.mp.1.16.bin

compile-micropython-1-17:
	docker build -t esp32-mdns-client:micropython.1.17 -f Dockerfile.micropython.1.17 .
	docker run --rm -v "$$(pwd):/opt/copy" -t esp32-mdns-client:micropython.1.17 cp build-MDNS/firmware.bin /opt/copy/firmware.mp.1.17.bin

compile-micropython-1-18:
	docker build -t esp32-mdns-client:micropython.1.18 -f Dockerfile.micropython.1.18 .
	docker run --rm -v "$$(pwd):/opt/copy" -t esp32-mdns-client:micropython.1.18 cp build-MDNS/firmware.bin /opt/copy/firmware.mp.1.18.bin

compile-micropython-1-19:
	docker build -t esp32-mdns-client:micropython.1.19 -f Dockerfile.micropython.1.19 .
	docker run --rm -v "$$(pwd):/opt/copy" -t esp32-mdns-client:micropython.1.19 cp build-MDNS/firmware.bin /opt/copy/firmware.mp.1.19.bin

compile-micropython-1-20:
	docker build -t esp32-mdns-client:micropython.1.20 -f Dockerfile.micropython.1.20 .
	docker run --rm -v "$$(pwd):/opt/copy" -t esp32-mdns-client:micropython.1.20 cp build-MDNS/firmware.bin /opt/copy/firmware.mp.1.20.bin

compile-newest: compile-micropython-1-20
	docker run --rm -v "$$(pwd):/opt/copy" -t esp32-mdns-client:micropython.1.20 cp build-MDNS/firmware.bin /opt/copy/firmware.bin

compile: compile-micropython-1-13 compile-micropython-1-15 compile-micropython-1-16 compile-micropython-1-17 compile-micropython-1-18 compile-micropython-1-19 compile-micropython-1-20

install: erase compile flash copy-certs copy-main


micropython-build-shell: compile-micropython-1-20
	docker run --rm -t esp32-mdns-client:micropython.1.20 bash


compile-and-flash: compile-newest flash

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
	docker run --rm -t -u $$(id -u) -v $(CURDIR):/data asciinema/asciicast2gif -w 116 -h 20 images/service-discovery.rec images/service-discovery.gif
