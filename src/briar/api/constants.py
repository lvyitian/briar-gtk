# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from os.path import join
from pathlib import Path
from urllib.parse import urljoin

_BRIAR_DIR = ".briar"

_HOST = "%s://localhost:7000"
_VERSION_SUFFIX = "v1/"

BRIAR_AUTH_TOKEN = join(Path.home(), _BRIAR_DIR, "auth_token")
BRIAR_DB = join(Path.home(), _BRIAR_DIR, "db", "db.mv.db")

BASE_HTTP_URL = urljoin(_HOST % "http", _VERSION_SUFFIX)
WEBSOCKET_URL = urljoin(_HOST % "ws", "%s/ws" % _VERSION_SUFFIX)
