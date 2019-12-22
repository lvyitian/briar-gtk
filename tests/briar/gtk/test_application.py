# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from unittest.mock import Mock

import pytest

from briar_wrapper.api import Api
from briar.gtk.application import Application
from briar.gtk.define import APPLICATION_NAME, APPLICATION_STYLING_PATH
from briar.gtk.define import BRIAR_HEADLESS_JAR
from briar.gtk.window import Window


def test_do_startup(mocker):
    do_startup_mock = mocker.patch("gi.repository.Gtk.Application.do_startup")
    _setup_styling_mock = mocker.patch(
        "briar.gtk.application.Application._setup_styling")
    _setup_api_mock = mocker.patch(
        "briar.gtk.application.Application._setup_api")

    Application().do_startup()

    do_startup_mock.assert_called_once()
    _setup_styling_mock.assert_called_once_with(APPLICATION_STYLING_PATH)
    _setup_api_mock.assert_called_once()


def test_do_activate(mocker):
    _setup_window_mock = mocker.patch(
        "briar.gtk.application.Application._setup_window")

    Application().do_activate()

    _setup_window_mock.assert_called_once()


def test_quit(mocker):
    api_mock = mocker.patch("briar_wrapper.api.Api")
    api_stop_mock = mocker.patch("briar_wrapper.api.Api.stop")
    window_mock = mocker.patch("briar.gtk.window.Window")
    window_hide_mock = mocker.patch("briar.gtk.window.Window.hide")
    quit_mock = mocker.patch("gi.repository.Gio.Application.quit")

    application = Application()
    application.api = api_mock
    application._window = window_mock

    application.quit()

    api_stop_mock.assert_called_once()
    window_hide_mock.assert_called_once()
    quit_mock.assert_called_once()


def test_set_application_name(mocker):
    set_application_name_mock = mocker.patch(
        "gi.repository.GLib.set_application_name")
    set_prgname_mock = mocker.patch("gi.repository.GLib.set_prgname")
    name_mock = "Mock"

    Application._set_application_name(name_mock)

    set_application_name_mock.assert_called_once_with(name_mock)
    set_prgname_mock.assert_called_once_with(name_mock)


def test_set_application_name_implicit(mocker):
    set_application_name_mock = mocker.patch(
        "gi.repository.GLib.set_application_name")
    set_prgname_mock = mocker.patch("gi.repository.GLib.set_prgname")

    Application()

    set_application_name_mock.assert_called_once_with(APPLICATION_NAME)
    set_prgname_mock.assert_called_once_with(APPLICATION_NAME)


def test_setup_styling(mocker):
    new_for_uri_mock = mocker.patch("gi.repository.Gio.File.new_for_uri")
    load_from_file_mock = mocker.patch(
        "gi.repository.Gtk.CssProvider.load_from_file")
    get_default_mock = mocker.patch("gi.repository.Gdk.Screen.get_default")
    add_provider_for_screen_mock = mocker.patch(
        "gi.repository.Gtk.StyleContext.add_provider_for_screen")

    Application._setup_styling(APPLICATION_STYLING_PATH)

    new_for_uri_mock.assert_called_with(APPLICATION_STYLING_PATH)
    load_from_file_mock.assert_called_once()
    get_default_mock.assert_called_once()
    add_provider_for_screen_mock.assert_called_once()


def test_setup_api(mocker):
    application = Application()

    assert not hasattr(application, "api")

    application._setup_api()

    assert isinstance(application.api, Api)
    assert application.api._command == ["java", "-jar", BRIAR_HEADLESS_JAR]


def test_setup_window(mocker):
    mocker.patch("briar.gtk.window.Window.__init__").return_value = None
    window_show_mock = mocker.patch("briar.gtk.window.Window.show")
    window_present_mock = mocker.patch("briar.gtk.window.Window.present")

    Application()._setup_window()

    window_show_mock.assert_called_once()
    window_present_mock.assert_called_once()


def test_setup_window_has_attribute(mocker):
    mocker.patch("briar.gtk.window.Window.__init__").return_value = None
    window_mock = Mock()

    application = Application()
    application._window = window_mock

    application._setup_window()

    window_mock.show.assert_not_called()
    window_mock.present.assert_called_once()


def test_setup_window_has_none_attribute(mocker):
    mocker.patch("briar.gtk.window.Window.__init__").return_value = None
    window_show_mock = mocker.patch("briar.gtk.window.Window.show")
    window_present_mock = mocker.patch("briar.gtk.window.Window.present")

    application = Application()

    application._setup_window()

    window_show_mock.assert_called_once()
    window_present_mock.assert_called_once()


@pytest.fixture(autouse=True)
def glib_set_application_name(mocker):
    mocker.patch("gi.repository.GLib.set_application_name")
