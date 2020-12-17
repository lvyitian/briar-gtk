# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gettext import gettext as _
from gi.repository import Gtk

from briar_wrapper.models.contacts import Contacts

from briar_gtk.containers.private_chat import PrivateChatContainer
from briar_gtk.controllers.main_menu import MainMenuController
from briar_gtk.controllers.notification import NotificationController
from briar_gtk.controllers.private_chat import PrivateChatController
from briar_gtk.controllers.sidebar import SidebarController
from briar_gtk.define import APP, NOTIFICATION_CONTACT_ADDED
from briar_gtk.define import NOTIFICATION_PRIVATE_MESSAGE
from briar_gtk.views.main_menu import MainMenuView
from briar_gtk.views.private_chat import PrivateChatView
from briar_gtk.views.sidebar import SidebarView
from briar_gtk.widgets.about_dialog import AboutDialogWidget
from briar_gtk.widgets.edit_dialog import EditDialog


class MainWindowController():

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
        self._private_chat_controller.open_change_contact_alias_dialog()

    def open_delete_all_messages_dialog(self):
        self._private_chat_controller.open_delete_all_messages_dialog()

    def open_delete_contact_dialog(self):
        self._private_chat_controller.open_delete_contact_dialog()

    def close_private_chat(self):
        self._private_chat_controller.close_private_chat()

    def open_private_chat(self, contact_id):
        self._private_chat_controller.open_private_chat(contact_id)

    def _setup_children(self):
        self._setup_notification_controller()
        self._setup_sidebar_controller()
        self._setup_private_chat_controller()
        self._setup_main_menu_controller()

    def _setup_notification_controller(self):
        self._notification_controller = NotificationController()

    def _setup_sidebar_controller(self):
        self._sidebar_view = SidebarView(self._builder)
        self._sidebar_controller = SidebarController(
            self._sidebar_view, APP().api)

    def _setup_private_chat_controller(self):
        self._private_chat_view = PrivateChatView(self._builder)
        self._private_chat_controller = PrivateChatController(
            self._private_chat_view, self._sidebar_controller,
            self._builder, APP().api)

    def _setup_main_menu_controller(self):
        self._main_menu_view = MainMenuView()
        self._main_menu_controller = MainMenuController(
            self._main_menu_view, APP().api)

    def _setup_destroy_listener(self):
        self._main_window_view.connect("destroy", self._on_destroy)

    # pylint: disable=unused-argument
    def _on_destroy(self, widget):
        self._disconnect_signals()

    def _disconnect_signals(self):
        self._sidebar_controller.disconnect_signals()
        self._notification_controller.disconnect_signals()
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)
