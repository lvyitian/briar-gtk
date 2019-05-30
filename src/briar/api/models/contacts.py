# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.models.model import Model

import requests


class Contacts (Model):

    def get(self):
        r = requests.get(self.constants.get_base_url())
        print(r.status_code)
