@echo off
cd "../dependencies/astron/"
title Toontown Stride Astron
mode con: cols=60 lines=20

:start
astrond --loglevel info config/cluster.yml
PAUSE
goto start