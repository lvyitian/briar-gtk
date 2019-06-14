# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from os.path import join
from pathlib import Path

import pytest

from briar.api.constants import BASE_HTTP_URL, BRIAR_AUTH_TOKEN
from briar.api.constants import BRIAR_DB, WEBSOCKET_URL


def test_base_http_url():
    assert BASE_HTTP_URL == "http://localhost:7000/v1/"


def test_briar_auth_token(briar_dir):
    assert BRIAR_AUTH_TOKEN == join(briar_dir, "auth_token")


def test_briar_db(briar_dir):
    assert BRIAR_DB == join(briar_dir, "db", "db.mv.db")


def test_websocket_url():
    assert WEBSOCKET_URL == "ws://localhost:7000/v1/ws"


@pytest.fixture
def briar_dir():
    return join(str(Path.home()), ".briar")
