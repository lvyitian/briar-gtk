# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gettext import gettext as _
from gi.repository import Gio

from briar_gtk.define import APP, NOTIFICATION_CONTACT_ADDED
from briar_gtk.define import NOTIFICATION_PRIVATE_MESSAGE


class NotificationController():

    def __init__(self):
        self._signals = list()

        self._setup_listeners()

    def disconnect_signals(self):
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)

    def _setup_listeners(self):
        socket_listener = APP().api.socket_listener
        self._setup_contact_added_listener(socket_listener)
        self._setup_message_received_listener(socket_listener)

    def _setup_contact_added_listener(self, socket_listener):
        signal_id = socket_listener.connect("ContactAddedEvent",
                                            self._notify_contact_added)
        self._signals.append(signal_id)

    def _setup_message_received_listener(self, socket_listener):
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
