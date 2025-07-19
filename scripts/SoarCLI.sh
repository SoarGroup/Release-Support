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

"$SOAR_HOME/soar" "$@"
