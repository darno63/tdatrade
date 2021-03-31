__all__ = (
    'place_order', 'cancel_order', 'save_order', 'delete_saved_order',
    'get_account', 'get_orders', 
)

from requests import request

from tdatrade.auth.tokens import get_tokens
from tdatrade.utils import auto_refresh, pretty_print, clean_dict

def status(func):
    def inner_decorator(*args, **kwargs):
        res = func(*args, **kwargs)
        print(res.status_code)
        return res
    return inner_decorator

def api_req(method, url_end, order=None, order_id=None):    
    auto_refresh()
    account_number, access_token = get_tokens(['account number', 'access token'])
    url = r'https://api.tdameritrade.com/v1/accounts/' + account_number + url_end
    return request(method, url, json=order, headers={"Authorization": "Bearer " + access_token})

@status
def place_order(order):
    url_end = r'/orders'
    return api_req("POST", url_end, order=order)

@status
def cancel_order(order_id):
    url_end = r'/orders/' + order_id
    return api_req("DELETE", url_end, order_id=order_id)

@status
def save_order(order):
    url_end = r'/savedorders'
    return api_req("POST", url_end, order=order)

@status
def delete_saved_order(saved_order_id):
    url_end = r'/savedorders/' + str(saved_order_id)
    return api_req("POST", url_end)

@status
def get_account(full_data = False, to_print=False):
    res = api_req("GET", '')
    json = res.json() if full_data else clean_dict(res.json())
    if to_print == True:
        pretty_print(json)
    return res

def get_orders(order_id=None):
    if order_id == None:
        url_end = r'/orders'
        json = api_req("GET", url_end).json()
        pretty_print(json)
        return json[0]['orderId']
    else:
        url_end = r'/orders/' + str(order_id)
        json = api_req("GET", url_end, order_id=order_id).json()
        pretty_print(json)
        return json['orderId']


