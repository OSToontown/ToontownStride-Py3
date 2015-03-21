@echo off
title TTU Game Launcher
set /P PPYTHON_PATH=<PPYTHON_PATH

echo Choose your game server!
echo #1 - Localhost
echo #2 - Custom
echo #3 - Custom w/ RemoteDB
echo.
set /P INPUT=
set TTU_GAMESERVER=unset

if %INPUT%==1 set TTU_GAMESERVER=127.0.0.1
if %TTU_GAMESERVER%==unset (
    echo.
    set /P TTU_GAMESERVER=Gameserver: 
)

echo.
set /P ttuUsername=Username: 

if %INPUT%==3 (
    echo.
    set /P ttuPassword=Password: 
)

set TTU_PLAYCOOKIE=%ttuUsername%

echo ===============================
echo Starting Toontown United...
echo ppython: %PPYTHON_PATH%
echo Username: %ttuUsername%
echo Password: %ttuPassword%
echo Gameserver: %TTU_GAMESERVER%
echo ===============================

if %INPUT%==3 (
    %PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
) else (
    %PPYTHON_PATH% -m toontown.toonbase.ClientStart
)

pause