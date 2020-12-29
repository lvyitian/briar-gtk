# Copyright (c) 2019-2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2
import os

from gi.repository import GLib, Gtk, Handy

from briar_wrapper.models.private_chat import PrivateChat

from briar_gtk.define import APP, RESOURCES_DIR
from briar_gtk.presenters.private_chat import PrivateChatPresenter
from briar_gtk.widgets.private_message import PrivateMessageWidget


# pylint: disable=too-many-instance-attributes
class PrivateChatView(Gtk.Overlay):

    CONTAINER_UI = "private_chat.ui"

    def __init__(self, builder, contact_id, sidebar_presenter):
        super().__init__()
        self._contact_name = ""
        self._draw_signal_id = -1
        self._messages_box = None
        self._messages_count = 0
        self._previous_message = dict()

        self.builder = builder
        self.contact_id = contact_id
        self.presenter = PrivateChatPresenter(self, sidebar_presenter)

    def setup_view(self, contact_name):
        self._contact_name = contact_name
        self._setup_builder()

        self._setup_messages_box()
        clamp = self._setup_clamp()
        self._setup_messages_column(clamp)
        self._setup_messages_scroll()

        self.builder.connect_signals(self)
        self._setup_destroy_listener()

    def show_messages(self, messages):
        self._messages_count = len(messages)
        for message in messages:
            # Abusing idle_add function here because otherwise the message box
            # is too small and scrolling cuts out messages
            GLib.idle_add(self.add_message, message)

    def add_message(self, message):
        if self._is_not_message(message):
            return
        message_widget = PrivateMessageWidget(
            self._contact_name,
            message,
            self._previous_message
        )
        self._previous_message = message
        self._messages_box.add(message_widget)

    def scroll_to_bottom(self):
        messages_scroll = self.builder.get_object("messages_scroll")
        adjustment = messages_scroll.get_vadjustment()
        adjustment.set_value(
            adjustment.get_upper() - adjustment.get_page_size()
        )

    def add_message_async(self, message):
        if message["data"]["contactId"] != self.contact_id:
            return
        GLib.idle_add(self._add_message_and_scroll, message["data"])
        if message["data"].get("read", True) is False:
            private_chat = PrivateChat(APP().api, self.contact_id)
            GLib.idle_add(private_chat.mark_read, message["data"]["id"])

    def _setup_builder(self):
        self.builder.add_from_resource(
            os.path.join(RESOURCES_DIR, self.CONTAINER_UI)
        )

    def _setup_messages_box(self):
        self._messages_box = Gtk.ListBox()
        self._messages_box.get_style_context().add_class("messages-history")
        self._messages_box.show()

    def _setup_clamp(self):
        clamp = Handy.Clamp.new()
        clamp.set_maximum_size(800)  # same as in main_window.ui
        clamp.set_tightening_threshold(600)
        clamp.set_hexpand(True)
        clamp.set_vexpand(True)
        clamp.add(self._messages_box)
        clamp.show()
        return clamp

    def _setup_messages_column(self, clamp):
        messages_column = self.builder.get_object("messages_column")
        messages_column.get_style_context().add_class("messages-box")
        messages_column.add(clamp)
        messages_column.show()

    def _setup_messages_scroll(self):  # TODO: (Hopefully) remove hack in GTK 4
        messages_scroll = self.builder.get_object("messages_scroll")
        self._draw_signal_id = messages_scroll.connect(
            "draw", self._on_message_scroll_draw
        )
        self.add(messages_scroll)

    def _setup_destroy_listener(self):
        self.connect("destroy", self._on_destroy)

    # pylint: disable=unused-argument
    def _on_destroy(self, widget):
        self.presenter.disconnect_signals()

    @staticmethod
    def _is_not_message(message):
        return "text" not in message

    def _add_message_and_scroll(self, message):
        self.add_message(message)
        GLib.idle_add(self.scroll_to_bottom)

    # pylint: disable=unused-argument
    def _on_message_scroll_draw(self, widget, cairo_context):
        self.scroll_to_bottom()
        if self._draw_signal_is_not_needed():
            widget.disconnect(self._draw_signal_id)

    def _draw_signal_is_not_needed(self):
        if self._messages_count == 0:
            return True

        messages_scroll = self.builder.get_object("messages_scroll")
        adjustment = messages_scroll.get_vadjustment()
        return adjustment.get_value() != 0
