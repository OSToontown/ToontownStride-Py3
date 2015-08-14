import json
import os
import requests
from panda3d.core import *


username = os.environ['ttsUsername']
password = os.environ['ttsPassword']

accountServerEndpoint = 'https://toontownstride.com/api/'
request = requests.post(
    accountServerEndpoint + 'login/',
    data={'username': username, 'password': password, 'distribution': 'qa'})

try:
    response = json.loads(request.text)
except ValueError:
    print "Couldn't verify account credentials."
else:
    if response['status'] != 7:
        print response['message']
    else:
        os.environ['TTS_PLAYCOOKIE'] = response['token']
        os.environ['TTS_GAMESERVER'] = response['gameserver']

        # Start the game:
        import toontown.toonbase.ToontownStart
