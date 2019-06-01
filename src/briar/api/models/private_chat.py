# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.constants import BASE_HTTP_URL
from briar.api.models.model import Model

from requests import get as _get
from requests import post as _post
from urllib.parse import urljoin


class PrivateChat(Model):

    def get(self, contact_id):
        url = urljoin(BASE_HTTP_URL, 'messages/%i' % contact_id)
        request = _get(url, headers=self._headers)
        return request.json()

    def watch_messages(self, contact_id, callback):
        self._api.socket_listener.watch(callback,
                                        "ConversationMessageReceivedEvent",
                                        contact_id=contact_id)

    def send(self, contact_id, message):
        url = urljoin(BASE_HTTP_URL, 'messages/%s' % contact_id)
        _post(url, headers=self._headers, json={'text': message})
