# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from urllib.parse import urljoin

from requests import get as _get
from requests import post as _post

from briar.api.constants import BASE_HTTP_URL
from briar.api.model import Model


class Contacts(Model):

    API_ENDPOINT = "contacts/"

    _on_contact_added_callback = None

    def add_pending(self, link, alias):
        url = urljoin(BASE_HTTP_URL, self.API_ENDPOINT + "add/" + "pending/")
        _post(url, headers=self._headers, json={"link": link, "alias": alias})

    def get(self):
        url = urljoin(BASE_HTTP_URL, self.API_ENDPOINT)
        request = _get(url, headers=self._headers)
        return request.json()

    def get_link(self):
        url = urljoin(BASE_HTTP_URL, self.API_ENDPOINT + "add/" + "link/")
        request = _get(url, headers=self._headers).json()
        return request['link']

    def watch_contacts(self, callback):
        self._on_contact_added_callback = callback
        self._api.socket_listener.watch("ContactAddedEvent",
                                        self._on_contact_added)

    # pylint: disable=unused-argument
    def _on_contact_added(self, event):
        self._on_contact_added_callback()
