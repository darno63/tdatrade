__all__ = (
    'market_hours', 'get_data', 'get_price_history'
)

import requests
from time import time
from datetime import date, datetime

from tdatrade.auth.tokens import get_tokens
from tdatrade.auth.auth import refresh_access_token
from tdatrade.utils import clean_dict, auto_refresh, pretty_print

def main():
    symbol_input = input("Ticker Symbol: ")
    choice = input("What do you want to see? (history or data)\n")
    if (choice == "history"):
        get_price_history(symbol_input)
    else:
        get_data(symbol_input)

def market_hours(markets = 'EQUITY, OPTION'):
    auto_refresh()
    access_token = get_tokens('access token')
    url = r'https://api.tdameritrade.com/v1/marketdata/hours'
    params = {
        'markets': markets,
        'data': date.today().isoformat(),
    }
    headers = {'Authorization': 'Bearer ' + access_token}
    return requests.get(url, params=params, headers=headers)

def get_user_principals(fields):
    # 'streamerSubscriptionKeys,streamerConnectionInfo,preferences,surrogateIds'
    auto_refresh()
    url = r'https://api.tdameritrade.com/v1/userprincipals'
    access_token = get_tokens('access token')
    params = {'fields': fields}
    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.get(url, params=params, headers=headers)
    print(res.status_code)
    return res

def get_data(symbol):
    tokens_to_get = ['account number', 'access token', 'access token ts', 'client id']
    account_number, access_token, ts, client_id = get_tokens(tokens_to_get)
    client_id = client_id.split('@')[0]
    url = r'https://api.tdameritrade.com/v1/instruments'
    
    params = {"apikey": client_id, "symbol": symbol, "projection": "fundamental"}
    
    if (time() - float(ts)) < 1800:
        res = requests.get(url, params=params, headers={"Authorization": "Bearer " + access_token})
    else:
        refresh_input = input("ERROR: access token has expired, do you want to refresh it? (y/n)\n")
        if (refresh_input in ["y", "Y"]):
            refresh_access_token()
            access_token = get_tokens('access token')
            res = requests.get(url, params=params, headers={"Authorization": "Bearer " + access_token})
        else:
            return None

    pretty_print(clean_dict(res.json()))
    print(res.status_code)
    print(res.url)
    return res.json()

def get_price_history(symbol, frequency_type="weekly", frequency=1, period_type="month",
                      period=None, enddate=None, startdate=None, to_pretty_print=False):
    auto_refresh()
    access_token, client_id = get_tokens(['access token', 'client id'])
    url = r'https://api.tdameritrade.com/v1/marketdata/' + symbol + r'/pricehistory'
    
    params = {
        "apikey": client_id.split('@')[0], 
        "periodType": period_type, 
        "frequencyType": frequency_type, 
        "frequency": frequency
    }

    if period != None and startdate != None:
        print('ERROR: period and startdate can not both be used')
    if period != None:
        params['period'] = period
    if enddate != None:
        params['endDate'] = int(datetime.fromisoformat(enddate).timestamp()) * 1000
    if startdate != None:
        params['startDate'] = int(datetime.fromisoformat(startdate).timestamp()) * 1000
    
    res = requests.get(url, params=params, headers={"Authorization": "Bearer " + access_token})

    if to_pretty_print == True:
        pretty_print(clean_dict(res.json()))
    return res.json()

def get_price_history2(symbol):
    tokens_to_get = ['access token', 'access token ts', 'client id']
    access_token, ts, client_id = get_tokens(tokens_to_get)
    client_id = client_id.split('@')[0]
    url = r'https://api.tdameritrade.com/v1/marketdata/' + symbol + r'/pricehistory'
    
    params = {"apikey": client_id, "periodType": "month", "period": 1, "frequencyType": "weekly", "frequency": 1}
    
    if (time() - float(ts)) < 1800:
        res = requests.get(url, params=params, headers={"Authorization": "Bearer " + access_token})
    else:
        refresh_input = input("ERROR: access token has expired, do you want to refresh it? (y/n)\n")
        if (refresh_input in ["y", "Y"]):
            refresh_access_token()
            access_token = get_tokens('access token')
            res = requests.get(url, params=params, headers={"Authorization": "Bearer " + access_token})
        else:
            return None
    pretty_print(clean_dict(res.json()))
    print(res.status_code)
    print(res.url)
    return res.json()

if __name__ == "__main__":
    get_price_history('TSLA')
