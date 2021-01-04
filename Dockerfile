FROM python:3.8

RUN apt-get update && \
    apt-get install -y git cmake wget make libncurses-dev flex bison gperf python python-serial

WORKDIR /opt/app

RUN wget https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz && \
    tar -xzvf ./xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz

ENV PATH=${PATH}:/opt/app/xtensa-esp32-elf/bin/

RUN git clone https://github.com/micropython/micropython && \
    git clone https://github.com/espressif/esp-idf.git && \
    cd esp-idf && \
    git checkout 4c81978a3e2220674a432a588292a4c860eef27b && \
    git submodule update --init && \
    cd /opt/app/micropython && \
    git submodule update --init && \
    pip install -U pip && \
    pip install pyparsing==2.3.1 && \
    pip install esptool==3.0 && \
    pip install pyserial==3.5 && \
    pip install --user -r /opt/app/esp-idf/requirements.txt

ENV ESPIDF "/opt/app/esp-idf"
ENV BOARD "MDNS"

ADD config/boards/ /opt/app/micropython/ports/esp32/boards/

WORKDIR /opt/app/micropython

RUN make -C mpy-cross && \
    git submodule init lib/berkeley-db-1.xx && \
    git submodule update

WORKDIR /opt/app/micropython/ports/esp32

RUN make

WORKDIR /opt/app/

WORKDIR /opt/app/micropython/ports/esp32

RUN make
