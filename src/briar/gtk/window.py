# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gtk

from briar.gtk.containers.chat import ChatContainer
from briar.gtk.containers.main import MainContainer
from briar.gtk.containers.startup import StartupContainer
from briar.gtk.define import App, APPLICATION_ID, APPLICATION_NAME
from briar.gtk.toolbar import Toolbar


class Window(Gtk.ApplicationWindow):

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self, application=App(),
                                       title=APPLICATION_NAME,
                                       icon_name=APPLICATION_ID)
        self._setup_content()

    @property
    def container(self):
        return self._container

    @property
    def toolbar(self):
        return self._toolbar

    def _setup_content(self):
        self._setup_size((600, 400))  # TODO: do properly (constants, save)
        self._setup_toolbar()
        self._setup_grid()
        self._setup_startup_container()

    def _setup_size(self, size):
        if len(size) == 2 and\
           isinstance(size[0], int) and\
           isinstance(size[1], int):
            self.resize(size[0], size[1])

    def _setup_toolbar(self):
        self._toolbar = Toolbar()
        self._toolbar.show()
        self._toolbar.set_show_close_button(True)
        self.set_titlebar(self._toolbar)

    def _setup_grid(self):
        self._grid = Gtk.Grid()
        self._grid.set_orientation(Gtk.Orientation.HORIZONTAL)
        self._grid.show()
        self.add(self._grid)

    def _setup_startup_container(self):
        self._container = StartupContainer()
        self._container.show()
        self._container.connect("briar_startup_completed",
                                self._on_startup_completed)
        self._grid.add(self._container)

    # TODO: remove unused arguments
    # pylint: disable=unused-argument
    def _on_startup_completed(self, inst, obj):
        self._grid.destroy()
        self._setup_grid()
        self._setup_main_container()

    def _setup_main_container(self):
        self._container = MainContainer()
        self._container.show()
        self._grid.add(self._container)

    def open_private_chat(self, contact_id):
        self._grid.destroy()
        self._setup_grid()
        self._setup_private_chat(contact_id)

    def _setup_private_chat(self, contact_id):
        self._container = ChatContainer(contact_id)
        self._container.show()
        self._grid.add(self._container)
        self._toolbar.show_back_button(True, self._back_to_main)

    def _back_to_main(self, widget):
        self._grid.destroy()
        self._setup_grid()
        self._toolbar.show_back_button(False)
        self._setup_main_container()
