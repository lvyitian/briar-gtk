# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import os

import pytest

from briar_gtk.container import Container

MODULE = "briar_gtk.container.%s"


@pytest.mark.skipif('CI' in os.environ, reason='segmentation fault')
def test_builder_at_init(mocker):
    builder_mock = mocker.patch(
        MODULE % "Gtk.Builder")

    Container()

    builder_mock.assert_called_once()


@pytest.fixture(autouse=True)
def briar_headless_jar(is_file):
    flatpak_path = "/app/share/java/briar-headless.jar"
    return_values = {flatpak_path: True}
    is_file.side_effect = return_values.get
    return is_file


@pytest.fixture(autouse=True)
def gi_dependencies(mocker):
    mocker.patch(MODULE % "Gtk")
