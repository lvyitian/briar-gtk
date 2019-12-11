# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import asyncio
import json
from threading import Thread

import websockets

from briar.api.constants import WEBSOCKET_URL
from briar.api.model import Model


class SocketListener(Model):  # pylint: disable=too-few-public-methods

    def watch(self, event, callback):
        websocket_thread = Thread(target=self._start_watch_loop,
                                  args=(event, callback),
                                  daemon=True)
        websocket_thread.start()

    def _start_watch_loop(self, event, callback):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self._start_websocket(event, callback))
        loop.run_forever()
        loop.close()

    async def _start_websocket(self, event, callback):
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            await websocket.send(self._api.auth_token)
            await self._watch_messages(websocket, event, callback)

    async def _watch_messages(self, websocket, event, callback):
        while not websocket.closed and not\
                asyncio.get_event_loop().is_closed():
            message_json = await websocket.recv()
            message = json.loads(message_json)
            if message['name'] == event:
                callback(message)
        if not asyncio.get_event_loop().is_closed():
            asyncio.get_event_loop().create_task(
                self._watch_messages(websocket, event, callback))
