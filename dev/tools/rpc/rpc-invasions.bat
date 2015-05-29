@echo off
cd ../../../
set /P serv=RPC Server:
"dependencies/panda/python/ppython.exe" "dev/tools/rpc/rpc-invasions.py" 6163636f756e7473 %serv%
pause