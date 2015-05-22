@echo off

title TTS Remote DB Launcher
rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttsUsername="Username: "
set /P ttsPassword="Password: "
echo Using Steve's dev server.
set TTS_GAMESERVER=192.99.167.192

echo ===============================
echo Starting Toontown Stride...
echo ppython: %PPYTHON_PATH%
echo Username: %ttsUsername%
echo Gameserver: %TTS_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
pause
