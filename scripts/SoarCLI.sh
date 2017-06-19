#!/usr/bin/env bash

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"
pushd $THISDIR > /dev/null
soar $1 $2 $3 $4 $5
popd > /dev/null
