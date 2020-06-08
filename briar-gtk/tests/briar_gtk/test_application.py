# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from unittest.mock import Mock

import pytest

from briar_wrapper.api import Api

from briar_gtk.application import Application
from briar_gtk.define import APPLICATION_NAME, APPLICATION_STYLING_PATH
from briar_gtk.define import BRIAR_HEADLESS_JAR
from briar_gtk.window import Window


def test_do_startup(mocker):
    do_startup_mock = mocker.patch("gi.repository.Gtk.Application.do_startup")
    _setup_styling_mock = mocker.patch(
        "briar_gtk.application.Application._setup_styling")
    _setup_api_mock = mocker.patch(
        "briar_gtk.application.Application._setup_api")

    Application().do_startup()

    do_startup_mock.assert_called_once()
    _setup_styling_mock.assert_called_once_with(APPLICATION_STYLING_PATH)
    _setup_api_mock.assert_called_once()


def test_do_activate(mocker):
    _setup_window_mock = mocker.patch(
        "briar_gtk.application.Application._setup_window")

    Application().do_activate()

    _setup_window_mock.assert_called_once()


def test_do_shutdown(mocker):
    api_mock = mocker.patch("briar_wrapper.api.Api")
    api_stop_mock = mocker.patch("briar_wrapper.api.Api.stop")
    window_mock = mocker.patch("briar_gtk.window.Window")
    window_hide_mock = mocker.patch("briar_gtk.window.Window.hide")
    do_shutdown_mock = mocker.patch(
        "gi.repository.Gio.Application.do_shutdown")

    application = Application()
    application.api = api_mock
    application.window = window_mock

    application.do_shutdown()

    api_stop_mock.assert_called_once()
    window_hide_mock.assert_called_once()
    do_shutdown_mock.assert_called_once()
