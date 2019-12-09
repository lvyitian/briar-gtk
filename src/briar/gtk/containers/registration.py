# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gettext import gettext as _

from gi.repository import GLib

from briar.gtk.container import Container
from briar.gtk.define import APP


class RegistrationContainer(Container):

    REGISTRATION_UI = "/app/briar/gtk/ui/registration.ui"
    STACK_NAME = "registration_flow_stack"
    HEADERS_NAME = "registration_flow_headers"

    def __init__(self, window):
        super().__init__()
        self._window = window
        self._setup_view()

    def _setup_view(self, ):
        self.builder.add_from_resource(self.REGISTRATION_UI)
        self.builder.connect_signals(self)

        self._setup_registration_flow_stack()
        self._setup_registration_flow_headers()
        self._setup_nickname_keystroke_listener()

    def _setup_registration_flow_stack(self):
        self.registration_flow_stack = self.builder.get_object(self.STACK_NAME)
        self.registration_flow_stack.show_all()
        self.add(self.registration_flow_stack)

    def _setup_registration_flow_headers(self):
        registration_flow_headers = self.builder.get_object(self.HEADERS_NAME)
        registration_flow_headers.show_all()
        self._window.set_titlebar(registration_flow_headers)

    def _setup_nickname_keystroke_listener(self):
        nickname_entry = self.builder.get_object("nickname_entry")
        nickname_entry.connect("key-press-event",
                               self._nickname_keystroke)

    # pylint: disable=unused-argument
    def _nickname_keystroke(self, widget, event):
        if event.hardware_keycode != 36 and event.hardware_keycode != 104:
            return
        self.on_nickname_next_pressed(None)

    # pylint: disable=unused-argument
    def on_nickname_next_pressed(self, button):
        nickname_error_label = self.builder.get_object("nickname_error_label")
        if self._nickname_is_empty():
            nickname_error_label.show()
            return
        nickname_error_label.hide()
        self._show_passwords_page()

    def _nickname_is_empty(self):
        nickname = self.builder.get_object("nickname_entry").get_text()
        return len(nickname) == 0

    def _show_passwords_page(self):
        passwords_page = self.builder.get_object("passwords_page")
        self.registration_flow_stack.set_visible_child(passwords_page)

        self._focus_password_entry()
        self._setup_passwords_keystroke_listener()

    def _focus_password_entry(self):
        password_entry = self.builder.get_object("password_entry")
        password_entry.grab_focus()

    def _setup_passwords_keystroke_listener(self):
        password_confirm_entry = self.builder.get_object(
            "password_confirm_entry")
        password_confirm_entry.connect(
            "key-press-event", self._passwords_keystroke)

    # pylint: disable=unused-argument
    def _passwords_keystroke(self, widget, event):
        if event.hardware_keycode != 36 and event.hardware_keycode != 104:
            return
        self.on_create_account_pressed(None)

    # pylint: disable=unused-argument
    def on_create_account_back_pressed(self, button):
        self._show_nickname_page()

    def _show_nickname_page(self):
        nickname_page = self.builder.get_object("nickname_page")
        self.registration_flow_stack.set_visible_child(nickname_page)

    # pylint: disable=unused-argument
    def on_create_account_pressed(self, button):
        passwords_error_label = self.builder.get_object(
            "passwords_error_label")
        if not self._passwords_match():
            passwords_error_label.show()
            return
        passwords_error_label.hide()
        self._show_loading_animation()
        self._register()

    def _passwords_match(self):
        password = self.builder.get_object("password_entry").get_text()
        password_confirm = self.builder.get_object(
            "password_confirm_entry").get_text()
        return password == password_confirm

    def _show_loading_animation(self):
        loading_animation = self.builder.get_object("loading_animation")
        self.registration_flow_stack.set_visible_child(loading_animation)

    def _register(self):
        nickname = self.builder.get_object("nickname_entry").get_text()
        password = self.builder.get_object("password_entry").get_text()
        APP().api.register((nickname, password),
                           self._registration_completed)

    def _registration_completed(self, succeeded):
        function = self._registration_failed
        if succeeded:
            function = self._window.on_startup_completed
        GLib.idle_add(function)

    def _registration_failed(self):
        self._show_error_message()
        self._show_passwords_page()

    def _show_error_message(self):
        passwords_error_label = self.builder.get_object(
            "passwords_error_label")
        passwords_error_label.set_label(_("Couldn't register account"))
        passwords_error_label.show()
