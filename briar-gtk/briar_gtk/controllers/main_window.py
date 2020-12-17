# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_wrapper.models.contacts import Contacts

from briar_gtk.containers.private_chat import PrivateChatContainer
from briar_gtk.controllers.main_menu import MainMenuController
from briar_gtk.controllers.private_chat import PrivateChatController
from briar_gtk.controllers.sidebar import SidebarController
from briar_gtk.define import APP
from briar_gtk.views.main_menu import MainMenuView
from briar_gtk.views.private_chat import PrivateChatView
from briar_gtk.views.sidebar import SidebarView
from briar_gtk.widgets.about_dialog import AboutDialogWidget


class MainWindowController():

    def __init__(self, main_window_view, builder):
        self._main_window_view = main_window_view
        self._builder = builder
        self._signals = list()

        self._setup_children()
        self._load_content()
        self._setup_destroy_listener()

    @staticmethod
    def open_about_page():
        about_dialog = AboutDialogWidget()
        about_dialog.show()

    def open_private_chat(self, contact_id):
        contact_name = self._get_contact_name(contact_id)
        self._prepare_chat_view(contact_name)
        self._setup_private_chat_widget(contact_name, contact_id)
        self._current_contact_id = contact_id

    def _setup_children(self):
        self._sidebar_view = SidebarView(self._builder)
        self._sidebar_controller = SidebarController(
            self._sidebar_view, APP().api)

        self._private_chat_view = PrivateChatView(self._builder)
        self._private_chat_controller = PrivateChatController(
            self._private_chat_view, APP().api)

        self._main_menu_view = MainMenuView()
        self._main_menu_controller = MainMenuController(
            self._main_menu_view, APP().api)

    def _get_contact_name(self, contact_id):
        name = ""
        for contact in Contacts(APP().api).get():
            if contact["contactId"] == contact_id:
                name = contact["author"]["name"]
                if "alias" in contact:
                    name = contact["alias"]
                break
        return name

    def _prepare_chat_view(self, contact_name):
        main_content_stack = self._builder.get_object("main_content_stack")
        chat_placeholder = main_content_stack.get_child_by_name(
            "chat_placeholder")
        if self._no_chat_opened():
            chat_placeholder.hide()
        else:
            self._clear_history_container()

        chat_view = main_content_stack.get_child_by_name("chat_view")
        chat_view.show()
        main_window_leaflet = self._builder.get_object("main_window_leaflet")
        main_content_container = self._builder.get_object(
            "main_content_container")
        main_window_leaflet.set_visible_child(main_content_container)
        contact_name_label = self._builder.get_object("contact_name")
        contact_name_label.set_text(contact_name)
        self._builder.get_object("chat_menu_button").show()

    def _no_chat_opened(self):
        main_content_stack = self._builder.get_object("main_content_stack")
        chat_placeholder = main_content_stack.get_child_by_name(
            "chat_placeholder")
        return chat_placeholder.get_visible()

    def _clear_history_container(self):
        history_container = self._builder.get_object("history_container")
        children = history_container.get_children()
        for child in children:
            child.destroy()
        if hasattr(self, "_selected_contact"):
            del self._selected_contact

    # pylint: disable=no-member
    def _load_content(self):
        socket_listener = APP().api.socket_listener
        self._setup_contact_added_listeners(socket_listener)
        self._setup_message_received_listeners(socket_listener)

    def _setup_contact_added_listeners(self, socket_listener):
        signal_id = socket_listener.connect("ContactAddedEvent",
                                            self._notify_contact_added)
        self._signals.append(signal_id)

    def _setup_message_received_listeners(self, socket_listener):
        signal_id = socket_listener.connect("ConversationMessageReceivedEvent",
                                            self._notify_message_received)
        self._signals.append(signal_id)

    # pylint: disable=unused-argument
    def _notify_contact_added(self, message):
        self._notify(
            _("Contact added"),  # context: "Notification"
            NOTIFICATION_CONTACT_ADDED
        )

    # pylint: disable=unused-argument
    def _notify_message_received(self, message):
        self._notify(
            _("New private message"),  # context: "Notification"
            NOTIFICATION_PRIVATE_MESSAGE
        )

    @staticmethod
    def _notify(title, identifier):
        if APP().window.is_active():
            return
        notification = Gio.Notification.new(title)
        notification.set_priority(Gio.NotificationPriority.HIGH)
        APP().send_notification(identifier, notification)

    def _setup_destroy_listener(self):
        self._main_window_view.connect("destroy", self._on_destroy)

    # pylint: disable=unused-argument
    def _on_destroy(self, widget):
        self._disconnect_signals()

    def _disconnect_signals(self):
        self._sidebar_controller.disconnect_signals()
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)

    def _setup_private_chat_widget(self, contact_name, contact_id):
        self._current_private_chat_widget = PrivateChatContainer(
            contact_name, contact_id)
        history_container = self._builder.get_object("history_container")
        history_container.add(self._current_private_chat_widget)
        history_container.show_all()

        self._disconnect_chat_entry_signals()
        chat_entry = self._builder.get_object("chat_entry")
        self._chat_entry_signal_id = chat_entry.connect(
            "activate", self._on_chat_entry_activate
        )
        chat_entry.grab_focus()

    def _disconnect_chat_entry_signals(self):
        if not hasattr(self, "_chat_entry_signal_id"):
            return
        chat_entry = self._builder.get_object("chat_entry")
        chat_entry.disconnect(self._chat_entry_signal_id)
        del self._chat_entry_signal_id

    def _on_chat_entry_activate(self, widget):
        if len(widget.get_text()) == 0:
            return
        self._current_private_chat_widget.send_message(widget)
        self._refresh_contacts()
