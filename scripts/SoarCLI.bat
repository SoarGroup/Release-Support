@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%
copy %SOAR_HOME%\tcl\pkgIndex-win64.tcl %SOAR_HOME%\pkgIndex.tcl
start bin\soar.exe %1 %2 %3 %4 %5 
