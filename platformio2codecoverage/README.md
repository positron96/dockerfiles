# Converter of PlatformIO static analyzer reports into CodeClimate's JSON

Suitable for Gitlab CI/CD.
You can use this image to convert `pio check --json` results into CodeClimate JSON results.

No CodeClimate is required.

The project is based on https://gitlab.com/ahogen/cppcheck-codequality cppcheck XML to CodeClimate JSON converter


## Example GitLab CI/CD file

```
piocheck:
  stage: build
  image:
    name: registry.gitlab.com/positron96/dockerfiles/platformio:2021-08-30-8af189f0
    entrypoint: [""]

  script:
    - pio check > pio.txt
    - pio check --json-output > pio.json
  artifacts:
    paths: ["pio.json"]

code_quality:
  stage: test
  image: 
    name: registry.gitlab.com/positron96/dockerfiles/platformio2codecoverage:2021-08-11-e0fb4477
    entrypoint: [""]

  dependencies: [piocheck]

  script:
    - piocheck-codecoverage.py -i pio.json -o codecoverage.json

  artifacts:
    reports:
      codequality: codecoverage.json
```

* You need to run `pio check` twice as on the first run it will download the tool and will dump info about it on stdout, spoiling the resulting JSON.
The bug is reported here: https://github.com/platformio/platformio-core/issues/4029