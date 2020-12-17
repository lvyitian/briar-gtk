# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.handlers.notification import NotificationHandler
from briar_gtk.controllers.private_chat import PrivateChatController
from briar_gtk.controllers.sidebar import SidebarController
from briar_gtk.define import APP
from briar_gtk.views.private_chat import PrivateChatView
from briar_gtk.views.sidebar import SidebarView
from briar_gtk.widgets.about_dialog import AboutDialogWidget


class MainWindowController:

    def __init__(self, main_window_view, builder):
        self._main_window_view = main_window_view
        self._builder = builder
        self._signals = list()

        self._setup_children()
        self._setup_destroy_listener()

    @staticmethod
    def open_about_page():
        about_dialog = AboutDialogWidget()
        about_dialog.show()

    def open_change_contact_alias_dialog(self):
        if self._private_chat_controller is not None:
            self._private_chat_controller.open_change_contact_alias_dialog()

    def open_delete_all_messages_dialog(self):
        if self._private_chat_controller is not None:
            self._private_chat_controller.open_delete_all_messages_dialog()

    def open_delete_contact_dialog(self):
        if self._private_chat_controller is not None:
            self._private_chat_controller.open_delete_contact_dialog()

    def close_private_chat(self):
        if self._private_chat_controller is not None:
            self._private_chat_controller.close_private_chat()
            self._private_chat_controller = None

    def open_private_chat(self, contact_id):
        if self._private_chat_controller is not None:
            raise Exception("Private Chat is already open")
        private_chat_view = PrivateChatView(self._builder)
        self._private_chat_controller = PrivateChatController(
            contact_id, private_chat_view, self._sidebar_controller,
            self._builder, APP().api)

    def _setup_children(self):
        self._setup_notification_handler()
        self._setup_sidebar_controller()
        self._private_chat_controller = None
        contact_name_label = self._builder.get_object("contact_name")
        contact_name_label.set_text("")

    def _setup_notification_handler(self):
        self._notification_handler = NotificationHandler()

    def _setup_sidebar_controller(self):
        sidebar_view = SidebarView(self._builder)
        self._sidebar_controller = SidebarController(
            sidebar_view, APP().api)

    def _setup_destroy_listener(self):
        self._main_window_view.connect("destroy", self._on_destroy)

    # pylint: disable=unused-argument
    def _on_destroy(self, widget):
        self._disconnect_signals()

    def _disconnect_signals(self):
        self._sidebar_controller.disconnect_signals()
        self._notification_handler.disconnect_signals()
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)
