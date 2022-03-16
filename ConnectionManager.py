from typing import *
import asyncio, json, websockets, time, sys
import janus

def encode_msg(msg: Dict) -> str:
    return json.dumps(msg, ensure_ascii=False)
    
def decode_msg(text: str) -> Dict:
    return json.loads(text)


class ConnectionManager:
    def __init__(self, ip, port, game_thread):
        self.uri = f"ws://{ip}:{port}"
        self.event_loop = asyncio.get_event_loop()
        #self.event_queue = asyncio.Queue()
        self.event_queue: janus.Queue[int] = None
        self.game_thread = game_thread
        self.stop = False

    def connect(self, room, nickname):
        print(f"Connecting to server {self.uri}...")
        #asyncio.get_event_loop().run_until_complete(hello())
        #self.event_loop.run_until_complete( self._start_connection(room, nickname) )
        #asyncio.run( self._start_connection(room, nickname) )
        try:
            asyncio.run( self._server_main() )
        except KeyboardInterrupt:
            self.disconnect()
        else:
            raise

    def disconnect(self):
        print(f"Disconnecting from server {self.uri}...")
        self.stop = True
        '''
        tasks = asyncio.Task.all_tasks()
        for t in tasks:
            t.cancel()
        '''
        pass

    def update(self, activity_type, activity_data=None):
        print(f"Server update for '{activity_type}'...")
        #asyncio.run( self._async_update(activity_type, activity_data) )
        #task = self.event_loop.create_task( self._async_update(activity_type, activity_data) )
        #self.event_loop.run_until_complete(task)
        print("Server update completed.")

    async def _server_main(self):
        #queue: janus.Queue[int] = janus.Queue()
        # self.event_queue.sync_q
        # self.event_queue.async_q
        self.event_queue = janus.Queue()

        loop = asyncio.get_running_loop()
        fut = loop.run_in_executor(None, self.game_thread)
        await self._async_listen()
        await fut
        queue.close()
        await queue.wait_closed()

    async def _async_listen():
        while not self.stop:
            val = await self.event_queue.async_q.get()
            await asyncio.sleep(1)
            print('Handled:', val)
'''
    async def _async_update(self, activity_type, activity_data):
        #await asyncio.sleep(0.1)
        await self.event_queue.put(encode_msg({'type': 'game_activity', 'activity': {
            'type': activity_type, 'value': activity_data
        }}))

    async def _start_connection(self, room, nickname):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(encode_msg({
                'type': 'join', 'room': room, 'player_name': nickname
            }))

            consumer_task = asyncio.ensure_future( self._consumer(websocket) )
            producer_task = asyncio.ensure_future( self._producer(websocket) )
            done = await asyncio.wait(
                [consumer_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            print("Connected.")

    async def _producer(self, websocket):
        while True:
            qevent = await self.event_queue.get()
            
            if qevent == None:
                break

            await websocket.send(qevent)

    async def _consumer(self, websocket):
        async for message_raw in websocket:
            msg = decode_msg(message_raw)
            print("Received:", msg)

'''
