@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%
copy %SOAR_HOME%\java\swt-win64.jar %SOAR_HOME%\java\swt.jar
copy %SOAR_HOME%\tcl\pkgIndex-win64.tcl %SOAR_HOME%\pkgIndex.tcl
start javaw -Djava.library.path=%SOAR_HOME% -jar bin\SoarJavaDebugger.jar %1 %2 %3 %4 %5 
