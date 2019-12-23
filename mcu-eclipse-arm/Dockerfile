FROM ubuntu:bionic

MAINTAINER positron96

ENV DEBIAN_FRONTEND noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    ca-certificates \
    wget \
    openjdk-8-jre-headless \
    make \
 && rm -rf /var/lib/apt/lists/*

# Download and extract GNU MCU Eclipse
RUN wget -qO- https://api.github.com/repos/gnu-mcu-eclipse/org.eclipse.epp.packages/releases/latest | sed -n 's/.*browser_download_url.*\(https.*linux.*x86_64.*tar.gz\)"/\1/p' | wget -qi - \
 && tar -xzf *.tar.gz \
 && rm *.tar.gz \
 && mv eclipse /opt/eclipse

# Download and extract GNU ARM Toolchain from xPack
RUN mkdir /ttt && cd /ttt && \
 wget -qO- https://api.github.com/repos/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases/latest | sed -n 's/.*browser_download_url.*\(https.*linux.*x64.*tar.gz\)"/\1/p' | wget -qi - \
 && tar -xzf *.tar.gz \
 && rm *.tar.gz \
 && mv $(ls) /opt/arm-none-eabi-gcc \
 && cd / && rm -rf /ttt

# Add Eclipse & gcc to PATH
ENV PATH="${PATH}:/opt/eclipse:/opt/arm-none-eabi-gcc/bin"

WORKDIR /workspace
VOLUME /workspace

ADD eclipse-build /usr/local/bin
ADD entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]