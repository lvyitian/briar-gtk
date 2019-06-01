# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.models.model import Model
from briar.api.models.socket_listener import SocketListener

from requests import get as _get
from urllib.parse import urljoin


class PrivateChat(Model):

    def get(self, contact_id):
        headers = {'Authorization': 'Bearer ' + self._api.auth_token}
        url = urljoin(self._constants.get_base_url(), 'messages/' + contact_id)
        r = _get(url, headers=headers)
        return r.json()

    def watch_messages(self, contact_id, callback):
        socket_listener = SocketListener(self._api)
        socket_listener.watch(callback, "ConversationMessageReceivedEvent",
                              contact_id=contact_id)
