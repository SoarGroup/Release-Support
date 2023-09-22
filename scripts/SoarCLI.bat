@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%

cmd /c "%~dp0setup.bat"

start bin\soar.exe %1 %2 %3 %4 %5
