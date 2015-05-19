@echo off
title GUI Editor
set /P PPYTHON_PATH=<PPYTHON_PATH

:main
%PPYTHON_PATH% -m guieditor.EditorStart
goto main