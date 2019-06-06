# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import GLib, Gtk

from briar.api.models.private_chat import PrivateChat
from briar.gtk.container import Container
from briar.gtk.define import App


class ChatContainer(Container):

    def __init__(self, contact_id):
        super().__init__()
        self._api = App().api
        self._contact_id = contact_id
        self._setup_view()
        self._load_content()

    def _setup_view(self):
        self.builder.add_from_resource("/app/briar/gtk/ui/chat.ui")
        self.add(self.builder.get_object("chat"))
        self.builder.connect_signals(self)
        chat_entry = self.builder.get_object("chat_entry")
        chat_entry.connect("key-press-event", self._key_pressed)

    def _load_content(self):
        private_chat = PrivateChat(self._api)
        messages_list = private_chat.get(self._contact_id)
        self._messages_list_box = self.builder.get_object("messages_list")
        for message in messages_list:
            self._add_message(message["text"], message["local"])
        private_chat.watch_messages(self._contact_id, self._add_message_async)

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
        private_chat = PrivateChat(self._api)
        private_chat.send(self._contact_id, message)

        self._add_message(message, True)
        chat_entry.set_text("")
