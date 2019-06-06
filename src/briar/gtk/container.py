# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gtk


class Container(Gtk.Overlay):

    def __init__(self):
        Gtk.Overlay.__init__(self)
        self.builder = Gtk.Builder()
        self.__setup_view()
        self.__register_signals()

    def __setup_view(self):
        pass

    def __register_signals(self):
        pass
