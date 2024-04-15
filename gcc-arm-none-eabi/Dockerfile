FROM ubuntu:22.04

RUN mkdir /workdir && \
    apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        make xz-utils wget git python3 python3-pip

RUN  wget -O archive.tar.xz "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi.tar.xz" && \
    tar xf archive.tar.xz -C /opt && \
    rm archive.tar.xz

ENV PATH=/opt/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi/bin:$PATH

WORKDIR /workdir
