@echo off

cd ../../../

title GUI Editor
set GUI=

:main

set /P GUI="File: %gui%"
"dependencies/panda/python/ppython.exe" "dev/tools/gui/EditorStart.py" %GUI%

echo.
echo.

goto main