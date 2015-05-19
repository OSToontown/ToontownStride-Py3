@echo off

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttsUsername="Username: "
set /P ttsPassword="Password: "
echo Choose your game server!
echo #1 - Localhost
echo #2 - Loudrob
echo #3 - Developer Server (Steve)
echo #4 - Custom
echo.
set /P INPUT=

if %INPUT%==1 set TTS_GAMESERVER=127.0.0.1
if %INPUT%==2 set TTS_GAMESERVER=71.200.196.180
if %INPUT%==3 set TTS_GAMESERVER=192.99.167.192
if %INPUT%==4 (
    echo.
    set /P TTS_GAMESERVER=Gameserver: 
)

echo.

echo ===============================
echo Starting Toontown Stride...
echo ppython: %PPYTHON_PATH%
echo Username: %ttsUsername%
echo Gameserver: %TTS_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
pause