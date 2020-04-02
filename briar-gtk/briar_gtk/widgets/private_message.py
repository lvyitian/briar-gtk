# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

from datetime import datetime
from gettext import gettext as _

from gi.repository import Gtk


class PrivateMessageWidget(Gtk.ListBoxRow):

    def __init__(self, contact_name, message):
        super().__init__()
        self._setup_view(contact_name, message)

    def _setup_view(self, contact_name, message):
        self.set_selectable(False)
        self.set_margin_top(12)

        username = contact_name
        if message["local"]:
            username = _("Myself")

        username_info = PrivateMessageWidget._create_username_info(username)
        date_info = PrivateMessageWidget._create_date_info(
            message["timestamp"] / 1000)
        info = PrivateMessageWidget._create_info(username_info, date_info)

        body_content = PrivateMessageWidget._create_body_content(
            message["text"])
        body = PrivateMessageWidget._create_body(body_content)

        content = PrivateMessageWidget._create_content(info, body)
        message_box = PrivateMessageWidget._create_message_box(content)

        event_box = Gtk.EventBox()
        event_box.add(message_box)

        self.add(event_box)
        self.show_all()

    @staticmethod
    def _create_username_info(username):
        username_label = Gtk.Label.new(username)
        username_label.set_justify(Gtk.Justification.LEFT)
        username_label.set_halign(Gtk.Align.START)
        username_label.get_style_context().add_class("username")

        username_event_box = Gtk.EventBox()
        username_event_box.add(username_label)
        return username_event_box

    @staticmethod
    def _create_date_info(timestamp):
        time = PrivateMessageWidget._make_timestamp_readable(timestamp)
        date_label = Gtk.Label.new(time)
        date_label.set_justify(Gtk.Justification.RIGHT)
        date_label.set_valign(Gtk.Align.START)
        date_label.set_halign(Gtk.Align.END)
        date_label.get_style_context().add_class("timestamp")
        return date_label

    @staticmethod
    def _make_timestamp_readable(timestamp):
        time = datetime.fromtimestamp(timestamp)
        current_time = datetime.today()
        if time.date() == current_time.date():
            return time.strftime("%I:%M")
        return time.strftime("%x %I:%M")

    @staticmethod
    def _create_info(username_info, date_info):
        info = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        info.pack_start(username_info, True, True, 0)
        info.pack_end(date_info, False, False, 0)
        return info

    @staticmethod
    def _create_body_content(text):
        body_content = Gtk.Label.new(text)
        body_content.set_line_wrap(True)
        body_content.set_halign(Gtk.Align.START)
        body_content.set_xalign(0)
        return body_content

    @staticmethod
    def _create_body(body_content):
        body = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        body.add(body_content)
        return body

    @staticmethod
    def _create_content(info, body):
        content = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        content.pack_start(info, False, False, 0)
        content.pack_start(body, True, True, 0)
        return content

    @staticmethod
    def _create_message_box(content):
        message_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 10)
        message_box.pack_start(content, True, True, 0)
        return message_box
