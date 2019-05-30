# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from os.path import join
from pathlib import Path
from urllib.parse import urljoin


class Constants:

    _BRIAR_AUTH_TOKEN = 'auth_token'
    _BRIAR_DIR = '.briar'

    _HOST = 'http://localhost:7000'
    _VERSION_SUFFIX = 'v1'

    def get_auth_token(self):
        return join(Path.home(), self._BRIAR_DIR, self._BRIAR_AUTH_TOKEN)

    def get_base_url(self):
        return urljoin(self._HOST, self._VERSION_SUFFIX)
