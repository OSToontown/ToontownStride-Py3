@echo off
title TTS Game Launcher
set /P PPYTHON_PATH=<PPYTHON_PATH

echo Choose your game server!
echo #1 - Localhost
echo #2 - Loudrob
echo #3 - Steve
echo #4 - Custom
echo.
set /P INPUT=

if %INPUT%==1 set TTS_GAMESERVER=127.0.0.1
if %INPUT%==2 set TTS_GAMESERVER=71.200.196.180
if %INPUT%==3 set TTS_GAMESERVER=167.114.220.172
if %INPUT%==4 (
    echo.
    set /P TTS_GAMESERVER=Gameserver: 
)

echo.
set /P TTS_PLAYCOOKIE=Username: 

echo ===============================
echo Starting Toontown Stride...
echo ppython: %PPYTHON_PATH%
echo Username: %TTS_PLAYCOOKIE%
echo Gameserver: %TTS_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause