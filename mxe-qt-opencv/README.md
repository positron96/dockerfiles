# Docker image with MXE, Qt and OpenCV

A cross-compile environment for qt applications with opencv library.

Uses mxe project. https://mxe.cc/

Based on https://github.com/sba1/qt-win-docker

This folder with dockerfiles can be built into single image using `Dockerfile`,
or it can be built into 3 separate images: mxe-base (with only mxe and related stuff),
mxe-opencv (with opencv added on top of it) and mxe-qt-opencv (with added qt). 
3-image structure was used to auto-build on docker hub which restricts building time.
 
