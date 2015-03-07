@echo off

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttuUsername="Username: "

rem Export the environment variables:
set ttuPassword=password
set TTU_PLAYCOOKIE=%ttuUsername%
set TTU_GAMESERVER=5.15.21.225

echo ===============================
echo Starting Toontown Unlimited...
echo ppython: %PPYTHON_PATH%
echo Username: %ttuUsername%
echo Gameserver: %TTU_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause
