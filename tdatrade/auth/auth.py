from time import time
from re import split as re_split
import urllib.parse as up

import requests
from requests_oauthlib import OAuth2Session

from auth.tokens import get_tokens, save_tokens

AUTH_URL = r'https://api.tdameritrade.com/v1/oauth2/token'
REDIRECT_URL = r'https://127.0.0.1'

def refresh_access_token():
    refresh_token = get_tokens('refresh token')
    client_id = get_tokens('client id')
    body = { 'grant_type': 'refresh_token', 'refresh_token': refresh_token, 'client_id': client_id }

    res = requests.post(AUTH_URL, data=body)

    access_token = res.json()["access_token"]
    access_token_ts = time()

    print("\nCode:", res.status_code)
    if res.status_code == 200:
        save_tokens(access_token=access_token, access_token_ts=access_token_ts)
        return access_token

def authentication():
    client_id = get_tokens("client id")
    oauth = OAuth2Session(client_id, redirect_uri=REDIRECT_URL)

    authorization_url, state = oauth.authorization_url(
        'https://auth.tdameritrade.com/auth')

    print('\n' + authorization_url)
    code = input("\nUse the Link above and Login into TDA account, then paste the url sent to your local server below:\n")
    code = re_split(r'[\?|&].+?=', up.unquote(code))[1]
    print("\n" + code)

    body = { 'grant_type': 'authorization_code', 'access_type': 'offline', 'code': code,
             'client_id': client_id, 'redirect_uri': REDIRECT_URL}

    res = requests.post(url=AUTH_URL, data=body)
    print(res.request.url)
    print(res.json())

    access_token = res.json()['access_token']
    refresh_token = res.json()['refresh_token']
    access_token_ts = time()

    print("\nStatus Code:", res.status_code)
    if res.status_code == 200:
        print("Authorization Complete")
        save_tokens(refresh_token=refresh_token, access_token=access_token, access_token_ts=access_token_ts)
        

if __name__ == "__main__":
    refresh_access_token()