# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from urllib.parse import urljoin

from requests import get as _get

from briar.api.constants import BASE_HTTP_URL
from briar.api.model import Model


# TODO: remove pylint disable once we have more methods
class Contacts(Model):  # pylint: disable=too-few-public-methods

    def get(self):
        url = urljoin(BASE_HTTP_URL, 'contacts')
        request = _get(url, headers=self._headers)
        return request.json()
