#!/bin/bash

day_old=$(date +%Y%m%d-%H:%M)
mkdir -p -v old/Safe2Net_${day_old}/
mv Safe2Net/ old/Safe2Net_${day_old}/
mkdir -p -v Safe2Net/doc
mkdir -p -v Safe2Net/cfg
cp -v ../doc/PikcioSDK_Python_2.05.odt Safe2Net/doc
python -m py_compile ../pikciosdk/log.py ../pikciosdk/pattern.py ../pikciosdk/PikcioChain.py ../pikciosdk/config.py ../pikciosdk/run.py
cp -v ../pikciosdk/log.pyc Safe2Net
cp -v ../pikciosdk/pattern.pyc Safe2Net
cp -v ../pikciosdk/PikcioChain.pyc Safe2Net
cp -v ../pikciosdk/config.pyc Safe2Net
cp -v ../pikciosdk/run.pyc Safe2Net

# create empty config file
printf '%s
[application]
name =
port =

[log]
level = 3
directory = log
file = pikciochain.log
life_time = 30

[server]
public_ip =
private_ip =
public_port =
private_port =
tls =

[api_client]
client_id =
client_secret =
auth_type =
redirect_uri =
scope =
' > Safe2Net/cfg/global.cfg

# create test script
printf "%s
import hashlib

from PikcioChain import ClientAPI
from log import Logger
from config import get_config
config = get_config()


def run_test():
    log = Logger()

    # initiate connexion to API
    username = 'your_name'
    password_hash = hashlib.sha1('your_password').digest().encode('hex')
    client_api = ClientAPI(username=username, password=password_hash)

    p = client_api.get_access_token()

    # example :
    result = client_api.get_contacts()

    if isinstance(result, str):
        log.debug('=== {0} ==='.format(result))
    else:
        log.debug('=== {0} ==='.format(result.content))
" > Safe2Net/tests.py