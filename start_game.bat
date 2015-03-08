@echo off
title TTU Game Launcher
set /P PPYTHON_PATH=<PPYTHON_PATH

echo Choose your game server!
echo #1 - Localhost
echo #2 - DenialMC
echo #3 - DenialMC Server
echo #4 - Custom
echo #5 - Custom w/ RemoteDB
echo.
set /P INPUT=
set TTU_GAMESERVER=unset

if %INPUT%==1 set TTU_GAMESERVER=127.0.0.1
if %INPUT%==2 set TTU_GAMESERVER=5.15.21.225
if %INPUT%==3 set TTU_GAMESERVER=23.92.75.62
if %TTU_GAMESERVER%==unset (
    echo.
    set /P TTU_GAMESERVER=Gameserver: 
)

echo.
set /P ttuUsername=Username: 

if %INPUT%==5 (
    echo.
    set /P ttuPassword=Password: 
)

set TTU_PLAYCOOKIE=%ttuUsername%

echo ===============================
echo Starting Toontown Unlimited...
echo ppython: %PPYTHON_PATH%
echo Username: %ttuUsername%
echo Password: %ttuPassword%
echo Gameserver: %TTU_GAMESERVER%
echo ===============================

if %INPUT%==5 (
    %PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
) else (
    %PPYTHON_PATH% -m toontown.toonbase.ClientStart
)

pause