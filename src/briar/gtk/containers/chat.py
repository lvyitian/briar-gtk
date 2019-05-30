# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.models.private_chat import PrivateChat
from briar.gtk.container import Container
from briar.gtk.define import App

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ChatContainer(Container):

    def __init__(self, contact_id):
        super().__init__()
        self._api = App().api
        self._setup_view()
        self._load_content(contact_id)

    def _setup_view(self):
        self.builder.add_from_resource("/app/briar/gtk/ui/main.ui")
        self.add(self.builder.get_object("main"))
        self.builder.connect_signals(self)

    def _load_content(self, contact_id):
        private_chat = PrivateChat(self._api)
        messages_list = private_chat.get(contact_id)
        messages_list_box = self.builder.get_object("contacts_list")
        for message in messages_list:
            message_label = Gtk.Label(message["text"])
            message_label.show()
            messages_list_box.add(message_label)
