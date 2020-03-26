# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

from gi.repository import GLib, Gtk, Pango


class ContactRowWidget(Gtk.ListBoxRow):

    def __init__(self, contact):
        super().__init__()
        self._setup_view(contact)

    def _setup_view(self, contact):
        name = ContactRowWidget._get_contact_name(contact)
        contact_label = ContactRowWidget._create_contact_label(name)
        contact_box = ContactRowWidget._create_contact_box()
        contact_event_box = Gtk.EventBox()

        contact_box.pack_start(contact_label, True, True, 0)
        contact_event_box.add(contact_box)
        self.add(contact_event_box)

        self.show_all()
        self._set_action(contact["contactId"])

    @staticmethod
    def _get_contact_name(contact):
        name = contact["author"]["name"]
        if "alias" in contact:
            name = contact["alias"]
        return name

    @staticmethod
    def _create_contact_label(name):
        contact_label = Gtk.Label(name)
        contact_label.set_valign(Gtk.Align.CENTER)
        contact_label.set_halign(Gtk.Align.START)
        contact_label.set_ellipsize(Pango.EllipsizeMode.END)
        return contact_label

    @staticmethod
    def _create_contact_box():
        contact_box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 5)
        contact_box.get_style_context().add_class("contact-row")
        return contact_box

    def _set_action(self, contact_id):
        data = GLib.Variant.new_int32(contact_id)
        self.set_action_target_value(data)
        self.set_action_name("win.open-private-chat")
