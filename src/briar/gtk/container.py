# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository.Gtk import Builder, Overlay


class Container(Overlay):

    def __init__(self):
        super().__init__()
        self.builder = Builder()
