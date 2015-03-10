#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " ttuUsername

# Export the environment variables:
export ttuUsername=$ttuUsername
export ttuPassword="password"
export TTU_PLAYCOOKIE=$ttuUsername
export TTU_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown United..."
echo "Username: $ttuUsername"
echo "Gameserver: $TTU_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStart
