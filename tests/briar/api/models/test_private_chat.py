# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import json

import requests_mock

from briar.api.models.private_chat import PrivateChat



@requests_mock.Mocker(kw="requests_mock")
def test_get_empty(api, request_headers, requests_mock):
    private_chat = PrivateChat(api)
    contact_id = 1
    url = "http://localhost:7000/v1/messages/%s" % contact_id
    response = []

    requests_mock.register_uri("GET", url, request_headers=request_headers,
                               text=json.dumps(response))
    assert private_chat.get(contact_id) == response
