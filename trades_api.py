from auth.tokens import get_tokens
from utils import auto_refresh, pretty_print
from requests import request


def trade(func):
    def inner_trade(*args):
        auto_refresh()
        order, method, url_end = func(*args)
        tokens_to_get = ['account number', 'access token']
        account_number, access_token = get_tokens(tokens_to_get)
        url = r'https://api.tdameritrade.com/v1/accounts/' + account_number + url_end

        res = request(method, url, json=order, headers={"Authorization": "Bearer " + access_token})
        print(res.status_code)
        return res
    return inner_trade

def api_req(method, url_end, order=None, order_id=None):    
    auto_refresh()
    tokens_to_get = ['account number', 'access token']
    account_number, access_token = get_tokens(tokens_to_get)
    url = r'https://api.tdameritrade.com/v1/accounts/' + account_number + url_end

    return request(method, url, json=order, headers={"Authorization": "Bearer " + access_token})


@trade
def save_order(order):
    method = 'POST'
    url_end = r'/savedorders'
    return order, method, url_end

@trade
def place_order(order):
    method = 'POST'
    url_end = r'orders'
    return order, method, url_end



'''
def place_order(order):
    auto_refresh()
    tokens_to_get = ['account number', 'access token']
    account_number, access_token = get_tokens(tokens_to_get)
    url = r'https://api.tdameritrade.com/v1/accounts/' + account_number + r'/orders'

    res = requests.post(url, json=order, headers={"Authorization": "Bearer " + access_token})
    print(res.status_code)

def save_order(order):
    auto_refresh()
    tokens_to_get = ['account number', 'access token']
    account_number, access_token = get_tokens(tokens_to_get)
    url = r'https://api.tdameritrade.com/v1/accounts/' + account_number + r'/savedorders'

    res = requests.post(url, json=order, headers={"Authorization": "Bearer " + access_token})
    print(res.status_code)

def cancel_order(order_id):
    auto_refresh()
    tokens_to_get = ['account number', 'access token']
    account_number, access_token = get_tokens(tokens_to_get)
    url = r'https://api.tdameritrade.com/v1/accounts/' + account_number + r'/orders/' + order_id

    res = request("DELETE", url, headers={"Authorization": "Bearer " + access_token})
    print(res.status_code)
'''
def cancel_order(order_id):
    url_end = r'/orders/' + order_id
    res = api_req("DELETE", url_end, order_id=order_id)
    print(res.status_code)

def get_orders(order_id=None):
    if order_id == None:
        url_end = r'orders'
        json = api_req("GET", url_end).json()
        pretty_print(json)
        return json #[0]['orderId']
    else:
        url_end = r'orders/' + order_id
        json = api_req("GET", url_end, order_id=order_id).json()
        pretty_print(json)
        return json['orderId']

'''
def get_orders(order_id=None):
    auto_refresh()
    tokens_to_get = ['account number', 'access token']
    account_number, access_token = get_tokens(tokens_to_get)
    if order_id == None:
        url = r'https://api.tdameritrade.com/v1/accounts/' + account_number + r'/orders'
    else:
        url = r'https://api.tdameritrade.com/v1/accounts/' + account_number + r'/orders/' + order_id

    res = request("GET",url, headers={"Authorization": "Bearer " + access_token})
    json = res.json()
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(json)
    if type(json) == list:
        return json[0]['orderId']
    else:
        return json['orderId']
'''