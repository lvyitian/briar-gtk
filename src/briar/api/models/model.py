# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md


class Model:

    def __init__(self, api):
        self._api = api
        self.constants = api.constants
