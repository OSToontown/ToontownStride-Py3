@echo off

cd ../../../

title GUI Editor
set GUI=

:main

set /P GUI="File: %gui%"
"C:\Panda3D-1.10.0\python\ppython.exe" "dev/tools/gui/EditorStart.py" %GUI%

echo.
echo.

goto main