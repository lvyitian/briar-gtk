# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

from datetime import datetime

from gettext import gettext as _
from gi.repository import Gtk, Pango


class PrivateMessageWidget(Gtk.ListBoxRow):

    def __init__(self, contact_name, message, previous_message):
        super().__init__()
        self._setup_view(contact_name, message, previous_message)

    def _setup_view(self, contact_name, message, previous_message):
        self.set_selectable(False)

        username = contact_name
        username_style_class = "username"
        if message["local"]:
            username = _(
                #  Context:
                #  "Used in message history to indicate that message is"
                #  "by the user itself, not by its contact"
                "Myself"
            )
            username_style_class = "username-self"

        username_info = PrivateMessageWidget._create_username_info(
            username, username_style_class)
        delivery_state_info = PrivateMessageWidget._create_delivery_state_info(
            message)
        date_info = PrivateMessageWidget._create_date_info(
            message["timestamp"] / 1000)
        info = PrivateMessageWidget._create_info(
            username_info,
            delivery_state_info,
            date_info
        )

        body_content = PrivateMessageWidget._create_body_content(
            message["text"])
        body = PrivateMessageWidget._create_body(body_content)

        event_box = Gtk.EventBox()
        if self._should_include_info(message, previous_message):
            self.set_margin_top(12)
            content = PrivateMessageWidget._create_content(info, body)
            message_box = PrivateMessageWidget._create_message_box(content)
        else:
            message_box = PrivateMessageWidget._create_message_box(body)

        event_box.add(message_box)
        self.add(event_box)
        self.show_all()

    @staticmethod
    def _create_username_info(username, username_style_class):
        username_label = Gtk.Label.new(username)
        username_label.set_justify(Gtk.Justification.LEFT)
        username_label.set_halign(Gtk.Align.START)
        username_label.get_style_context().add_class(username_style_class)

        username_event_box = Gtk.EventBox()
        username_event_box.add(username_label)
        return username_event_box

    @staticmethod
    def _create_delivery_state_info(message):
        file_name = "message_stored"
        if not message.get("local", True):
            return Gtk.EventBox()
        # TODO: Remove once web events updating is implemented
        if message.get("no_stored_indicator", False):
            return Gtk.EventBox()
        if message.get("sent", False):
            file_name = "message_sent"
        if message.get("seen", False):
            file_name = "message_delivered"
        delivery_state = Gtk.Image.new_from_icon_name(file_name,
                                                      Gtk.IconSize.MENU)
        return delivery_state

    @staticmethod
    def _create_date_info(timestamp):
        time = PrivateMessageWidget._make_timestamp_relative(timestamp)
        date_label = Gtk.Label.new(time)
        date_label.set_justify(Gtk.Justification.RIGHT)
        date_label.set_valign(Gtk.Align.START)
        date_label.set_halign(Gtk.Align.END)
        date_label.get_style_context().add_class("timestamp")
        return date_label

    @staticmethod
    def _make_timestamp_relative(timestamp):
        time = datetime.fromtimestamp(timestamp)
        time_diff = (datetime.now() - time).total_seconds()

        time_use_gen = lambda x, y: int(x // y) if x >= y else ''
        time_term_gen = lambda x, y: x+'s' if y > 1 and x[-1] != '.' else x
        time_list = ['day', 'hr.', 'min.']
        seconds_list = [86400, 3600, 60]

        time_use, time_term = '', ''
        for t, s in zip(time_list, seconds_list):
            time_use = time_use_gen(time_diff, s)
            if time_use:
                time_term = time_term_gen(t, time_use)
                break

        time_relative = '{} {} ago'.format(time_use, time_term) if time_use \
                            else 'now'
        if time_term in ['days', 'day']:
            time_relative += ', {}'.format(datetime.strftime(time, '%H:%M %p'))

        return time_relative

    @staticmethod
    def _create_info(username_info, delivery_state_info, date_info):
        info = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        info.pack_start(username_info, True, True, 0)
        if isinstance(delivery_state_info, Gtk.Image):
            info.pack_end(delivery_state_info, False, False, 3)
        else:
            info.pack_end(delivery_state_info, False, False, 11)
        info.pack_end(date_info, False, False, 0)
        return info

    @staticmethod
    def _create_body_content(text):
        body_content = Gtk.Label.new(text)
        body_content.set_line_wrap(True)
        body_content.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        body_content.set_halign(Gtk.Align.START)
        body_content.set_selectable(True)
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

    @staticmethod
    def _should_include_info(message, previous_message):
        if "local" not in previous_message:
            return True
        if message["local"] != previous_message["local"]:
            return True
        if message["sent"] != previous_message["sent"]:
            return True
        if message["seen"] != previous_message["seen"]:
            return True

        time = datetime.fromtimestamp(message.get("timestamp", 0) / 1000)
        previous_time = datetime.fromtimestamp(
            previous_message.get("timestamp", 0) / 1000)
        time_difference = time - previous_time
        return time_difference.total_seconds() > 60
