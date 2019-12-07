# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import GLib

from briar.gtk.container import Container
from briar.gtk.define import APP


class StartupContainer(Container):

    SETUP_UI = "/app/briar/gtk/ui/setup.ui"
    LOGIN_UI = "/app/briar/gtk/ui/login.ui"

    def __init__(self):
        super().__init__()
        self._api = APP().api
        self._setup_view()

    # pylint: disable=unused-argument
    def on_username_button_clicked(self, button):
        self.builder.get_object("username_grid").set_visible(False)
        self.builder.get_object("password_grid").set_visible(True)
        self.username = self.builder.get_object("username_entry").get_text()

    # pylint: disable=unused-argument
    def on_password_button_clicked(self, button):
        password = self.builder.get_object("password_entry").get_text()
        password_confirm = self.builder.get_object(
            "password_confirm_entry").get_text()
        if password != password_confirm:
            raise Exception("Passwords do not match")
        self._api.register((self.username, password),
                           StartupContainer._startup_completed)

    # pylint: disable=unused-argument
    def on_login_pressed(self, button):
        password = self.builder.get_object("password_entry").get_text()
        self._api.login(password, StartupContainer._startup_completed)

    def _setup_view(self):
        self.set_hexpand(True)
        self.set_vexpand(True)
        if not APP().api.has_account():
            self.builder.add_from_resource(self.SETUP_UI)
            self.add(self.builder.get_object("setup"))
        else:
            self.builder.add_from_resource(self.LOGIN_UI)
            self.add(self.builder.get_object("login"))
        self.builder.connect_signals(self)

    @staticmethod
    def _startup_completed(succeeded):
        if succeeded:
            GLib.idle_add(APP().window.on_startup_completed)
            return
        print("Startup failed")
