# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository.Gtk import ApplicationWindow, Grid

from briar.gtk.containers.add_contact import AddContactContainer
from briar.gtk.containers.chat import ChatContainer
from briar.gtk.containers.main import MainContainer
from briar.gtk.containers.startup import StartupContainer
from briar.gtk.define import APP, APPLICATION_ID, APPLICATION_NAME
from briar.gtk.toolbar import Toolbar


class Window(ApplicationWindow):

    DEFAULT_WINDOW_SIZE = (600, 400)

    def __init__(self):
        self._initialize_gtk_application_window()
        self._setup_content()

    @property
    def container(self):
        return self._container

    @property
    def toolbar(self):
        return self._toolbar

    def _initialize_gtk_application_window(self):
        ApplicationWindow.__init__(self, application=APP(),
                                   title=APPLICATION_NAME,
                                   icon_name=APPLICATION_ID)

    def _setup_content(self):
        self._setup_size(self.DEFAULT_WINDOW_SIZE)
        self._setup_startup_container()

    def _setup_size(self, size):
        if Window._size_is_valid(size):
            self.resize(size[0], size[1])

    @staticmethod
    def _size_is_valid(size):
        return len(size) == 2 and\
               isinstance(size[0], int) and\
               isinstance(size[1], int)

    def _setup_startup_container(self):
        self._container = StartupContainer(self)
        self._container.show()
        self.add(self._container)

    def on_startup_completed(self):
        self._container.destroy()
        self._setup_grid()
        self._setup_toolbar()
        self._setup_main_container()

    def _setup_grid(self):
        self._grid = Grid()
        self._grid.show()
        self.add(self._grid)

    def _reset_window(self):
        self._container.destroy()
        self._grid.destroy()
        self._setup_grid()
        self._setup_toolbar()

    def _setup_toolbar(self):
        self._toolbar = Toolbar()
        self._toolbar.show()
        self._toolbar.set_show_close_button(True)
        self.set_titlebar(self._toolbar)

    def _setup_main_container(self):
        self._container = MainContainer()
        self._container.show()
        self._grid.add(self._container)
        self._toolbar.show_add_contact_button(True, self.show_add_contact)

    # pylint: disable=unused-argument
    def show_add_contact(self, widget):
        self._setup_add_contact()

    def _setup_add_contact(self):
        self._grid.destroy()
        self._container = AddContactContainer(self)
        self._container.show()
        self.add(self._container)

    def open_private_chat(self, contact_id):
        self._reset_window()
        self._setup_private_chat(contact_id)

    def _setup_private_chat(self, contact_id):
        self._container = ChatContainer(contact_id)
        self._container.show()
        self._grid.add(self._container)
        self._toolbar.show_back_button(True, self.back_to_main)
        self._toolbar.show_add_contact_button(False)

    # pylint: disable=unused-argument
    def back_to_main(self, widget):
        self._reset_window()
        self._toolbar.show_back_button(False)
        self._setup_main_container()
