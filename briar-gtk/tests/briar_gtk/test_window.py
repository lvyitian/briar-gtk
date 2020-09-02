# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import pytest

from briar_gtk.window import Window

MODULE = "briar_gtk.window.%s"


def test_default_resize_at_init(mocker, startup_container, window_actions,
                                window_add, window_resize):
    Window()

    window_resize.assert_called_once_with(900, 600)


def test_startup_container_at_init(mocker, startup_container, window_actions,
                                   window_add, window_resize):
    window = Window()

    startup_container.assert_called_once_with(window)
    window.current_container.show_all.assert_called_once()


def test_window_actions_at_init(mocker, startup_container, window_actions,
                                window_add, window_resize):
    Window()

    window_actions.assert_called_once()


def test_window_add_at_init(mocker, startup_container, window_actions,
                            window_add, window_resize):
    window = Window()

    window_add.assert_called_once_with(window.current_container)


def test_show_main_container(main_window_container, mocker,
                             startup_container, window_actions,
                             window_add, window_resize):
    Window().show_main_container()

    main_window_container.assert_called_once()


def test_show_main_shown(main_window_container, mocker,
                         startup_container, window_actions,
                         window_add, window_resize):
    window = Window()

    window.show_main_container()

    window.current_container.show_all.assert_called_once()


def test_show_main_add(main_window_container, mocker,
                       startup_container, window_actions,
                       window_add, window_resize):
    window = Window()
    window_add = mocker.patch(MODULE % "Window.add")

    window.show_main_container()

    window_add.assert_called_once_with(window.current_container)


def test_show_main_destroy_old(main_window_container, mocker,
                               startup_container, window_actions,
                               window_add, window_resize):
    window = Window()
    current_container_mock = mocker.MagicMock()
    window.current_container = current_container_mock

    window.show_main_container()

    current_container_mock.destroy.assert_called_once()


@pytest.fixture(autouse=True)
def briar_headless_jar(is_file):
    flatpak_path = "/app/share/java/briar-headless.jar"
    return_values = {flatpak_path: True}
    is_file.side_effect = return_values.get
    return is_file


# For some reason, this gives a '6681 Segmentation fault'. Therefore 'False'
@pytest.fixture(autouse=False)
def gi_dependencies(mocker):
    mocker.patch(MODULE % "Gtk")


@pytest.fixture()
def startup_container(mocker):
    return mocker.patch(MODULE % "StartupContainer")


@pytest.fixture()
def main_window_container(mocker):
    return mocker.patch(MODULE % "MainWindowContainer")


@pytest.fixture()
def window_actions(mocker):
    return mocker.patch(MODULE % "WindowActions")


@pytest.fixture()
def window_add(mocker):
    return mocker.patch(MODULE % "Window.add")


@pytest.fixture()
def window_resize(mocker):
    return mocker.patch(MODULE % "Window.resize")
