@echo off
title TTU Game Launcher
set /P PPYTHON_PATH=<PPYTHON_PATH

echo Choose your game server!
echo #1 - Localhost
echo #2 - Custom
echo #3 - Loudrob
echo.
set /P INPUT=
set server=unset

if %INPUT%==1 set TTU_GAMESERVER=127.0.0.1
if %INPUT%==3 set TTU_GAMESERVER=71.200.196.180

if %TTU_GAMESERVER%==unset (
    echo.
    set /P TTU_GAMESERVER=Gameserver: 
)

echo.
set /P TTU_PLAYCOOKIE=Username: 

echo ===============================
echo Starting Toontown United...
echo ppython: %PPYTHON_PATH%
echo Username: %TTU_PLAYCOOKIE%
echo Gameserver: %TTU_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause