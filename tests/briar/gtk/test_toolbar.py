# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import pytest
from unittest.mock import Mock

from briar.gtk.toolbar import Toolbar


def test_show_back_button(mocker):
    get_object_mock = mocker.patch("gi.repository.Gtk.Builder.get_object")
    back_button_mock = get_object_mock.return_value
    callback = Mock()
    mocker.patch("briar.gtk.toolbar.Toolbar._setup_toolbar")

    Toolbar().show_back_button(True, callback)

    get_object_mock.assert_called_once_with("back_button")
    back_button_mock.hide.assert_not_called()
    back_button_mock.show.assert_called_once()
    back_button_mock.connect.assert_called_once()


def test_show_back_button_without_callback(mocker):
    get_object_mock = mocker.patch("gi.repository.Gtk.Builder.get_object")
    back_button_mock = get_object_mock.return_value
    mocker.patch("briar.gtk.toolbar.Toolbar._setup_toolbar")

    with pytest.raises(Exception,
                       match="Callback needed when showing back button"):
        Toolbar().show_back_button(True)

    get_object_mock.assert_called_once_with("back_button")
    back_button_mock.hide.assert_not_called()
    back_button_mock.show.assert_not_called()
    back_button_mock.connect.assert_not_called()


def test_hide_back_button(mocker):
    get_object_mock = mocker.patch("gi.repository.Gtk.Builder.get_object")
    back_button_mock = get_object_mock.return_value
    mocker.patch("briar.gtk.toolbar.Toolbar._setup_toolbar")

    Toolbar().show_back_button(False)

    get_object_mock.assert_called_once_with("back_button")
    back_button_mock.hide.assert_called_once()
    back_button_mock.show.assert_not_called()
    back_button_mock.connect.assert_not_called()
