# Copyright (c) 2019-2021 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
import os
from gettext import gettext as _

from gi.repository import GLib, Gtk

from briar_gtk.startup.registration_actions import RegistrationActions
from briar_gtk.actions.prefixes import REGISTRATION_PREFIX
from briar_gtk.define import APP, RESOURCES_DIR


class RegistrationView(Gtk.Overlay):

    # TODO: Move more logic into RegistrationPresenter

    REGISTRATION_UI = "registration.ui"
    STACK_NAME = "registration_flow_stack"
    HEADERS_NAME = "registration_flow_headers"

    def __init__(self, window):
        super().__init__()
        self.builder = Gtk.Builder()
        RegistrationActions(self)
        self._window = window
        self._setup_view()

    @property
    def nickname_entry(self):
        return self.builder.get_object("nickname_entry")

    @property
    def nickname_error_label(self):
        return self.builder.get_object("nickname_error_label")

    @property
    def password_entry(self):
        return self.builder.get_object("password_entry")

    @property
    def passwords_error_label(self):
        return self.builder.get_object("passwords_error_label")

    def proceed_from_nickname(self):
        if self._nickname_is_empty():
            self._show_nickname_error_message(_("Please enter a nickname"))
            return
        self.nickname_error_label.hide()
        self._show_passwords_page()

    def show_nickname_page(self):
        nickname_page = self.builder.get_object("nickname_page")
        self.registration_flow_stack.set_visible_child(nickname_page)

    def on_create_account_pressed(self):
        if self._password_is_empty():
            self._show_passwords_error_message(_("Please enter a password"))
            return
        if not self._passwords_match():
            self._show_passwords_error_message(_("The passwords do not match"))
            return
        self.passwords_error_label.hide()
        self._show_loading_animation()
        self._register()

    def _setup_view(self):
        self._add_from_resource(self.REGISTRATION_UI)
        self.builder.connect_signals(self)

        self._setup_registration_flow_stack()
        self._setup_registration_flow_headers()
        self._setup_nickname_enter_listener()

    def _add_from_resource(self, ui_filename):
        self.builder.add_from_resource(
            os.path.join(RESOURCES_DIR, ui_filename)
        )

    def _setup_registration_flow_stack(self):
        self.registration_flow_stack = self.builder.get_object(self.STACK_NAME)
        self.registration_flow_stack.show_all()
        self.add(self.registration_flow_stack)

    def _setup_registration_flow_headers(self):
        registration_flow_headers = self.builder.get_object(self.HEADERS_NAME)
        registration_flow_headers.show_all()
        registration_flow_headers.insert_action_group(
            REGISTRATION_PREFIX, self.get_action_group(REGISTRATION_PREFIX)
        )
        self._window.set_titlebar(registration_flow_headers)

    def _setup_nickname_enter_listener(self):
        self.nickname_entry.connect("activate", self._on_nickname_enter)

    # pylint: disable=unused-argument
    def _on_nickname_enter(self, widget):
        self.proceed_from_nickname()

    def _nickname_is_empty(self):
        nickname = self.nickname_entry.get_text()
        return len(nickname) == 0

    def _show_passwords_page(self):
        passwords_page = self.builder.get_object("passwords_page")
        self.registration_flow_stack.set_visible_child(passwords_page)

        self._focus_password_entry()
        self._setup_passwords_enter_listener()

    def _focus_password_entry(self):
        self.password_entry.grab_focus()

    def _setup_passwords_enter_listener(self):
        password_confirm_entry = self.builder.get_object(
            "password_confirm_entry")
        password_confirm_entry.connect(
            "activate", self._on_passwords_enter)

    # pylint: disable=unused-argument
    def _on_passwords_enter(self, widget):
        self.on_create_account_pressed()

    def _password_is_empty(self):
        password = self.password_entry.get_text()
        return len(password) == 0

    def _passwords_match(self):
        password = self.password_entry.get_text()
        password_confirm = self.builder.get_object(
            "password_confirm_entry").get_text()
        return password == password_confirm

    def _show_loading_animation(self):
        loading_animation = self.builder.get_object("loading_animation")
        self.registration_flow_stack.set_visible_child(loading_animation)

    def _register(self):
        nickname = self.nickname_entry.get_text()
        password = self.password_entry.get_text()
        APP().api.register((nickname, password),
                           self._registration_completed)

    def _registration_completed(self, succeeded):
        function = self._registration_failed
        if succeeded:
            function = self._window.show_conversation_view
        GLib.idle_add(function)

    def _registration_failed(self):
        self._show_passwords_error_message(_("Couldn't register account"))
        self._show_passwords_page()

    def _show_nickname_error_message(self, error_message):
        self._show_error_message(self.nickname_error_label, error_message)

    def _show_passwords_error_message(self, error_message):
        self._show_error_message(self.passwords_error_label, error_message)

    @staticmethod
    def _show_error_message(error_label, error_message):
        error_label.set_label(error_message)
        error_label.show()
