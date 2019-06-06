# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import json
import requests_mock
from unittest import mock, TestCase

from briar.api.models.contacts import Contacts


class TestContacts(TestCase):

    @requests_mock.Mocker()
    def test_get(self, requests_mock):
        api = mock.Mock()
        contacts = Contacts(api)
        response_mock = {}
        response_mock["author"] = {}
        response_mock["author"]["formatVersion"] = 1
        response_mock["author"]["id"] = "y1wkIzAimAbYoCGgWxkWlr6vnq1F8t1QRA/UMPgI0E0="
        response_mock["author"]["name"] = "Test"
        response_mock["author"]["publicKey"] = "BDu6h1S02bF4W6rgoZfZ6BMjTj/9S9hNN7EQoV05qUo="
        response_mock["contactId"] = 1
        response_mock["alias"] = "A local nickname"
        response_mock["handshakePublicKey"] = "XnYRd7a7E4CTqgAvh4hCxh/YZ0EPscxknB9ZcEOpSzY="
        response_mock["verified"] = True

        requests_mock.get("http://localhost:7000/v1/contacts", text=json.dumps(response_mock))
        self.assertEqual(contacts.get(), response_mock)
