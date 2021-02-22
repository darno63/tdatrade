import asyncio
import time
import json
from calendar import timegm
import urllib.parse as up

import websockets


from data import get_user_principals

def json_to_query(json):
    query =  '&'.join([f'{key}={val}' for key, val in json.items()])
    return up.quote(query)

def build_creds():
    res = get_user_principals('streamerSubscriptionKeys,streamerConnectionInfo').json()
    stream_token_ts = res['streamerInfo']['tokenTimestamp']
    struct_time = time.strptime(stream_token_ts, '%Y-%m-%dT%H:%M:%S+0000')
    stream_token_epoch = timegm(struct_time) * 100

    credentials = {
        "userid": res['accounts'][0]['accountId'],
        "token": res['streamerInfo']['token'],
        "company": res['accounts'][0]['company'],
        "segment": res['accounts'][0]['segment'],
        "cddomain": res['accounts'][0]['accountCdDomainId'],
        "usergroup": res['streamerInfo']['userGroup'],
        "accesslevel": res['streamerInfo']['accessLevel'],
        "authorized": "Y",
        "timestamp": stream_token_epoch,
        "appid": res['streamerInfo']['appId'],
        "acl": res['streamerInfo']['acl']
    }

    request = {
        "requests": [
            {
                "service": "ADMIN",
                "command": "LOGIN",
                "requestid": 0,
                "account": res['accounts'][0]['accountId'],
                "source": res['streamerInfo']['appId'],
                "parameters": {
                    "credential": json_to_query(credentials),
                    "token": res['streamerInfo']['token'],
                    "version": "1.0"
                }
            }
        ]
    }

    uri = "wss://" + res['streamerInfo']['streamerSocketUrl'] + "/ws"
    return json.dumps(request), uri


async def connect_stream():
    req, uri = build_creds()
    async with websockets.connect(uri) as websocket:
        await websocket.send(req)
    
        res = await websocket.recv()
        print(res)
        websocket.close()


# https://github.com/aaugustin/websockets/issues/484
asyncio.get_event_loop().run_until_complete(connect_stream())

