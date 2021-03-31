from time import time
import websockets
import asyncio
import json
import time
from contextlib import suppress
from websockets import client

from tdatrade.stream.stream_reqs import Principals

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
    await asyncio.create_task(self.receiveMessage())

  async def _disconnect_stream(self):
    await self.connection.send(self.logout())
    print('Logging Out')
    await asyncio.sleep(1)

  def connect(self):
    try:
      loop = asyncio.new_event_loop()
      loop.create_task(self.connect_stream())
      loop.run_forever()
    except KeyboardInterrupt:
      loop.run_until_complete(self._disconnect_stream())
      loop.stop()
      self._cancel_tasks(loop)
      loop.close()
  
  def _cancel_tasks(self, loop):
    to_cancel = asyncio.all_tasks(loop)
    for task in to_cancel:
      task.cancel()
      with suppress(asyncio.CancelledError):
        loop.run_until_complete(task)
      if task.cancelled():
        continue
      if task.exception() is not None:
        loop.call_exception_handler({
          'message': 'unhandled exception',
          'exception': task.exception(),
          'task': task
        })

  async def receiveMessage(self):
    while True:
        try:
          # grab and decode the message
          message = await self.connection.recv()
          message_decoded = json.loads(message)
          if self.callback_func is not None:
            self.callback_func(message_decoded)

          #if 'notify' not in message_decoded:
          #  print(message_decoded)
        
        except websockets.exceptions.ConnectionClosed:
          print("Connection with server closed")
          break
  
  def create_callback(self, function):
    self.callback_func = function

def callback_print(res):
  print(res)  
        
if __name__ == '__main__':
  client = WebSocketClient()
  client.forex_lvl1('EUR/USD')
  client.future_lvl1('/ES')
  client.create_callback(callback_print)
  client.connect()