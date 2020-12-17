# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import os

from gi.repository import Gtk

from briar_gtk.define import RESOURCES_DIR


class ChatMenuView():

    CHAT_MENU_UI = "chat_menu.ui"

    def __init__(self):
        self._builder = Gtk.Builder()

    def _add_from_resource(self, ui_filename):
        self._builder.add_from_resource(
            os.path.join(RESOURCES_DIR, ui_filename)
        )

    def _setup_view(self):
        self._add_from_resource(self.CHAT_MENU_UI)
        self._builder.connect_signals(self)
        self._builder.get_object("chat_menu_button").hide()
