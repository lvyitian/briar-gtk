# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.gtk.containers.chat import ChatContainer
from briar.gtk.containers.main import MainContainer
from briar.gtk.containers.startup import StartupContainer
from briar.gtk.define import App

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib


class Window(Gtk.ApplicationWindow):

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self, application=App(), title="Briar",
                                       icon_name="app.briar.gtk")
        self.__setup_content()

    @property
    def container(self):
        return self.__container

    def __setup_content(self):
        self.__setup_size((600, 400))  # TODO: do properly (constants, save)
        self.__setup_grid()
        self.__setup_startup_container()

    def __setup_size(self, size):
        if len(size) == 2 and\
           isinstance(size[0], int) and\
           isinstance(size[1], int):
            self.resize(size[0], size[1])

    def __setup_grid(self):
        self.__grid = Gtk.Grid()
        self.__grid.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.__grid.show()
        self.add(self.__grid)

    def __setup_startup_container(self):
        self.__container = StartupContainer()
        self.__container.show()
        self.__container.connect("briar_startup_completed",
                                 self.__on_startup_completed)
        self.__grid.add(self.__container)

    def __on_startup_completed(self, inst, obj):
        self.__grid.destroy()
        self.__setup_grid()
        self.__setup_main_container()

    def __setup_main_container(self):
        self.__container = MainContainer()
        self.__container.show()
        self.__grid.add(self.__container)

    def open_private_chat(self, contact_id):
        self.__grid.destroy()
        self.__setup_grid()
        self.__setup_private_chat(contact_id)

    def __setup_private_chat(self, contact_id):
        self.__container = ChatContainer(contact_id)
        self.__container.show()
        self.__grid.add(self.__container)

