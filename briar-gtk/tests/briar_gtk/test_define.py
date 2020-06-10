# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import pytest

from briar_gtk.define import get_briar_headless_jar


def test_headless_flatpak_path(is_file):
    flatpak_path = "/app/share/java/briar-headless.jar"
    return_values = {flatpak_path: True}
    is_file.side_effect = return_values.get

    assert get_briar_headless_jar() == flatpak_path
    is_file.assert_called_once_with(flatpak_path)


def test_headless_debian_path(is_file):
    debian_path = "/usr/share/java/briar-headless.jar"
    return_values = {debian_path: True}
    is_file.side_effect = return_values.get

    assert get_briar_headless_jar() == debian_path
    is_file.assert_called_with(debian_path)


def test_headless_local_path(is_file, mocker):
    local_path = "/home/alice/.local/share/java/briar-headless.jar"

    home_mock = mocker.patch('pathlib.Path.home')
    home_mock.return_value = "/home/alice"

    return_values = {local_path: True}
    is_file.side_effect = return_values.get

    assert get_briar_headless_jar() == local_path
    is_file.assert_called_with(local_path)


def test_headless_no_path(is_file):
    is_file.return_value = False

    with pytest.raises(FileNotFoundError,
                       match="Couldn't find briar-headless.jar"):
        get_briar_headless_jar()

    assert is_file.called is True
