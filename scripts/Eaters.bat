@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%
copy %SOAR_HOME%\java\swt-win64.jar %SOAR_HOME%\java\swt.jar
start javaw -Djava.library.path=%SOAR_HOME% -jar bin\Eaters_TankSoar.jar config\eaters.cnf

