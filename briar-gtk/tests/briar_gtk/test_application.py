# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import pytest

from briar_gtk.application import Application

MODULE = "briar_gtk.application.%s"


def test_application_actions_at_init(mocker):
    application_actions_mock = mocker.patch(
        MODULE % "ApplicationActions")

    application = Application()

    application_actions_mock.assert_called_once_with(application)


def test_application_name_at_init(mocker):
    application_name_mock = mocker.patch(
        MODULE % "GLib.set_application_name")
    prgname_mock = mocker.patch(
        MODULE % "GLib.set_prgname")

    application = Application()

    application_name_mock.assert_called_once_with("Briar")
    prgname_mock.assert_called_once_with("Briar")


def test_api_at_startup(mocker):
    api_mock = mocker.patch(MODULE % "Api")

    Application().do_startup()

    api_mock.assert_called_once_with("/app/share/java/briar-headless.jar")


def test_css_provider_at_startup(mocker):
    css_provider_mock = mocker.patch(MODULE % "Gtk.CssProvider")

    Application().do_startup()

    css_provider_mock.assert_called_once()


def test_handy_at_startup(mocker):
    handy_mock = mocker.patch(MODULE % "Handy.init")

    Application().do_startup()

    handy_mock.assert_called_once()


def test_startup_at_startup(mocker):
    do_startup_mock = mocker.patch(MODULE % "Gtk.Application.do_startup")

    application = Application()

    application.do_startup()

    do_startup_mock.assert_called_once_with(application)


def test_style_context_at_startup(mocker):
    style_context_mock = mocker.patch(MODULE % "Gtk.StyleContext")

    Application().do_startup()

    style_context_mock.assert_called_once()


def test_window_at_activate(mocker):
    window_mock = mocker.patch(MODULE % "Window")

    Application().do_activate()

    window_mock.assert_called_once()


def test_already_window_at_activate(mocker):
    gtk_window_mock = mocker.patch(MODULE % "Window")
    window_mock = mocker.MagicMock()

    application = Application()
    application.window = window_mock

    application.do_activate()

    window_mock.present.assert_called_once()
    assert gtk_window_mock.called is False


def test_api_stop_at_shutdown(mocker):
    api_mock = mocker.patch(MODULE % "Api")

    application = Application()
    application.api = api_mock
    application.window = mocker.MagicMock()

    application.do_shutdown()

    api_mock.stop.assert_called_once()


def test_window_hide_at_shutdown(mocker):
    window_mock = mocker.patch(MODULE % "Window")

    application = Application()
    application.api = mocker.MagicMock()
    application.window = window_mock

    application.do_shutdown()

    window_mock.hide.assert_called_once()


@pytest.fixture(autouse=True)
def briar_headless_jar(is_file):
    flatpak_path = "/app/share/java/briar-headless.jar"
    return_values = {flatpak_path: True}
    is_file.side_effect = return_values.get
    return is_file


@pytest.fixture(autouse=True)
def gi_dependencies(mocker):
    gi_dependencies = ('Gdk', 'Gio', 'GLib', 'Gtk', 'Handy')
    for dependency in gi_dependencies:
        mocker.patch(MODULE % dependency)
