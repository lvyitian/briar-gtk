# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from random import choice
from string import ascii_letters, digits
from unittest import mock

import pytest

# pylint: disable=redefined-outer-name


@pytest.fixture
def api(auth_token):
    api = mock.Mock()
    api.auth_token = auth_token
    return api


@pytest.fixture
def auth_token():
    return ''.join(choice(ascii_letters + digits) for i in range(33))


@pytest.fixture
def request_headers(auth_token):
    request_headers = {
        "Authorization": 'Bearer %s' % auth_token
    }
    return request_headers
