# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gtk

from briar_gtk.actions.window import WindowActions
from briar_gtk.containers.add_contact import AddContactContainer
from briar_gtk.containers.main import MainContainer
from briar_gtk.containers.startup import StartupContainer
from briar_gtk.define import APP, APPLICATION_ID, APPLICATION_NAME


class Window(Gtk.ApplicationWindow, WindowActions):

    DEFAULT_WINDOW_SIZE = (900, 600)

    def __init__(self):
        self._initialize_gtk_application_window()
        WindowActions.__init__(self)
        self._setup_content()

    def show_main_container(self):
        self.current_container.destroy()
        self._setup_main_container()

    def show_add_contact_container(self):
        self.current_container.destroy()
        self._setup_add_contact_container()

    def _initialize_gtk_application_window(self):
        Gtk.ApplicationWindow.__init__(self, application=APP(),
                                       title=APPLICATION_NAME,
                                       icon_name=APPLICATION_ID)

    def _setup_content(self):
        self._resize_window(self.DEFAULT_WINDOW_SIZE)
        self._setup_startup_container()

    def _resize_window(self, size):
        if not Window._size_is_valid(size):
            raise Exception("Couldn't resize window; invalid size parameter")
        self.resize(size[0], size[1])

    @staticmethod
    def _size_is_valid(size):
        return len(size) == 2 and\
               isinstance(size[0], int) and\
               isinstance(size[1], int)

    def _setup_container(self, container):
        self.current_container = container
        self.current_container.show_all()
        self.add(self.current_container)

    def _setup_startup_container(self):
        self._setup_container(StartupContainer(self))

    def _setup_main_container(self):
        self._setup_container(MainContainer())

    def _setup_add_contact_container(self):
        self._setup_container(AddContactContainer())
