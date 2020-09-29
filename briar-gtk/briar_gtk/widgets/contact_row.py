# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

from gi.repository import GLib, Gtk, Pango

from briar_wrapper.models.contacts import Contacts

from briar_gtk.define import APP


class ContactRowWidget(Gtk.ListBoxRow):

    def __init__(self, contact):
        super().__init__()
        self._setup_view(contact)

    def _setup_view(self, contact):
        name = ContactRowWidget._get_contact_name(contact)
        contact_label = ContactRowWidget._create_contact_label(name)
        connected = contact["connected"]
        contact_state = ContactRowWidget._create_contact_state(connected)
        contact_box = ContactRowWidget._create_contact_box()
        contact_separator = ContactRowWidget._create_separator()
        contact_edit = ContactRowWidget._create_contact_edit(contact_box, contact_label, contact["contactId"])
        contact_event_box = Gtk.EventBox().new()

        contact_box.pack_start(contact_label, True, True, 0)
        contact_box.pack_end(contact_state, False, False, 0)
        contact_box.pack_end(contact_separator, False, False, 0)
        contact_box.pack_end(contact_edit, False, False, 0)
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
        contact_label = Gtk.Label.new(name)
        contact_label.set_valign(Gtk.Align.CENTER)
        contact_label.set_halign(Gtk.Align.START)
        contact_label.set_ellipsize(Pango.EllipsizeMode.END)
        return contact_label

    @staticmethod
    def _create_contact_state(connected):
        file_name = "contact_disconnected"
        if connected is True:
            file_name = "contact_connected"
        contact_state = Gtk.Image.new_from_icon_name(file_name,
                                                     Gtk.IconSize.MENU)
        return contact_state

    @staticmethod
    def _create_contact_box():
        contact_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        contact_box.get_style_context().add_class("contact-row")
        return contact_box

    @staticmethod
    def _create_contact_edit(contact_box, contact_label, contact_id):
        file_name = "contact_edit_alias"
        contact_image = Gtk.Image.new_from_icon_name(file_name, Gtk.IconSize.MENU)
        contact_edit_button = Gtk.Button()
        contact_edit_button.add(contact_image)

        def switch_label_elements(widget):
            contact_box.remove(contact_label)
            accept_button = Gtk.Button()
            accept_button.add(Gtk.Image.new_from_icon_name("contact_edit_accept", Gtk.IconSize.MENU))
            cancel_button = Gtk.Button()
            cancel_button.add(Gtk.Image.new_from_icon_name("contact_edit_cancel", Gtk.IconSize.MENU))
            edit_field = Gtk.Edit()
            edit_field.set_text(contact_label.get_text())
            contact_box.pack_start(cancel_button)
            contact_box.pack_start(accept_button)
            contact_box.pack_start(edit_field)

            def reset_view(widget):
                contact_box.remove(accept_button)
                contact_box.remove(cancel_button)
                contact_box.remove(edit_field)
                contact_box.pack_start(contact_label)

            def save_label(widget):
                reset_view(widget)
                new_alias = edit_field.get_text()
                contact_label.set_text(new_alias)
                ContactRowWidget._change_alias(contact_id, new_alias)
            cancel_button.connect("clicked", reset_view)
            accept_button.connect("clicked", )

        contact_edit_button.connect("clicked")
        return contact_edit_button

    @staticmethod
    def _create_separator():
        return Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)

    @staticmethod
    def _change_alias(contact_id, alias):
        contacts = Contacts(APP().api)
        contacts.set_alias(contact_id, alias)

    def _set_action(self, contact_id):
        data = GLib.Variant.new_int32(contact_id)
        self.set_action_target_value(data)
        self.set_action_name("win.open-private-chat")
