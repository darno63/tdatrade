from pprint import PrettyPrinter, pprint
from time import time, localtime, strftime

from auth.auth import refresh_access_token
from auth.tokens import get_tokens

def auto_refresh():
    ts = get_tokens('access token ts')
    if (time() - float(ts)) < 1800:
        pass
    else:
        refresh_access_token()
        print('Token Expired: Automatically Refreshed')

def pretty_print(text):
    pp = PrettyPrinter(indent=4)
    pprint(text)

def clean_dict(arg):
    if type(arg) == dict:
        to_del = []
        for key in arg.keys():
            if bool(arg[key]):
                arg[key] = clean_dict(arg[key])
            else:
                to_del.append(key)
        for key in to_del:
            del arg[key]
    elif type(arg) == list:
        n = len(arg)
        to_del = []
        for i in range(0, n):
            if bool(arg[i]):
                arg[i] = clean_dict(arg[i])
            else:
                to_del.append(i)
        for i in to_del:
            del arg[i]
    elif type(arg) == int and len("%i" % arg) == 13:
        t = localtime(arg // 1000)
        arg = strftime("%a, %d %b %Y %I:%M%p", t)
    else:
        pass
    return arg

def test():
    candles = {'candles': [{'open': 837.8, 'high': 859.5, 'low': 828.62, 'close': 846.64, 'volume': 91697493, 'datetime': 1610949600000}, {'open': 855.0, 'high': 900.4, 'low': 780.1, 'close': 793.53, 'volume': 153007757, 'datetime': 1611554400000}, {'open': 814.29, 'high': 880.5, 'low': 795.5601, 'close': 852.23, 'volume': 102460406, 'datetime': 1612159200000}, {'open': 869.67, 'high': 877.77, 'low': 785.3306, 'close': 816.12, 'volume': 116926526, 'datetime': 1612764000000}], 'symbol': 'TSLA', 'empty': False}
    res = clean_dict(candles)
    print(res)
