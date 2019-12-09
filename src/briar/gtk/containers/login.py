# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import GLib

from briar.gtk.container import Container
from briar.gtk.define import APP


class LoginContainer(Container):

    LOGIN_UI = "/app/briar/gtk/ui/login.ui"
    STACK_NAME = "login_flow_stack"
    HEADERS_NAME = "login_flow_headers"

    def __init__(self, window):
        super().__init__()
        self._window = window
        self._setup_view()

    def _setup_view(self, ):
        self.builder.add_from_resource(self.LOGIN_UI)
        self.builder.connect_signals(self)

        self._setup_login_flow_stack()
        self._setup_login_flow_headers()
        self._setup_keystroke_listener()

    def _setup_login_flow_stack(self):
        self.login_flow_stack = self.builder.get_object(self.STACK_NAME)
        self.login_flow_stack.show_all()
        self.add(self.login_flow_stack)

    def _setup_login_flow_headers(self):
        login_flow_headers = self.builder.get_object(self.HEADERS_NAME)
        login_flow_headers.show_all()
        self._window.set_titlebar(login_flow_headers)

    def _setup_keystroke_listener(self):
        password_entry = self.builder.get_object("password_entry")
        password_entry.connect("key-press-event",
                               self._password_keystroke)

    # pylint: disable=unused-argument
    def _password_keystroke(self, widget, event):
        if event.hardware_keycode != 36 and event.hardware_keycode != 104:
            return
        self.on_login_pressed(None)

    # pylint: disable=unused-argument
    def on_login_pressed(self, button):
        self._show_loading_animation()
        self._login()

    def _show_loading_animation(self):
        loading_animation = self.builder.get_object("loading_animation")
        self.login_flow_stack.set_visible_child(loading_animation)

    def _login(self):
        password = self.builder.get_object("password_entry").get_text()
        APP().api.login(password, self._login_completed)

    def _login_completed(self, succeeded):
        function = self._login_failed
        if succeeded:
            function = self._window.on_startup_completed
        GLib.idle_add(function)

    def _login_failed(self):
        self._show_error_message()
        self._focus_password_entry()
        self._show_login_page()

    def _show_error_message(self):
        error_message = self.builder.get_object("error_message")
        error_message.show()

    def _focus_password_entry(self):
        password_entry = self.builder.get_object("password_entry")
        password_entry.grab_focus()

    def _show_login_page(self):
        login_page = self.builder.get_object("login_page")
        self.login_flow_stack.set_visible_child(login_page)
