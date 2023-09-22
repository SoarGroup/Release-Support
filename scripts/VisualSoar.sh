#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"

"$THISDIR/setup.sh"

pushd "$SOAR_HOME" > /dev/null || { echo "Failed to cd to $THISDIR"; exit 1; }
java -Djava.library.path="$SOAR_HOME" -jar "$SOAR_HOME/VisualSoar.jar" &
popd > /dev/null || { echo "popd failed"; exit 1; }
