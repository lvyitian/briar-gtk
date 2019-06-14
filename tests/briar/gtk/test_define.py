# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gio

from briar.gtk.define import App


def test_app():
    assert App == Gio.Application.get_default
