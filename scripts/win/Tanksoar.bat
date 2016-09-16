@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%
start javaw -Djava.library.path=%SOAR_HOME% -jar bin\Eaters_TankSoar.jar config\tanksoar.cnf