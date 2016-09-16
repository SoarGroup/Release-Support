#!/bin/bash
export SOAR_HOME="$(pwd)/bin"
export LD_LIBRARY_PATH="$SOAR_HOME"
java -Djava.library.path="$SOAR_HOME" -jar "$SOAR_HOME/SoarJavaDebugger.jar"
