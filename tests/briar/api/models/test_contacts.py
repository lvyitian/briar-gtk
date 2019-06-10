# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import json
import requests_mock
from unittest import mock, TestCase

from briar.api.models.contacts import Contacts


class TestContacts(TestCase):

    # TODO: randomly generate token
    AUTH_TOKEN = "xxhQhFNdq5R2YcipNcT3uYoMyOT2PxBl3tpWiO5Qy65w="

    @requests_mock.Mocker()
    def test_get_empty(self, requests_mock):
        api = TestContacts._get_mocked_api()
        request_headers = TestContacts._get_mocked_request_headers()

        contacts = Contacts(api)
        response = list()

        requests_mock.register_uri("GET", "http://localhost:7000/v1/contacts",
                                   request_headers=request_headers,
                                   text=json.dumps(response))
        assert contacts.get() == response

    # TODO: Use pytest fixtures
    def _get_mocked_api():
        api = mock.Mock()
        api.auth_token = TestContacts.AUTH_TOKEN
        return api

    # TODO: Use pytest fixtures
    def _get_mocked_request_headers():
        request_headers = {}
        authorization_header = 'Bearer %s' % TestContacts.AUTH_TOKEN
        request_headers["Authorization"] = authorization_header
        return request_headers
