# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from os.path import join
from pathlib import Path
from unittest import TestCase

from briar.api.constants import BASE_HTTP_URL, BRIAR_AUTH_TOKEN
from briar.api.constants import BRIAR_DB, WEBSOCKET_URL


class TestConstants(TestCase):

    def test_base_http_url(self):
        assert BASE_HTTP_URL == "http://localhost:7000/v1/"

    def test_briar_auth_token(self):
        briar_dir = TestConstants._get_briar_dir()
        assert BRIAR_AUTH_TOKEN == join(briar_dir, "auth_token")

    def test_briar_db(self):
        briar_dir = TestConstants._get_briar_dir()
        assert BRIAR_DB == join(briar_dir, "db", "db.mv.db")

    def test_websocket_url(self):
        assert WEBSOCKET_URL == "ws://localhost:7000/v1/ws"

    # TODO: Use pytest fixtures
    def _get_briar_dir():
        return join(str(Path.home()), ".briar")
