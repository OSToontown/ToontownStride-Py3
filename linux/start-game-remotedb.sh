#!/bin/bash
cd ..

# Get the user input:
read -p "Username: " ttsUsername
read -s -p "Password: " ttsPassword
echo
read -p "Gameserver (DEFAULT: 167.114.28.238): " TTS_GAMESERVER
TTS_GAMESERVER=${TTS_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export ttsUsername=$ttsUsername
export ttsPassword=$ttsPassword
export TTS_PLAYCOOKIE=$ttsUsername
export TTS_GAMESERVER=$TTS_GAMESERVER

echo "==============================="
echo "Starting Toontown Stride..."
echo "Username: $ttsUsername"
echo "Gameserver: $TTS_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStartRemoteDB
