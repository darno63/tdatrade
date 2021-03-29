import websockets
import asyncio
import json

from websockets import client
from streamdata.stream_reqs import Principals

class WebSocketClient(Principals):

  def __init__(self):
    super().__init__()
    self.connection = None
    self.callback_func = None

  async def connect_stream(self):
    # Collecting uri and requests
    login_req = self.login()
    uri = self.uri()

    self.connection = await websockets.client.connect(uri)
    if self.connection.open:
        print("Connection established. Client correctly connected.")

    await self.connection.send(login_req)
    print('sending request')

    res = await self.connection.recv()
    print(json.loads(res))

    await self.connection.send(self.subscriptions())
    task = asyncio.create_task(self.receiveMessage())
    await task
    """
    await self.receiveMessage()
    while True:
        res = await connection.recv()
        print(json.loads(res))
    """
  
  def connect(self):
    asyncio.run(self.connect_stream())

  async def receiveMessage(self):
    while True:
        try:
          # grab and decode the message
          message = await self.connection.recv()
          message_decoded = json.loads(message)
          if self.callback_func is not None:
            self.callback_func(message_decoded)

          if 'notify' not in message_decoded:
            print(message_decoded)
        
        except websockets.exceptions.ConnectionClosed:
          print("Connection with server closed")
          break
  
  def create_callback(self, function):
    self.callback_func = function

  
        
if __name__ == '__main__':
  client = WebSocketClient()
  client.forex_lvl1('EUR/USD')
  client.future_lvl1('/ES')
  #client.chart_futures('/ES')
  client.connect()