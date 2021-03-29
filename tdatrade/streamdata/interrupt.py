import asyncio
import logging
import websockets

async def shutdown():
  shutdown_event = asyncio.Event()
  logging.info("waiting for shutdown")
  await shutdown_event.wait()

## example
async def waiter(event):
  print('waiting')
  await event.wait()
  print('... got it')

async def hello(stop):
    async with websockets.connect('ws://localhost:8765') as ws:
        # How do we interrupt here?
        async for msg in ws:
            print(msg)

loop = asyncio.get_event_loop()

stop = asyncio.Future()
client_task = loop.create_task(hello(stop))  # modified line

try:
    loop.run_forever()

except KeyboardInterrupt:
    client_task.cancel()  # modified line

    pending = asyncio.Task.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))

    print('All tasks concluded.')
