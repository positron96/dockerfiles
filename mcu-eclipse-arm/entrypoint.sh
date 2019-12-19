#!/bin/sh
PROJ=$1
TARGET=$2
eclipse --launcher.suppressErrors -nosplash -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data /workspace -import /workspace/$PROJ -cleanBuild $PROJ/$TARGET