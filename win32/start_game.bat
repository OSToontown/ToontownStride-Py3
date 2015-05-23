@echo off
cd..

title Toontown Stride Game Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo Choose your connection method!
echo.
echo #1 - Localhost
echo #2 - Dev Server
echo #3 - Custom
echo.

set /P INPUT=Selection: 

if %INPUT%==1 (
    set TTS_GAMESERVER=127.0.0.1
) else if %INPUT%==2 (
    set TTS_GAMESERVER=167.114.220.172
) else if %INPUT%==3 (
    echo.
    set /P TTS_GAMESERVER=Gameserver: 
) else exit

echo.

if %INPUT%==2 (
    set /P ttsUsername="Username: "
    set /P ttsPassword="Password: "
) else (
    set /P TTS_PLAYCOOKIE=Username: 
)

echo.

echo ===============================
echo Starting Toontown Stride...
echo ppython: %PPYTHON_PATH%

if %INPUT%==2 (
    echo Username: %ttsUsername%
) else (
    echo Username: %TTS_PLAYCOOKIE%
)

echo Gameserver: %TTS_GAMESERVER%
echo ===============================

if %INPUT%==2 (
    %PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
) else (
    %PPYTHON_PATH% -m toontown.toonbase.ClientStart
)

pause
