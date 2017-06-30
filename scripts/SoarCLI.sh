#!/usr/bin/env bash

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"

unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
    cp $SOAR_HOME/tcl/pkgIndex-linux64.tcl $SOAR_HOME/pkgIndex.tcl
elif [[ "$unamestr" == 'Darwin' ]]; then
    cp $SOAR_HOME/tcl/pkgIndex-mac64.tcl $SOAR_HOME/pkgIndex.tcl
else
    echo 'Unsupported OS'
    cp $SOAR_HOME/tcl/pkgIndex-linux64.tcl $SOAR_HOME/pkgIndex.tcl
fi

pushd $THISDIR > /dev/null
soar $1 $2 $3 $4 $5
popd > /dev/null
