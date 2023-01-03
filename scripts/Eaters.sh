#!/usr/bin/env bash

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
FLAG=""
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"

unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
  if [ ! -e "$SOAR_HOME/pkgIndex.tcl" ]; then
    echo 'First time initialization of Soar for Linux...'
    mv "$SOAR_HOME/linux_x86-64/swt.jar" "$SOAR_HOME/java/"
    mv "$SOAR_HOME/linux_x86-64"/* "$SOAR_HOME/"
    rm -rf "$SOAR_HOME/mac_x86-64"
    rm -rf "$SOAR_HOME/mac_ARM64"
    rm -rf "$SOAR_HOME/win_x86-64"
    rm -rf "$SOAR_HOME/linux_x86-64"
    rm -f "$THISDIR"/*.bat
    rm -f "$THISDIR/macOS_setup.command"
  fi
elif [[ "$unamestr" == 'Darwin' ]]; then
  if [ ! -e "$SOAR_HOME/pkgIndex.tcl" ]; then
    if [ "$(uname -m)" == "arm64" ]; then
      echo 'First time initialization of Soar for Mac OSX ARM64...'
      mv "$SOAR_HOME/mac_ARM64/swt.jar" "$SOAR_HOME/java/"
      mv "$SOAR_HOME/mac_ARM64"/* "$SOAR_HOME/"
      "$THISDIR/macOS_setup.command" "$SOAR_HOME"
      rm -rf "$SOAR_HOME/mac_x86-64"
      rm -rf "$SOAR_HOME/linux_x86-64"
      rm -rf "$SOAR_HOME/win_x86-64"
      rm -rf "$SOAR_HOME/mac_ARM64"
      rm -f "$THISDIR"/*.bat
    else
      echo 'First time initialization of Soar for Mac OSX x86-64...'
      mv "$SOAR_HOME/mac_x86-64/swt.jar" "$SOAR_HOME/java/"
      mv "$SOAR_HOME/mac_x86-64"/* "$SOAR_HOME/"
      "$THISDIR/macOS_setup.command" $SOAR_HOME
      rm -rf "$SOAR_HOME/mac_x86-64"
      rm -rf "$SOAR_HOME/mac_ARM64"
      rm -rf "$SOAR_HOME/linux_x86-64"
      rm -rf "$SOAR_HOME/win_x86-64"
      rm -f "$THISDIR"/*.bat
    fi
  fi
  FLAG="-XstartOnFirstThread"
else
  if [ ! -e "$SOAR_HOME/pkgIndex.tcl" ]; then
    echo 'First time initialization of Soar for an unsupported OS.  Assuming Linux.'
    mv "$SOAR_HOME/linux_x86-64/swt.jar" "$SOAR_HOME/java/"
    mv "$SOAR_HOME/linux_x86-64"/* "$SOAR_HOME/"
    rm -rf "$SOAR_HOME/mac_x86-64"
    rm -rf "$SOAR_HOME/mac_ARM64"
    rm -rf "$SOAR_HOME/win_x86-64"
    rm -rf "$SOAR_HOME/linux_x86-64"
    rm -f "$THISDIR"/*.bat
    rm -f "$THISDIR/macOS_setup.command"
  fi
fi

pushd "$THISDIR" > /dev/null
java $FLAG -Djava.library.path="$SOAR_HOME" -jar "$SOAR_HOME/Eaters_TankSoar.jar" bin/games/eaters.cnf
popd > /dev/null
