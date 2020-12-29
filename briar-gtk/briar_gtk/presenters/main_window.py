# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.handlers.notification import NotificationHandler
from briar_gtk.presenters.private_chat import PrivateChatPresenter
from briar_gtk.presenters.sidebar import SidebarPresenter
from briar_gtk.define import APP
from briar_gtk.views.private_chat import PrivateChatView
from briar_gtk.views.sidebar import SidebarView
from briar_gtk.widgets.about_dialog import AboutDialogWidget


class MainWindowPresenter:

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
        if self._private_chat_presenter is not None:
            self._private_chat_presenter.open_change_contact_alias_dialog()

    def open_delete_all_messages_dialog(self):
        if self._private_chat_presenter is not None:
            self._private_chat_presenter.open_delete_all_messages_dialog()

    def open_delete_contact_dialog(self):
        if self._private_chat_presenter is not None:
            self._private_chat_presenter.open_delete_contact_dialog()

    def close_private_chat(self):
        if self._private_chat_presenter is not None:
            self._private_chat_presenter.close_private_chat()
            self._private_chat_presenter = None

    def open_private_chat(self, contact_id):
        private_chat_view = PrivateChatView(self._builder)
        self._private_chat_presenter = PrivateChatPresenter(
            contact_id, private_chat_view, self._sidebar_presenter,
            self._builder, APP().api)

    def _setup_children(self):
        self._setup_notification_handler()
        self._setup_sidebar_presenter()
        self._private_chat_presenter = None
        contact_name_label = self._builder.get_object("contact_name")
        contact_name_label.set_text("")

    def _setup_notification_handler(self):
        self._notification_handler = NotificationHandler()

    def _setup_sidebar_presenter(self):
        sidebar_view = SidebarView(self._builder)
        self._sidebar_presenter = SidebarPresenter(
            sidebar_view, APP().api)

    def _setup_destroy_listener(self):
        self._main_window_view.connect("destroy", self._on_destroy)

    # pylint: disable=unused-argument
    def _on_destroy(self, widget):
        self._disconnect_signals()

    def _disconnect_signals(self):
        self._sidebar_presenter.disconnect_signals()
        self._notification_handler.disconnect_signals()
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)
