# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import os

from gi.repository import Gtk

from briar_gtk.define import RESOURCES_DIR


class PrivateChatView():

    def __init__(self, builder):
        self._builder = builder
        self._setup_view()

    def _setup_view(self):
        contact_name_label = self._builder.get_object("contact_name")
        contact_name_label.set_text("")
