#TODO
Create base request class or token class
Fix 'api.py' file and put everything related to auth and tokens in auth.py

# Architecture 
- authorization
- order builder
- trade api
- data api
- utils




## Build Order
### STOCK requirements to saved collection
"session": "'NORMAL' or 'AM' or 'PM' or 'SEAMLESS'",
"duration": "'DAY' or 'GOOD_TILL_CANCEL' or 'FILL_OR_KILL'",
"orderType": "'MARKET' or 'LIMIT' or 'STOP' or 'STOP_LIMIT' or 'TRAILING_STOP' or 'MARKET_ON_CLOSE' or 'EXERCISE' or 'TRAILING_STOP_LIMIT' or 'NET_DEBIT' or 'NET_CREDIT' or 'NET_ZERO'",
"orderStrategyType": "'SINGLE' or 'OCO' or 'TRIGGER'",
"orderLegCollection": [
        {
            "instrument": {
                "assetType": "'EQUITY' or 'OPTION' or 'INDEX' or 'MUTUAL_FUND' or 'CASH_EQUIVALENT' or 'FIXED_INCOME' or 'CURRENCY'",
                "cusip": "string",
                "symbol": "string",
                "description": "string"
            }
            "instruction": "'BUY' or 'SELL' or 'BUY_TO_COVER' or 'SELL_SHORT' or 'BUY_TO_OPEN' or 'BUY_TO_CLOSE' or 'SELL_TO_OPEN' or 'SELL_TO_CLOSE' or 'EXCHANGE'",
            "positionEffect": "'OPENING' or 'CLOSING' or 'AUTOMATIC'",
            "quantity": 0,
        }
