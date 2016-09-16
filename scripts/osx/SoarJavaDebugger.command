#!/bin/bash
export SOAR_HOME="$(dirname "$0")/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"
cd $(dirname "$0")
java -XstartOnFirstThread -Djava.library.path="$SOAR_HOME" -jar "$SOAR_HOME/SoarJavaDebugger.jar" &

