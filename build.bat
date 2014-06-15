@echo off
setlocal EnableDelayedExpansion

set PYTHON_HOME=C:\Python27
set JAVA_HOME=C:\Program Files\Java\jdk1.7.0_45
set SWIG_HOME=C:\swigwin-2.0.11

echo PYTHON_HOME=%PYTHON_HOME%
echo JAVA_HOME=%JAVA_HOME%
echo SWIG_HOME=%SWIG_HOME%

if not exist %PYTHON_HOME%\python.exe (
	echo cannot locate python executable
	exit /B
)


set PATH=%PYTHON_HOME%;%JAVA_HOME%\bin;%SWIG_HOME%;%PATH%
%PYTHON_HOME%\python.exe scons\scons.py -Q %*  -u --jobs=1 --warn=cache-write-error --warn=future-deprecated --warn=reserved-variable --build=build_win --out=Z:\mazzin\git\Soar\Release\Shuffler_Input\windows64\out --opt
cd "Z:\mazzin\git\Soar\Domains\Eaters_TankSoar"
call ant
cd "Z:\mazzin\git\Soar\AgentDevelopmentTools\VisualSoar"
call ant
move "Z:\mazzin\git\Soar\Domains\Eaters_TankSoar\Eaters_TankSoar.jar" "Z:\mazzin\git\Soar\Release\Shuffler_Input\jars\"
move "Z:\mazzin\git\Soar\AgentDevelopmentTools\VisualSoar\VisualSoar.jar" "Z:\mazzin\git\Soar\Release\Shuffler_Input\jars\"
exit /B
