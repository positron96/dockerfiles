# Eclipse MCU with ARM toolchain 

Eclipse IDE with MCU plugins and ARM toolchain,
for headless builds in CI/CD environments.

The image uses latest versions of Eclipse and ARM toolchain from their respective
releases page from Github. See:

 * https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases/
 * https://github.com/gnu-mcu-eclipse/org.eclipse.epp.packages/releases/

## Usage:

``docker run -it -v ... eclipse-mcu-arm project Debug``


Can also be used with, e.g. Gitlab CI/CD, with following job in .gitlab-ci.yml:
```

```
