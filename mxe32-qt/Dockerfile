FROM ubuntu:xenial

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
       curl gnupg2 openssl apt-transport-https ca-certificates

RUN echo mxe \
    && curl -sSL "https://pkg.mxe.cc/repos/apt/client-conf/mxeapt.gpg" | apt-key add - \
    && echo "deb https://pkg.mxe.cc/repos/apt xenial main" >> /etc/apt/sources.list \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends \
       make \
       mxe-i686-w64-mingw32.static-cc \
       mxe-i686-w64-mingw32.static-qtbase \
       mxe-i686-w64-mingw32.static-qtserialport \
       mxe-i686-w64-mingw32.static-qttools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add a qmake alias
RUN ln -s /usr/lib/mxe/usr/i686-w64-mingw32.static/qt5/bin/qmake  /usr/lib/mxe/usr/bin/qmake

# Enhance path
ENV PATH /usr/lib/mxe/usr/bin:$PATH

ENTRYPOINT [ "/bin/sh", "-c" ]

CMD ["qmake && make"]

##########################################################################
# Here the project specific workflow starts.

WORKDIR /src

