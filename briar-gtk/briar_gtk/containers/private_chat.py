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

    CONTAINER_UI = "private_chat.ui"

    def __init__(self, contact_name, contact_id):
        super().__init__()

        self._contact_name = contact_name
        self._contact_id = contact_id

        self._setup_view()
        self._load_content()

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
        GLib.idle_add(self._scroll_to_bottom)

    def _setup_view(self):
        self._add_from_resource(self.CONTAINER_UI)

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

        messages_scroll = self.builder.get_object("messages_scroll")
        self._draw_signal_id = messages_scroll.connect(
            "draw", self._on_message_scroll_draw
        )
        self.add(messages_scroll)

        self.builder.connect_signals(self)

    def _load_content(self):
        private_chat = PrivateChat(APP().api, self._contact_id)
        messages_list = private_chat.get()
        self._messages_count = len(messages_list)
        for message in messages_list:
            # Abusing idle_add function here because otherwise the message box
            # is too small and scrolling cuts out messages
            GLib.idle_add(self._add_message, message)
        # TODO: Disconnect if no more needed
        APP().api.socket_listener.connect("ConversationMessageReceivedEvent",
                                          self._add_message_async)

    def _add_message(self, message):
        message_widget = PrivateMessageWidget(self._contact_name, message)
        self._messages_box.add(message_widget)

    def _add_message_async(self, message):
        if message["data"]["contactId"] == self._contact_id:
            GLib.idle_add(self._add_message_and_scroll, message["data"])

    def _add_message_and_scroll(self, message):
        self._add_message(message)
        GLib.idle_add(self._scroll_to_bottom)

    # pylint: disable=unused-argument
    def _on_message_scroll_draw(self, widget, cairo_context):
        self._scroll_to_bottom()
        if self._draw_signal_is_not_needed():
            widget.disconnect(self._draw_signal_id)

    def _scroll_to_bottom(self):
        messages_scroll = self.builder.get_object("messages_scroll")
        adjustment = messages_scroll.get_vadjustment()
        adjustment.set_value(
            adjustment.get_upper() - adjustment.get_page_size()
        )

    def _draw_signal_is_not_needed(self):
        if self._messages_count == 0:
            return True

        messages_scroll = self.builder.get_object("messages_scroll")
        adjustment = messages_scroll.get_vadjustment()
        return adjustment.get_value() != 0
