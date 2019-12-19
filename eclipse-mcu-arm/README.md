# Eclipse MCU with ARM toolchain 

Eclipse IDE with MCU plugins and ARM toolchain,
for headless builds in CI/CD environments.

The image uses latest versions of Eclipse and ARM toolchain from their respective
releases page from Github. See:

 * https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases/
 * https://github.com/gnu-mcu-eclipse/org.eclipse.epp.packages/releases/

## Usage:

``docker run -it -v dir:/workspace eclipse-mcu-arm project Debug``

Where:
 * ``dir`` is directory on hst that contains folder with project
 * ``project`` project folder
 * `Debug` name of target.

This command will create a new Eclipse workspace in directory `dir`.


Can also be used with, e.g. Gitlab CI/CD, with following job in .gitlab-ci.yml:
```

```
