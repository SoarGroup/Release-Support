@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%

cmd /c "%~dp0setup.bat"

start javaw -Djava.library.path="%SOAR_HOME%" -jar bin\SoarJavaDebugger.jar %1 %2 %3 %4 %5
