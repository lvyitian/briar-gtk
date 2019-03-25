# Copyright (c) 2019 Torsten Grote
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Originally coming from
# https://code.briarproject.org/grote/briar-cli-python-demo/blob/master/briar-cli.py

import asyncio
import json
import sys
import threading
from datetime import datetime

import requests
import websockets

HOST = 'localhost:7000'
CONTACT_ID = '1'

URL = 'http://%s/v1/messages/%s' % (HOST, CONTACT_ID)
URL_WS = 'ws://%s/v1/ws' % HOST

PROMPT = '$> '


def main():
    if len(sys.argv) != 2:
        print("Please provide auth token: %s <token>" % sys.argv[0])
        sys.exit(1)

    auth_token = sys.argv[1]
    load_history(auth_token)
    threading.Thread(target=get_message_stdin, args=[auth_token]).start()

    loop = asyncio.get_event_loop()
    loop.create_task(connect_websocket(auth_token))
    loop.run_forever()
    loop.close()


async def connect_websocket(token):
    async with websockets.connect(URL_WS) as ws:
        await ws.send(token)
        await get_message_websocket(ws)


async def get_message_websocket(ws):
    while not ws.closed and not asyncio.get_event_loop().is_closed():
        message = await ws.recv()
        m = json.loads(message)
        if m['name'] == 'ConversationMessageReceivedEvent':
            print()  # line-break
            print_message(m['data'])
            print(PROMPT, end='', flush=True)
    if not asyncio.get_event_loop().is_closed():
        asyncio.get_event_loop().create_task(get_message_websocket(ws))


def get_message_stdin(token):
    while True:
        body = input(PROMPT)
        if len(body) > 0:
            res = requests.post(URL, headers=get_auth_header(token), json={'text': body})
            if res.status_code == 200:
                print_message(res.json())
            else:
                print("Error: %d" % res.status_code)


def print_message(message):
    prefix = '>' if message['local'] else '<'
    time = get_timestamp(datetime.fromtimestamp(message['timestamp'] / 1000))
    print(f"{time} {prefix} {message['text']}")


def get_timestamp(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S')


def load_history(token):
    history = requests.get(URL, headers=get_auth_header(token)).json()
    for message in history:
        print_message(message)


def get_auth_header(token):
    return {'Authorization': 'Bearer %s' % token}


if __name__ == "__main__":
    main()

