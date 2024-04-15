An Ubuntu image with ARM gcc compiler.

Version of GCC is [12.2.rel1](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads/12-2-rel1).
The container is specifically created for building of Blackmagic Debug probe firmware, which requires this particular version of GCC.
Also for this reason, `python3` and `pip` are included, so that  `meson` can be installed manually if needed. 

The compiler is in `/opt/` (and also in `$PATH`), workdir is `/workdir`.
