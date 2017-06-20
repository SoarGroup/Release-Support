@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%
start bin\soar.exe %1 %2 %3 %4 %5 
