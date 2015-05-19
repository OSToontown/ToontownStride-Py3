#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " ttsUsername

# Export the environment variables:
export ttsUsername=$ttsUsername
export ttsPassword="password"
export TTS_PLAYCOOKIE=$ttsUsername
export TTS_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Stride..."
echo "Username: $ttsUsername"
echo "Gameserver: $TTS_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStart
