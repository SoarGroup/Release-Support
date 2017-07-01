#!/usr/bin/env bash

THISDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export SOAR_HOME="$THISDIR/bin"
export DYLD_LIBRARY_PATH="$SOAR_HOME"

if [ ! -e $SOAR_HOME/pkgIndex.tcl ]; then
  unamestr=`uname`
  if [[ "$unamestr" == 'Linux' ]]; then
      echo 'First time initialization of Soar for Linux...'
      mv $SOAR_HOME/linux64/swt.jar $SOAR_HOME/java/
      mv $SOAR_HOME/linux64/* $SOAR_HOME/
      rm -rf $SOAR_HOME/mac64
      rm -rf $SOAR_HOME/windows64
      rm -rf $SOAR_HOME/linux64
  elif [[ "$unamestr" == 'Darwin' ]]; then
      echo 'First time initialization of Soar for Mac OSX...'
      mv $SOAR_HOME/mac64/swt.jar $SOAR_HOME/java/
      mv $SOAR_HOME/mac64/* $SOAR_HOME/
      rm -rf $SOAR_HOME/mac64
      rm -rf $SOAR_HOME/linux64
      rm -rf $SOAR_HOME/win64
  else
      echo 'First time initialization of Soar for an unsupported OS.  Assuming Linux.'
      mv $SOAR_HOME/linux64/swt.jar $SOAR_HOME/java/
      mv $SOAR_HOME/linux64/* $SOAR_HOME/
      rm -rf $SOAR_HOME/mac64
      rm -rf $SOAR_HOME/win64
      rm -rf $SOAR_HOME/linux64
  fi
  rm -f $THISDIR/*.bat
fi

pushd $SOAR_HOME > /dev/null
./soar $1 $2 $3 $4 $5
popd > /dev/null
