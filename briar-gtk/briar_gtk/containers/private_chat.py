# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

import time

from gi.repository import GLib, Gtk, Handy

from briar_wrapper.models.private_chat import PrivateChat

from briar_gtk.container import Container
from briar_gtk.define import APP
from briar_gtk.widgets.private_message import PrivateMessageWidget


# pylint: disable=too-few-public-methods
class PrivateChatContainer(Container):

    CONTAINER_UI = "/app/briar/gtk/private_chat.ui"

    def __init__(self, contact_name, contact_id):
        super().__init__()

        self._contact_name = contact_name
        self._contact_id = contact_id

        self._setup_view()
        self._load_content()

    def _setup_view(self):
        self.builder.add_from_resource(self.CONTAINER_UI)

        self._messages_box = Gtk.ListBox()
        self._messages_box.get_style_context().add_class("messages-history")
        self._messages_box.show()

        column = Handy.Column()
        column.set_maximum_width(800)
        column.set_linear_growth_width(600)
        column.set_hexpand(True)
        column.set_vexpand(True)
        column.add(self._messages_box)
        column.show()

        messages_column = self.builder.get_object("messages_column")
        messages_column.get_style_context().add_class("messages-box")
        messages_column.add(column)
        messages_column.show()

        self.add(self.builder.get_object("messages_scroll"))

        self.builder.connect_signals(self)

    def _load_content(self):
        private_chat = PrivateChat(APP().api, self._contact_id)
        messages_list = private_chat.get()
        for message in messages_list:
            self._add_message(message)
        private_chat.watch_messages(self._add_message_async)

    def _add_message(self, message):
        message = PrivateMessageWidget(self._contact_name, message)
        self._messages_box.add(message)

    def _add_message_async(self, message):
        GLib.idle_add(self._add_message, message)

    # pylint: disable=unused-argument
    def send_message(self, widget):
        message = widget.get_text()
        private_chat = PrivateChat(APP().api, self._contact_id)
        private_chat.send(message)

        self._add_message(
            {
                "text": message,
                "local": True,
                "timestamp": int(round(time.time() * 1000))
            })
        widget.set_text("")
