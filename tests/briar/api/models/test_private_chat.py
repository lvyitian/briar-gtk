# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import json

import requests_mock

from briar.api.models.private_chat import PrivateChat

BASE_HTTP_URL = "http://localhost:7000/v1/messages/%s"

TEST_CONTACT_ID = 42
TEST_TEXT = "Hello World"


@requests_mock.Mocker(kw="requests_mock")
def test_get_empty(api, request_headers, requests_mock):
    private_chat = PrivateChat(api)
    url = BASE_HTTP_URL % TEST_CONTACT_ID
    response = []

    requests_mock.register_uri("GET", url, request_headers=request_headers,
                               text=json.dumps(response))
    assert private_chat.get(TEST_CONTACT_ID) == response


@requests_mock.Mocker(kw="requests_mock")
def test_send_message(api, request_headers, requests_mock):
    private_chat = PrivateChat(api)
    url = BASE_HTTP_URL % TEST_CONTACT_ID

    requests_mock.register_uri("POST", url, request_headers=request_headers,
                               additional_matcher=match_request_send_message)
    private_chat.send(TEST_CONTACT_ID, TEST_TEXT)


def match_request_send_message(request):
    return {"text": TEST_TEXT} == request.json()
