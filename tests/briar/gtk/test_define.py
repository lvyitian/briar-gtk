# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from unittest import TestCase

from gi.repository import Gio

from briar.gtk.define import App


class TestDefine(TestCase):

    def test_app(self):
        assert App == Gio.Application.get_default
