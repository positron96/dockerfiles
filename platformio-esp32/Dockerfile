FROM registry.gitlab.com/positron96/dockerfiles/platformio:2021-09-21-f860debe

RUN pio platform install \
      --with-package framework-espidf \
      --with-package framework-arduino \
      espressif32 \
    && pio system prune