@echo off

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttuUsername="Username: "
set /P ttuPassword="Password: "
set /P TTU_GAMESERVER="Gameserver (DEFAULT: 167.114.28.238): " || ^
set TTU_GAMESERVER=167.114.28.238

echo ===============================
echo Starting Toontown Unlimited...
echo ppython: %PPYTHON_PATH%
echo Username: %ttuUsername%
echo Gameserver: %TTU_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
pause
