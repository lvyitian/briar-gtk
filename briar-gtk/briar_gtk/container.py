# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository.Gtk import Builder, Overlay

from briar_gtk.define import RESOURCES_DIR


class Container(Overlay):

    def __init__(self):
        super().__init__()
        self.builder = Builder()

    def _add_from_resource(self, ui_filename):
        self.builder.add_from_resource(RESOURCES_DIR + ui_filename)
