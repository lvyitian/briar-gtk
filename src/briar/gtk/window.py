# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.gtk.container import Container
from briar.gtk.define import App

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib


class Window(Gtk.ApplicationWindow):

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self,
                                       application=App(),
                                       title="Briar",
                                       icon_name="app.briar.gtk")
        self.__setup_content()

    @property
    def container(self):
        return self.__container

    def __setup_content(self):
        self.__container = Container()
        self.__container.show()
        self.__container.set_hexpand(True)
        self.__container.set_vexpand(True)
        self.__vgrid = Gtk.Grid()
        self.__vgrid.set_orientation(Gtk.Orientation.VERTICAL)
        self.__vgrid.show()
        self.__vgrid.add(self.__container)
        self.add(self.__vgrid)
        self.__setup_size((800, 600))

    def __setup_size(self, size):
        if len(size) == 2 and\
           isinstance(size[0], int) and\
           isinstance(size[1], int):
            self.resize(size[0], size[1])

