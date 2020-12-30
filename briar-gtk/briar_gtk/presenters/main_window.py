# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.handlers.notification import NotificationHandler
from briar_gtk.presenters.private_chat import PrivateChatPresenter
from briar_gtk.define import APP
from briar_gtk.views.private_chat import PrivateChatView
from briar_gtk.views.sidebar import SidebarView
from briar_gtk.widgets.about_dialog import AboutDialogWidget


class MainWindowPresenter:

    def __init__(self, view):
        self._notification_handler = NotificationHandler()
        self._private_chat_presenter = None
        self._sidebar_presenter = SidebarView(view.builder).presenter
        self._signals = list()
        self._view = view

        self._setup_destroy_listener()

    @staticmethod
    def open_about_page():
        about_dialog = AboutDialogWidget()
        about_dialog.show()

    def open_change_contact_alias_dialog(self):
        if isinstance(self._private_chat_presenter, PrivateChatPresenter):
            self._private_chat_presenter.open_change_contact_alias_dialog()

    def open_delete_all_messages_dialog(self):
        if isinstance(self._private_chat_presenter, PrivateChatPresenter):
            self._private_chat_presenter.open_delete_all_messages_dialog()

    def open_delete_contact_dialog(self):
        if isinstance(self._private_chat_presenter, PrivateChatPresenter):
            self._private_chat_presenter.open_delete_contact_dialog()

    def open_emoji_menu(self):
        if isinstance(self._private_chat_presenter, PrivateChatPresenter):
            self._private_chat_presenter.open_emoji_menu()

    def close_private_chat(self):
        if isinstance(self._private_chat_presenter, PrivateChatPresenter):
            self._private_chat_presenter.close_private_chat()
            self._private_chat_presenter = None

    def open_private_chat(self, contact_id):
        self.close_private_chat()
        private_chat_view = PrivateChatView(
            self._view.builder, contact_id, self._sidebar_presenter)
        self._private_chat_presenter = private_chat_view.presenter

    def send_message(self):
        if isinstance(self._private_chat_presenter, PrivateChatPresenter):
            self._private_chat_presenter.send_message()

    def _setup_destroy_listener(self):
        self._view.connect("destroy", self._on_destroy)

    # pylint: disable=unused-argument
    def _on_destroy(self, widget):
        self._disconnect_signals()

    def _disconnect_signals(self):
        self._sidebar_presenter.disconnect_signals()
        self._notification_handler.disconnect_signals()
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)
