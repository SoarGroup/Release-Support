#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
FLAG=""
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"

"$THISDIR/setup.sh"

# SWT requirement: display must be created on main thread due to Cocoa restrictions
if [[ $(uname) == 'Darwin' ]]; then
  FLAG="-XstartOnFirstThread"
fi

pushd "$THISDIR" > /dev/null || { echo "Failed to cd to $THISDIR"; exit 1; }
java $FLAG -Djava.library.path="$SOAR_HOME" -jar "$SOAR_HOME/SoarJavaDebugger.jar" "$@" &
popd > /dev/null || { echo "popd failed"; exit 1; }
