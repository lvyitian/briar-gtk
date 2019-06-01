# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md


class Model:

    _headers = {}

    def __init__(self, api):
        self._api = api
        self._initialize_headers()

    def _initialize_headers(self):
        self._headers['Authorization'] = 'Bearer %s' % self._api.auth_token
