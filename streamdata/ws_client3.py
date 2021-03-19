import websockets
import asyncio
import json

from streamdata.stream_reqs import Principals

class WebSocketClient():

  def __init__(self):
      self.cnxn = None
      self.crsr = None
  
  async def connect(self, uri):
    self.connection = await websockets.client.connect(uri)
    if self.connection.open:
        print("Connection established. Client correctly connected.")
        return self.connection

  async def sendMessage(self, message):
    await self.connection.send(message)

  async def receiveMessage(self, connection):
    while True:
        try:
          # grab and decode the message
          message = await connection.recv()
          message_decoded = json.loads(message)
          if 'notify' not in message_decoded:
            print(message_decoded)
        
        except websockets.exceptions.ConnectionClosed:
          print("Connection with server closed")
          break

  async def heartbeat(self, connection):
    while True:
      try:
        await connection.send("ping")
        await asyncio.sleep(5)
      except websockets.exceptions.ConnectionClosed:
        print("")

        
if __name__ == '__main__':
  # Initialize Princepals
  principals = Principals()
  # Collecting uri and requests
  login_req = principals.login_request()
  uri = principals.uri()
  # Creating client object
  client = WebSocketClient()
  # Define an event loop
  loop = asyncio.get_event_loop()
  # Start connection and get client connection protocol
  connection = loop.run_until_complete(client.connect(uri))
  # Start listener and heartbeat
  tasks = [
    asyncio.ensure_future(client.receiveMessage(connection)),
    asyncio.ensure_future(client.sendMessage(login_req)),
    asyncio.ensure_future(client.receiveMessage(connection)),
    asyncio.ensure_future(client.sendMessage(principals.chart_equity("AAPL"))),
    asyncio.ensure_future(client.receiveMessage(connection))
  ]

  # run your tasks
  loop.run_until_complete(asyncio.wait(tasks))