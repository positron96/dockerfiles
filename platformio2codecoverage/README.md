# Converter of PlatformIO static analyzer reports into CodeClimate's JSON

Despite the name, it has nothing to do with code coverage.

Suitable for Gitlab CI/CD.
You can use this image to convert `pio check --json` results into CodeClimate JSON results.

No CodeClimate is required.

The project is based on https://gitlab.com/ahogen/cppcheck-codequality cppcheck XML to CodeClimate JSON converter


## Example GitLab CI/CD file

```

.analyze_rules: &analyze_rules
  rules:
    - if: '$CODE_QUALITY_DISABLED'
      when: never
    - if: '$CI_PIPELINE_SOURCE == "web"' 
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"' # Run code quality job in merge request pipelines
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'      # Run code quality job in pipelines on the master branch (but not in other branch pipelines)
    - if: '$CI_COMMIT_TAG'

piocheck:
  stage: build
  image:
    name: registry.gitlab.com/positron96/dockerfiles/platformio:2021-08-30-8af189f0
    entrypoint: [""]

  <<: *analyze_rules  

  script:
    - pio check > pio.txt
    - pio check --json-output > pio.json
    - echo $CI_PROJECT_DIR > basedir.txt
  artifacts:
    # pio.txt can be removed altogether
    paths: ["pio.json", "pio.txt", "basedir.txt"]

code_quality:
  stage: test
  image: 
    name: registry.gitlab.com/positron96/dockerfiles/platformio2codecoverage:2021-08-30-571a9b3c
    entrypoint: [""]

  <<: *analyse_rules  

  dependencies: [piocheck]

  script:
    - export BASEDIR=$(cat basedir.txt)
    - piocheck-codecoverage.py -i pio.json -o codecoverage.json -s $BASEDIR

  artifacts:
    reports:
      codequality: codecoverage.json
    paths: [codecoverage.json]

```

* You need to run `pio check` twice as on the first run it will download the tool and will dump info about it on stdout, spoiling the resulting JSON.
The bug is reported here: https://github.com/platformio/platformio-core/issues/4029
