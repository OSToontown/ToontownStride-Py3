@echo off
title TTU Game Launcher
set /P PPYTHON_PATH=<PPYTHON_PATH

echo Choose your game server!
echo #1 - Localhost
echo #2 - Custom
echo.
set /P INPUT=
set server=unset

if %INPUT%==1 set server=127.0.0.1
if %server%==unset (
    echo.
    set /P server=Gameserver: 
)

echo.
set /P user=Username: 

echo ===============================
echo Starting Toontown United...
echo ppython: %PPYTHON_PATH%
echo Username: %user%
echo Password: %ttuPassword%
echo Gameserver: %server%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart %server% %user%
pause