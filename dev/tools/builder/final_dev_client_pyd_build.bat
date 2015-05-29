@echo off
cd ../../../
rem NOTE: This must be run from the visual c++ 2008 32 bit command prompt!
set PPYTHON_PATH="dependencies/panda/python/ppython.exe"
echo ppython path: %PPYTHON_PATH%
%PPYTHON_PATH% prepare_client.py --distribution dev
echo Preparing client done!
echo Time to build client.
%PPYTHON_PATH% build_client.py --main-module toontown.toonbase.ClientStartRemoteDB
rem ClientStartRemoteDB requires ttsUsername and ttsPassword
echo Done! The PYD is in /build/GameData.pyd.
pause