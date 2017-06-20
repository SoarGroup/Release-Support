#!/usr/bin/env bash

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"

unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
    cp $SOAR_HOME/java/swt-linux64.jar $SOAR_HOME/java/swt.jar
elif [[ "$unamestr" == 'Darwin' ]]; then
    cp $SOAR_HOME/java/swt-mac64.jar $SOAR_HOME/java/swt.jar
else
    echo 'Unsupported OS'
    exit 1
fi

pushd $SOAR_HOME > /dev/null
java -Djava.library.path="$SOAR_HOME" -jar "$SOAR_HOME/VisualSoar.jar" &
popd > /dev/null
