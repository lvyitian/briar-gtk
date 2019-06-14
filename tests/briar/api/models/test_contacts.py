# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import json

import requests_mock

from briar.api.models.contacts import Contacts


@requests_mock.Mocker(kw='requests_mock')
def test_get_empty(api, request_headers, requests_mock):
    contacts = Contacts(api)
    response = []

    requests_mock.register_uri("GET", "http://localhost:7000/v1/contacts",
                               request_headers=request_headers,
                               text=json.dumps(response))
    assert contacts.get() == response
