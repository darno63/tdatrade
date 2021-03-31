# TD Ameritrade Python API
Purpose of this package is allow a simple interface to authenticate trades for TD Ameritrade Account Holders using the official API.

## Installation
```bash
pip install git+https://github.com/darno63/tdatrade.git --upgrade
```
  
  
## Getting Started
Requires a TD Ameritrade Account with at least level one streaming access  
1. Create a developer account through TD Ameritrade [here](https://developer.tdameritrade.com/)
2. Go to My Apps to create your own app and take note of your Consumer Key

<<<<<<< HEAD
 ---*under construction*---

## Real-time Streaming
The package `tdatrade.stream` provides the class `WebSocketClient()` which allows for building a group of requests and then handles sending and receiveing data form TDA's data stream.  
```python
client = WebSocketClient()
client.forex_lvl1('EUR/USD')
client.future_lvl1('/ES')
client.connect()
```

You can also add a callback function to handle the received data. All callback functions must contain one argument that respresents the received message in python dictionary format.
```python
# simple callback function that prints message contents to console
def callback_print(res):
  print(res)  

client = WebSocketClient()
client.forex_lvl1('EUR/USD')
client.future_lvl1('/ES')
client.create_callback(callback_print)
client.connect()
```
=======
Next Run authenticate  
``
    authenticate()
      ``
# TODO
1. fix pathing for imports
2. fix FILE_LOCATION path for tokens.ini
3. add requests-oauth to requires
>>>>>>> 3a6a3a00e60d3d1f1f7bcd74cb584db5f03a6701
