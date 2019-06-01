# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.constants import WEBSOCKET_URL
from briar.api.models.model import Model

import asyncio
import json
from threading import Thread
import websockets


# TODO: Make more general; currently very specific to private messages
class SocketListener(Model):

    def watch(self, callback, event, contact_id="0"):
        websocket_thread = Thread(target=self._start_watch_loop,
                                  args=(callback, event, contact_id),
                                  daemon=True)
        websocket_thread.start()

    def _start_watch_loop(self, callback, event, contact_id="0"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self._start_websocket(callback, event, contact_id))
        loop.run_forever()
        loop.close()

    async def _start_websocket(self, callback, event, contact_id="0"):
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            await websocket.send(self._api.auth_token)
            await self._watch_messages(websocket, event, callback)

    async def _watch_messages(self, websocket, event, callback):
        while not websocket.closed and not\
                         asyncio.get_event_loop().is_closed():
            message = await websocket.recv()
            message = json.loads(message)
            if message['name'] == event:
                callback(message['data'])
        if not asyncio.get_event_loop().is_closed():
            asyncio.get_event_loop().create_task(
                self._watch_messages(websocket, callback))
