# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.constants import BASE_HTTP_URL
from briar.api.models.model import Model

from requests import get as _get
from urllib.parse import urljoin


class Contacts(Model):

    def get(self):
        url = urljoin(BASE_HTTP_URL, 'contacts')
        r = _get(url, headers=self._headers)
        return r.json()
