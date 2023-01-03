@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%

if not exist "%SOAR_HOME%\pkgIndex.tcl" (
    echo "First time initialization of Soar for Windows..."
    move "%SOAR_HOME%\win_x86-64\swt.jar" "%SOAR_HOME%\java\swt.jar"
    move "%SOAR_HOME%\win_x86-64\*.*" "%SOAR_HOME%\"
    rmdir /S /Q "%SOAR_HOME%\mac_x86-64"
    rmdir /S /Q "%SOAR_HOME%\mac_ARM64"
    rmdir /S /Q "%SOAR_HOME%\linux_x86-64"
    rmdir /S /Q "%SOAR_HOME%\win_x86-64"
    del /F /Q "%~dp0*.sh"
)

start javaw -Djava.library.path="%SOAR_HOME%" -jar bin\Eaters_TankSoar.jar bin\games\eaters.cnf

