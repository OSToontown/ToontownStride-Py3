@echo off
cd..

title TTS Game Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo Choose your game server!
echo #1 - Localhost
echo #2 - Custom
echo #3 - Loudrob
echo.
set /P INPUT=
set server=unset

if %INPUT%==1 set TTS_GAMESERVER=127.0.0.1
if %INPUT%==3 set TTS_GAMESERVER=71.200.196.180

if %TTS_GAMESERVER%==unset (
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
