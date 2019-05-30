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
        self._setup_view()
        self._register_signals()
        self._api = App().api

    def on_username_button_clicked(self, button):
        self.builder.get_object("username_grid").set_visible(False)
        self.builder.get_object("password_grid").set_visible(True)
        self.username = self.builder.get_object("username_entry").get_text()

    def on_password_button_clicked(self, button):
        password = self.builder.get_object("password_entry").get_text()
        password_confirm = self.builder.get_object("password_confirm_entry").get_text()
        if password != password_confirm:
            raise Exception("Passwords do not match")
        self._api.register((self.username, password), self._startup_finished)

    def on_login_pressed(self, button):
        password = self.builder.get_object("password_entry").get_text()
        self._api.login(password, self._startup_finished)

    def _setup_view(self):
        self.set_hexpand(True)
        self.set_vexpand(True)
        if not App().api.has_account():
            self.builder.add_from_resource("/app/briar/gtk/ui/setup.ui")
            self.add(self.builder.get_object("setup"))
        else:
            self.builder.add_from_resource("/app/briar/gtk/ui/login.ui")
            self.add(self.builder.get_object("login"))
        self.builder.connect_signals(self)

    def _register_signals(self):
        GObject.signal_new("briar_startup_completed", Gtk.Overlay,
                           GObject.SignalFlags.RUN_LAST, GObject.TYPE_BOOLEAN,
                           (GObject.TYPE_STRING,))

    def _startup_finished(self, succeeded):
        if succeeded:
            print("Startup succeeded")
            self.emit("briar_startup_completed", (succeeded,))
            return
        print("Startup failed")
