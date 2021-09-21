FROM python:3.9.0-slim

ENV APP_VERSION="5.2.0" \
    APP="platformio-core"

LABEL app.name="${APP}" \
      app.version="${APP_VERSION}" \
      maintainer="Paul Melnikov <positron96@gmail.com>"

ENV USERDIR=/pio

RUN groupadd -r pio --gid=1001 && \
    useradd -r -g pio --uid=1001 --home $USERDIR --create-home --shell /bin/sh pio

ENV PATH=$USERDIR/.local/bin:$PATH

USER pio

RUN pip install -U platformio==${APP_VERSION} && rm -rf $USERDIR/.cache

WORKDIR /work

ENTRYPOINT ["platformio"] 

