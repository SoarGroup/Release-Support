@echo off
set SOAR_HOME=%~dp0bin
set PATH=%SOAR_HOME%;%PATH%

if not exist  %SOAR_HOME%\pkgIndex.tcl (
    echo "First time initialization of Soar for Windows..."
    move %SOAR_HOME%\win64\swt.jar %SOAR_HOME%\java\swt.jar
    move %SOAR_HOME%\win64\*.* %SOAR_HOME%\
    rmdir /S /Q %SOAR_HOME%\mac64
    rmdir /S /Q %SOAR_HOME%\linux64
    rmdir /S /Q %SOAR_HOME%\win64
    del /F /Q %~dp0SoarCLI.sh
    del /F /Q %~dp0SoarJavaDebugger.sh
    del /F /Q %~dp0VisualSoar.sh
    del /F /Q %~dp0Eaters.sh
    del /F /Q %~dp0TankSoar.sh
)

start javaw -Djava.library.path=%SOAR_HOME% -jar bin\SoarJavaDebugger.jar %1 %2 %3 %4 %5 
