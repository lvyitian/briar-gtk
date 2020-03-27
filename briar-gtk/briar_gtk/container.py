# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import os

from gi.repository import Gtk

from briar_gtk.define import RESOURCES_DIR


class Container(Gtk.Overlay):

    def __init__(self):
        super().__init__()
        self.builder = Gtk.Builder()

    def _add_from_resource(self, ui_filename):
        self.builder.add_from_resource(os.path.join(RESOURCES_DIR, ui_filename))
