@echo off
set /P serv=RPC Server:

python rpc-invasions.py 6163636f756e7473 %serv%