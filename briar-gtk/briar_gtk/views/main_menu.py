# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import os

from gi.repository import Gtk

from briar_gtk.define import RESOURCES_DIR


class MainMenuView():

    MAIN_MENU_UI = "main_menu.ui"

    def __init__(self):
        self._builder = Gtk.Builder()

    def _add_from_resource(self, ui_filename):
        self._builder.add_from_resource(
            os.path.join(RESOURCES_DIR, ui_filename)
        )

    def _setup_view(self):
        self._add_from_resource(self.MAIN_MENU_UI)
        self._builder.connect_signals(self)
