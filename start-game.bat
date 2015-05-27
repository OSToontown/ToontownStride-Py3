@echo off

title Toontown Stride Game Launcher

echo Choose your connection method!
echo.
echo #1 - Localhost
echo #2 - Dev Server
echo #3 - Custom
echo.

:selection

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    set TTS_GAMESERVER=127.0.0.1
) else if %INPUT%==2 (
    set TTS_GAMESERVER=167.114.220.172
) else if %INPUT%==3 (
    echo.
    set /P TTS_GAMESERVER=Gameserver: 
) else (
	goto selection
)

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
echo ppython: "panda/python/ppython.exe"

if %INPUT%==2 (
    echo Username: %ttsUsername%
) else (
    echo Username: %TTS_PLAYCOOKIE%
)

echo Gameserver: %TTS_GAMESERVER%
echo ===============================

if %INPUT%==2 (
    "panda/python/ppython.exe" -m toontown.toonbase.ClientStartRemoteDB
) else (
    "panda/python/ppython.exe" -m toontown.toonbase.ClientStart
)

pause
