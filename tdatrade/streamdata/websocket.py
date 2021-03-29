import websockets
import asyncio
import json

from websockets import client
from streamdata.stream_reqs import Principals

class WebSocketClient(Principals):

  def __init__(self):
    super().__init__()
    self.connection = None

  async def connect_stream(self):
    # Collecting uri and requests
    login_req = self.login()
    uri = self.uri()

    socket = await websockets.client.connect(uri)
    await socket.send(login_req)
    print('sending request')

    res = await socket.recv()
    print(json.loads(res))

    await socket.send(self.subscriptions())
    while True:
        res = await socket.recv()
        print(json.loads(res))

  async def connect(self):
    uri = self.uri()
    self.connection = await websockets.client.connect(uri)
    if self.connection.open:
        print("Connection established. Client correctly connected.")
        return self.connection

  async def receiveMessage(self):
    while True:
        try:
          # grab and decode the message
          message = await self.connection.recv()
          message_decoded = json.loads(message)
          if 'notify' not in message_decoded:
            print(message_decoded)
        
        except websockets.exceptions.ConnectionClosed:
          print("Connection with server closed")
          break
        
if __name__ == '__main__':
  client = WebSocketClient()
  client.forex_lvl1('EUR/USD')
  client.future_lvl1('/ES')
  asyncio.run(client.connect_stream())