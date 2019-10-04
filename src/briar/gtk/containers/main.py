# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import GLib, Gtk

from briar.api.models.contacts import Contacts
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
        contacts = Contacts(self._api)
        contacts_list = contacts.get()
        contacts_list_box = self.builder.get_object("contacts_list")
        for contact in contacts_list:
            contact_button = Gtk.Button(contact["author"]["name"])
            contact_button.connect("clicked", MainContainer._contact_clicked,
                                   contact["contactId"])
            contact_button.show()
            contacts_list_box.add(contact_button)

    # pylint: disable=unused-argument
    @staticmethod
    def _contact_clicked(widget, contact_id):
        GLib.idle_add(APP().window.open_private_chat, contact_id)
