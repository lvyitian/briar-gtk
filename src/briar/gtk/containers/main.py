# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import GLib, Gtk

from briar_wrapper.models.contacts import Contacts
from briar.gtk.container import Container
from briar.gtk.define import APP


class MainContainer(Container):

    CONTAINER_UI = "/app/briar/gtk/ui/main.ui"

    def __init__(self):
        super().__init__()
        self._api = APP().api
        self._setup_view()
        self._load_content()

    def _setup_view(self):
        self.builder.add_from_resource(self.CONTAINER_UI)
        self.add(self.builder.get_object("contacts_list"))
        self.builder.connect_signals(self)

    def _load_content(self):
        self._contacts = Contacts(self._api)
        self._load_contacts()
        self._contacts.watch_contacts(self._refresh_contacts_async)

    def _load_contacts(self):
        contacts_list = self._contacts.get()
        contacts_list_box = self.builder.get_object("contacts_list")
        for contact in contacts_list:
            name = contact["author"]["name"]
            if "alias" in contact:
                name = contact["alias"]
            contact_button = Gtk.Button(name)
            contact_button.connect("clicked", MainContainer._contact_clicked,
                                   contact["contactId"])
            contact_button.show()
            contacts_list_box.add(contact_button)

    def _refresh_contacts_async(self):
        GLib.idle_add(self._refresh_contacts)

    def _refresh_contacts(self):
        self._clear_contact_list()
        self._load_contacts()

    def _clear_contact_list(self):
        contacts_list_box = self.builder.get_object("contacts_list")
        contacts_list_box_children = contacts_list_box.get_children()
        for child in contacts_list_box_children:
            contacts_list_box.remove(child)

    # pylint: disable=unused-argument
    @staticmethod
    def _contact_clicked(widget, contact_id):
        GLib.idle_add(APP().get_property("active_window").
                      open_private_chat, contact_id)
