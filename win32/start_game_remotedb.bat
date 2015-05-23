@echo off
cd..

title Toontown Stride RemoteDB Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttsUsername="Username: "
set /P ttsPassword="Password: "
set TTS_GAMESERVER=167.114.220.172

echo ===============================
echo Starting Toontown Stride...
echo ppython: %PPYTHON_PATH%
echo Username: %ttsUsername%
echo Gameserver: %TTS_GAMESERVER% (Steve's Dev Server)
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
pause
