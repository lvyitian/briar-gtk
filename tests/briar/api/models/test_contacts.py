# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import json
from random import choice
import requests_mock
from string import ascii_letters, digits
from unittest import mock

import pytest

from briar.api.models.contacts import Contacts


@requests_mock.Mocker(kw='requests_mock')
def test_get_empty(api, request_headers, requests_mock):
    contacts = Contacts(api)
    response = []

    requests_mock.register_uri("GET", "http://localhost:7000/v1/contacts",
                               request_headers=request_headers,
                               text=json.dumps(response))
    assert contacts.get() == response


@pytest.fixture
def api(auth_token):
    api = mock.Mock()
    api.auth_token = auth_token
    return api


@pytest.fixture
def request_headers(auth_token):
    request_headers = {
        "Authorization": 'Bearer %s' % auth_token
        }
    return request_headers


@pytest.fixture
def auth_token():
    return ''.join(choice(ascii_letters + digits) for i in range(33))
