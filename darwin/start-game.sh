#!/bin/sh
cd ..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

# Get the user input:
read -p "Username: " ttuUsername
read -p "Gameserver (DEFAULT:  167.114.28.238): " TTU_GAMESERVER
TTU_GAMESERVER=${TTU_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export ttuUsername=$ttuUsername
export ttuPassword="password"
export TTU_PLAYCOOKIE=$ttuUsername
export TTU_GAMESERVER=$TTU_GAMESERVER

echo "==============================="
echo "Starting Toontown Unlimited..."
echo "Username: $ttuUsername"
echo "Gameserver: $TTU_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ClientStart
