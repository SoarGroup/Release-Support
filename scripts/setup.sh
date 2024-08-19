#!/usr/bin/env bash

# Set up Soar to work with this platform, if not done already

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export SOAR_HOME="$THISDIR/bin"

echo_yellow () {
  echo -e "\e[93m$1\e[0m"
}

linux64_setup () {
  echo_yellow 'First time initialization of Soar for Linux...'
  mv "$SOAR_HOME/linux_x86-64/swt.jar" "$SOAR_HOME/java/"
  mv "$SOAR_HOME/linux_x86-64"/* "$SOAR_HOME/"
  rm -f "$THISDIR/macOS_setup.command"
}

macOS_quarantine_fix () {
  echo "macOS setup: removing quarantine attributes from Soar binaries..."
  for file in "soar" "libSoar.dylib" "libTcl_sml_ClientInterface.dylib" "libtclsoarlib.dylib" "_Python_sml_ClientInterface.so" "libCSharp_sml_ClientInterface.dylib" "sml_csharp.dll" "libJava_sml_ClientInterface.jnilib"; do
    echo "  Removing quarantine attributes from $file..."
    if [ ! -f "$THISDIR/bin/$file" ]; then
      echo "Error: could not unquarantine '$THISDIR/bin/$file' because it does not exist."
      exit 1
    fi
    xattr -d com.apple.quarantine "$THISDIR/bin/$file" >/dev/null 2>&1 || { echo "   File already unquarantined"; true; }
  done
}

if [ ! -e "$SOAR_HOME/pkgIndex.tcl" ]; then
  unamestr=$(uname)
  if [[ "$unamestr" == 'Linux' ]]; then
      linux64_setup
  elif [[ "$unamestr" == 'Darwin' ]]; then
    if [ "$(uname -m)" == "arm64" ]; then
      echo_yellow 'First time initialization of Soar for Mac OSX ARM64...'
      mv "$SOAR_HOME/mac_ARM64/swt.jar" "$SOAR_HOME/java/"
      mv "$SOAR_HOME/mac_ARM64"/* "$SOAR_HOME/"
    else
      echo_yellow 'First time initialization of Soar for Mac OSX x86-64...'
      mv "$SOAR_HOME/mac_x86-64/swt.jar" "$SOAR_HOME/java/"
      mv "$SOAR_HOME/mac_x86-64"/* "$SOAR_HOME/"
    fi
      macOS_quarantine_fix
  else
      echo_yellow 'First time initialization of Soar for an unsupported OS. Assuming Linux.'
      linux64_setup
  fi
  rm -rf "$SOAR_HOME/mac_x86-64"
  rm -rf "$SOAR_HOME/mac_ARM64"
  rm -rf "$SOAR_HOME/win_x86-64"
  rm -rf "$SOAR_HOME/linux_x86-64"
  rm -f "$THISDIR"/*.bat
fi
