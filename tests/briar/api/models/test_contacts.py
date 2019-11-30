# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import json

import requests_mock

from briar.api.models.contacts import Contacts

BASE_HTTP_URL = "http://localhost:7000/v1/contacts/"

TEST_LINK = "briar://wvui4uvhbfv4tzo6xwngknebsxrafainnhldyfj63x6ipp4q2vigy"
TEST_ALIAS = "Alice"


@requests_mock.Mocker(kw="requests_mock")
def test_add_pending(api, request_headers, requests_mock):
    contacts = Contacts(api)

    requests_mock.register_uri("POST",
                               BASE_HTTP_URL + "add/pending/",
                               request_headers=request_headers,
                               additional_matcher=match_request_add_pending)
    contacts.add_pending(TEST_LINK, TEST_ALIAS)


@requests_mock.Mocker(kw='requests_mock')
def test_get_empty(api, request_headers, requests_mock):
    contacts = Contacts(api)
    response = []

    requests_mock.register_uri("GET", BASE_HTTP_URL,
                               request_headers=request_headers,
                               text=json.dumps(response))
    assert contacts.get() == response


@requests_mock.Mocker(kw='requests_mock')
def test_get_link(api, request_headers, requests_mock):
    contacts = Contacts(api)
    response = {"link": TEST_LINK}

    requests_mock.register_uri("GET", BASE_HTTP_URL + "add/link/",
                               request_headers=request_headers,
                               text=json.dumps(response))
    assert contacts.get_link() == TEST_LINK


def match_request_add_pending(request):
    return {"alias": TEST_ALIAS, "link": TEST_LINK} == request.json()
