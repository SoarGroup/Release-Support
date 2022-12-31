#!/usr/bin/env bash

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"

if [ ! -e $SOAR_HOME/pkgIndex.tcl ]; then
  unamestr=`uname`
  if [[ "$unamestr" == 'Linux' ]]; then
      echo 'First time initialization of Soar for Linux...'
      mv $SOAR_HOME/linux_x86-64/swt.jar $SOAR_HOME/java/
      mv $SOAR_HOME/linux_x86-64/* $SOAR_HOME/
  elif [[ "$unamestr" == 'Darwin' ]]; then
    if [ "$(uname -m)" == "arm64" ]; then
      echo 'First time initialization of Soar for Mac OSX ARM64...'
      mv $SOAR_HOME/mac_ARM64/swt.jar $SOAR_HOME/java/
      mv $SOAR_HOME/mac_ARM64/* $SOAR_HOME/
      ./macOS_setup.command $SOAR_HOME
    else
      echo 'First time initialization of Soar for Mac OSX x86-64...'
      mv $SOAR_HOME/mac_x86-64/swt.jar $SOAR_HOME/java/
      mv $SOAR_HOME/mac_x86-64/* $SOAR_HOME/
      ./macOS_setup.command $SOAR_HOME
    fi
  else
      echo 'First time initialization of Soar for an unsupported OS.  Assuming Linux.'
      mv $SOAR_HOME/linux_x86-64/swt.jar $SOAR_HOME/java/
      mv $SOAR_HOME/linux_x86-64/* $SOAR_HOME/
  fi
  rm -rf $SOAR_HOME/mac_x86-64
  rm -rf $SOAR_HOME/mac_ARM64
  rm -rf $SOAR_HOME/win_x86-64
  rm -rf $SOAR_HOME/linux_x86-64
  rm -f $THISDIR/*.bat
fi

pushd $SOAR_HOME > /dev/null
java -Djava.library.path="$SOAR_HOME" -jar "$SOAR_HOME/VisualSoar.jar" &
popd > /dev/null
