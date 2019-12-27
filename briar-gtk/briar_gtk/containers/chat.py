# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import GLib, Gtk

from briar_wrapper.models.private_chat import PrivateChat

from briar_gtk.container import Container
from briar_gtk.define import APP


class ChatContainer(Container):

    CONTAINER_UI = "/app/briar/gtk/ui/chat.ui"

    def __init__(self, contact_id):
        super().__init__()
        self._api = APP().api
        self._contact_id = contact_id
        self._setup_view()
        self._load_content()

    def _setup_view(self):
        self.builder.add_from_resource(self.CONTAINER_UI)
        self.add(self.builder.get_object("chat"))
        self.builder.connect_signals(self)
        chat_entry = self.builder.get_object("chat_entry")
        chat_entry.connect("key-press-event", self._key_pressed)

    def _load_content(self):
        private_chat = PrivateChat(self._api, self._contact_id)
        messages_list = private_chat.get()
        self._messages_list_box = self.builder.get_object("messages_list")
        for message in messages_list:
            self._add_message(message["text"], message["local"])
        private_chat.watch_messages(self._add_message_async)

    def _add_message(self, message, local):
        message_label = Gtk.Label(message)
        message_label.set_halign(Gtk.Align.START)
        if local:
            message_label.set_halign(Gtk.Align.END)
        message_label.show()
        self._messages_list_box.add(message_label)

    def _add_message_async(self, message):
        GLib.idle_add(self._add_message, message["text"], False)

    # pylint: disable=unused-argument
    def _key_pressed(self, widget, event):
        if event.hardware_keycode != 36 and event.hardware_keycode != 104:
            return
        chat_entry = self.builder.get_object("chat_entry")
        message = chat_entry.get_text()
        private_chat = PrivateChat(self._api, self._contact_id)
        private_chat.send(message)

        self._add_message(message, True)
        chat_entry.set_text("")
