FROM ubuntu:xenial
MAINTAINER positron96

ENV DEBIAN_FRONTEND noninteractive

# Install updates & requirements:
RUN apt-get -qq update && apt-get -qq dist-upgrade && apt-get install -qq -y --no-install-recommends \
    git \
    openssh-client \
    ca-certificates \
    && apt-get -qq clean

RUN apt-get install -qq -y openjdk-8-jdk netbeans=8.1+dfsg2-3 --no-install-recommends \
    && apt-get -qq clean

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

WORKDIR /work

COPY build.properties /
