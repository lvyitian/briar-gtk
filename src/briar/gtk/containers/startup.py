# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.gtk.container import Container
from briar.gtk.define import App

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk


class StartupContainer(Container):

    def __init__(self):
        super().__init__()
        self.__setup_view()
        self.__register_signals()

    def on_username_button_clicked(self, button):
        self.builder.get_object("username_grid").set_visible(False)
        self.builder.get_object("password_grid").set_visible(True)
        self.username = self.builder.get_object("username_entry").get_text()

    def on_password_button_clicked(self, button):
        password = self.builder.get_object("password_entry").get_text()
        App().api.register((self.username, password),
                           self.__startup_completed)

    def on_login_pressed(self, button):
        password = self.builder.get_object("password_entry").get_text()
        App().api.login(password, self.__startup_completed)

    def __setup_view(self):
        self.set_hexpand(True)
        self.set_vexpand(True)
        if not App().api.has_account():
            self.builder.add_from_resource("/app/briar/gtk/ui/setup.ui")
            self.add(self.builder.get_object("setup"))
        else:
            self.builder.add_from_resource("/app/briar/gtk/ui/login.ui")
            self.add(self.builder.get_object("login"))
        self.builder.connect_signals(self)

    def __register_signals(self):
        GObject.signal_new("briar_startup_completed", Gtk.Overlay,
                           GObject.SignalFlags.RUN_LAST, GObject.TYPE_BOOLEAN,
                           (GObject.TYPE_STRING,))

    def __startup_completed(self, succeded=True):
        self.emit("briar_startup_completed", ("succeded",))
