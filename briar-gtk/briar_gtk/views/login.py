# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
import os
from gettext import gettext as _

from gi.repository import GLib, Gtk

from briar_gtk.actions.login import LoginActions
from briar_gtk.actions.prefixes import LOGIN_PREFIX
from briar_gtk.define import APP, RESOURCES_DIR


class LoginView(Gtk.Overlay):

    LOGIN_UI = "login.ui"
    STACK_NAME = "login_flow_stack"
    HEADERS_NAME = "login_flow_headers"

    def __init__(self, window):
        super().__init__()
        self.builder = Gtk.Builder()
        LoginActions(self)
        self._window = window
        self._setup_view()

    def on_login_pressed(self):
        if self._password_is_empty():
            self._show_error_message(_("Please enter a password"))
            return
        self._show_loading_animation()
        self._login()

    def _setup_view(self, ):
        self._add_from_resource(self.LOGIN_UI)
        self.builder.connect_signals(self)

        self._setup_login_flow_stack()
        self._setup_login_flow_headers()
        self._setup_enter_listener()

    def _add_from_resource(self, ui_filename):
        self.builder.add_from_resource(
            os.path.join(RESOURCES_DIR, ui_filename)
        )

    def _setup_login_flow_stack(self):
        self.login_flow_stack = self.builder.get_object(self.STACK_NAME)
        self.login_flow_stack.show_all()
        self.add(self.login_flow_stack)

    def _setup_login_flow_headers(self):
        login_flow_headers = self.builder.get_object(self.HEADERS_NAME)
        login_flow_headers.show_all()
        login_flow_headers.insert_action_group(
            LOGIN_PREFIX, self.get_action_group(LOGIN_PREFIX)
        )
        self._window.set_titlebar(login_flow_headers)

    def _setup_enter_listener(self):
        password_entry = self.builder.get_object("password_entry")
        password_entry.connect("activate", self._on_password_enter)

    # pylint: disable=unused-argument
    def _on_password_enter(self, widget):
        self.on_login_pressed()

    def _password_is_empty(self):
        password = self.builder.get_object("password_entry").get_text()
        return len(password) == 0

    def _show_loading_animation(self):
        loading_animation = self.builder.get_object("loading_animation")
        self.login_flow_stack.set_visible_child(loading_animation)

    def _login(self):
        password = self.builder.get_object("password_entry").get_text()
        APP().api.login(password, self._login_completed)

    def _login_completed(self, succeeded):
        function = self._login_failed
        if succeeded:
            function = self._window.show_main_container
        GLib.idle_add(function)

    def _login_failed(self):
        self._show_error_message(_("Couldn't log in"))
        self._focus_password_entry()
        self._show_login_page()

    def _show_error_message(self, error_message):
        error_label = self.builder.get_object("error_label")
        error_label.set_label(error_message)
        error_label.show()

    def _focus_password_entry(self):
        password_entry = self.builder.get_object("password_entry")
        password_entry.grab_focus()

    def _show_login_page(self):
        login_page = self.builder.get_object("login_page")
        self.login_flow_stack.set_visible_child(login_page)
