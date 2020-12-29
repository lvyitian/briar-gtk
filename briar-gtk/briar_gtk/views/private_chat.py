# Copyright (c) 2019-2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2
import os
import time

from gi.repository import GLib, Gtk, Handy

from briar_wrapper.models.private_chat import PrivateChat

from briar_gtk.define import APP, RESOURCES_DIR
from briar_gtk.widgets.private_message import PrivateMessageWidget


# pylint: disable=too-many-instance-attributes
class PrivateChatView(Gtk.Overlay):

    # TODO: Move more logic into PrivateChatPresenter

    CONTAINER_UI = "private_chat.ui"

    def __init__(self, builder):
        super().__init__()
        self.builder = builder

        self._signals = list()
        self._contact_name = ""
        self._contact_id = -1
        self._previous_message = dict()

    def send_message(self, widget):
        message = widget.get_text()
        private_chat = PrivateChat(APP().api, self._contact_id)
        private_chat.send(message)

        self._add_message(
            {
                "text": message,
                "local": True,
                "sent": False,
                "seen": False,

                # TODO: Remove once web events updating is implemented
                "no_stored_indicator": True,

                "timestamp": int(round(time.time() * 1000))
            })
        widget.set_text("")
        GLib.idle_add(self._scroll_to_bottom)

    def setup_view(self, contact_name, contact_id):
        self._contact_name = contact_name
        self._contact_id = contact_id
        self._add_from_resource(self.CONTAINER_UI)

        self._messages_box = Gtk.ListBox()
        self._messages_box.get_style_context().add_class("messages-history")
        self._messages_box.show()

        clamp = Handy.Clamp.new()
        clamp.set_maximum_size(800)
        clamp.set_tightening_threshold(600)
        clamp.set_hexpand(True)
        clamp.set_vexpand(True)
        clamp.add(self._messages_box)
        clamp.show()

        messages_column = self.builder.get_object("messages_column")
        messages_column.get_style_context().add_class("messages-box")
        messages_column.add(clamp)
        messages_column.show()

        messages_scroll = self.builder.get_object("messages_scroll")
        self._draw_signal_id = messages_scroll.connect(
            "draw", self._on_message_scroll_draw
        )
        self.add(messages_scroll)

        self.builder.connect_signals(self)
        self._setup_destroy_listener()

    def _add_from_resource(self, ui_filename):
        self.builder.add_from_resource(
            os.path.join(RESOURCES_DIR, ui_filename)
        )

    def _setup_destroy_listener(self):
        self.connect("destroy", self._on_destroy)

    # pylint: disable=unused-argument
    def _on_destroy(self, widget):
        self._disconnect_signals()

    def _disconnect_signals(self):
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)

    def load_content(self):
        private_chat = PrivateChat(APP().api, self._contact_id)
        messages_list = private_chat.get()
        self._messages_count = len(messages_list)
        for message in messages_list:
            # Abusing idle_add function here because otherwise the message box
            # is too small and scrolling cuts out messages
            GLib.idle_add(self._add_message, message)
            if message.get("read", True) is False:
                GLib.idle_add(private_chat.mark_read, message["id"])
        socket_listener = APP().api.socket_listener
        signal_id = socket_listener.connect("ConversationMessageReceivedEvent",
                                            self._add_message_async)
        self._signals.append(signal_id)

    def _add_message(self, message):
        if self._is_not_message(message):
            return
        message_widget = PrivateMessageWidget(
            self._contact_name,
            message,
            self._previous_message
        )
        self._previous_message = message
        self._messages_box.add(message_widget)

    @staticmethod
    def _is_not_message(message):
        return "text" not in message

    def _add_message_async(self, message):
        if message["data"]["contactId"] != self._contact_id:
            return
        GLib.idle_add(self._add_message_and_scroll, message["data"])
        if message["data"].get("read", True) is False:
            private_chat = PrivateChat(APP().api, self._contact_id)
            GLib.idle_add(private_chat.mark_read, message["data"]["id"])

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
