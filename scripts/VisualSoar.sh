#!/usr/bin/env bash

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
FLAG=""
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"

unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
    cp $SOAR_HOME/java/swt-linux64.jar $SOAR_HOME/java/swt.jar
elif [[ "$unamestr" == 'Darwin' ]]; then
    cp $SOAR_HOME/java/swt-mac64.jar $SOAR_HOME/java/swt.jar
    FLAG="-XstartOnFirstThread"
else
    echo 'Unsupported OS'
    exit 1
fi

pushd $THISDIR > /dev/null
java $FLAG -Djava.library.path="$SOAR_HOME" -jar "$SOAR_HOME/VisualSoar.jar" $1 $2 $3 $4 $5 &
popd > /dev/null
