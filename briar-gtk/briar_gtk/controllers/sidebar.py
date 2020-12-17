# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gio, GLib

from briar_wrapper.models.contacts import Contacts

from briar_gtk.define import APP, NOTIFICATION_CONTACT_ADDED
from briar_gtk.define import NOTIFICATION_PRIVATE_MESSAGE


class SidebarController():

    def __init__(self, sidebar_view, api):
        self._sidebar_view = sidebar_view
        self._api = api
        self._signals = list()

        self._load_content()

    def refresh_contacts(self):
        selected_row = self._sidebar_view.get_selected_row()
        self._load_contacts(selected_row)

    def disconnect_signals(self):
        for signal in self._signals:
            self._api.socket_listener.disconnect(signal)

    # pylint: disable=no-member
    def _load_content(self):
        self._contacts = Contacts(self._api)
        self._load_contacts()
        socket_listener = self._api.socket_listener
        self._setup_contact_added_listeners(socket_listener)
        self._setup_message_received_listeners(socket_listener)
        self._setup_contact_connection_listener(socket_listener)

    def _load_contacts(self, selected_row=-1):
        self.contacts_list = self._contacts.get()
        self._sidebar_view.show_contacts(
            self.contacts_list, selected_row)

    def _setup_contact_added_listeners(self, socket_listener):
        signal_id = socket_listener.connect("ContactAddedEvent",
                                            self._refresh_contacts_async)
        self._signals.append(signal_id)

    def _setup_message_received_listeners(self, socket_listener):
        signal_id = socket_listener.connect("ConversationMessageReceivedEvent",
                                            self._refresh_contacts_async)
        self._signals.append(signal_id)

    def _setup_contact_connection_listener(self, socket_listener):
        callback = self._refresh_contact_connection_state
        signal_ids = self._contacts.watch_connections(callback)
        self._signals.extend(signal_ids)

    # pylint: disable=unused-argument
    def _refresh_contacts_async(self, message):
        GLib.idle_add(self.refresh_contacts)

    # pylint: disable=unused-argument
    def _refresh_contact_connection_state(self, contact_id, connected):
        self._refresh_contacts_async(None)
