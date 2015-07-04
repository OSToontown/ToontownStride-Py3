import json
import os
import requests
from panda3d.core import *


username = os.environ['ttsUsername']
password = os.environ['ttsPassword']

accountServerEndpoint = 'http://www.toontownstride.com/api/'
session = requests.Session()
csrf_query = session.get(accountServerEndpoint + 'login/')
csrf = session.cookies.get_dict().get('csrftoken', '')
request = session.post(
    accountServerEndpoint + 'login/',
    data={'username': username, 'password': password, 'csrfmiddlewaretoken': csrf})

try:
    response = json.loads('{'+request.text.split('{', 1)[1]) # so that we ignore the csrf token
except ValueError:
    print "Couldn't verify account credentials."
else:
    if response['status'] != 7:
        print response['message']
    else:
        os.environ['TTS_PLAYCOOKIE'] = response['token']
        os.environ['TTS_GAMESERVER'] = response['gameserver']

        # Start the game:
        import toontown.toonbase.ClientStart
