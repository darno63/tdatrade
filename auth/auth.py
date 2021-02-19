from time import time
import urllib.parse as up

import requests
from requests_oauthlib import OAuth2Session

from auth.tokens import get_tokens, save_tokens

def refresh_access_token():
    url = r'https://api.tdameritrade.com/v1/oauth2/token'
    refresh_token = get_tokens('refresh token')
    client_id = get_tokens('client id')
    body = { 'grant_type': 'refresh_token', 'refresh_token': refresh_token, 'client_id': client_id }

    res = requests.post(url, data=body)

    access_token = res.json()["access_token"]
    access_token_ts = time()

    print("\nCode:", res.status_code)
    if res.status_code == 200:
        save_tokens(access_token=access_token, access_token_ts=access_token_ts)
        return access_token

def authentication():

    client_id = get_tokens("client id")
    redirect_uri = 'https://127.0.0.1'
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)

    authorization_url, state = oauth.authorization_url(
        'https://auth.tdameritrade.com/auth')

    print(authorization_url)
    code = input("\nInput Code after login:\n")
    print("\n" + up.unquote(code))


if __name__ == "__main__":
    refresh_access_token()