# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from urllib.parse import urljoin

from requests import get as _get
from requests import post as _post

from briar.api.constants import BASE_HTTP_URL
from briar.api.model import Model


class PrivateChat(Model):

    API_ENDPOINT = "messages/"

    _contact_id = 0
    _on_message_received_callback = None

    def __init__(self, api, contact_id):
        super().__init__(api)
        self._contact_id = contact_id

    def get(self):
        url = urljoin(BASE_HTTP_URL,
                      self.API_ENDPOINT + "/%d" % self._contact_id)
        request = _get(url, headers=self._headers)
        return request.json()

    def watch_messages(self, callback):
        self._on_message_received_callback = callback
        self._api.socket_listener.watch("ConversationMessageReceivedEvent",
                                        self._on_message_received)

    def _on_message_received(self, event):
        self._on_message_received_callback(event['data'])

    def send(self, message):
        url = urljoin(BASE_HTTP_URL,
                      self.API_ENDPOINT + "/%i" % self._contact_id)
        _post(url, headers=self._headers, json={"text": message})
