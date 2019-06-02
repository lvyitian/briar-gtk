# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.models.contacts import Contacts
from briar.gtk.container import Container
from briar.gtk.define import App

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk


class MainContainer(Container):

    def __init__(self):
        super().__init__()
        self._api = App().api
        self._setup_view()
        self._load_content()

    def _setup_view(self):
        self.builder.add_from_resource("/app/briar/gtk/ui/main.ui")
        self.add(self.builder.get_object("contacts_list"))
        self.builder.connect_signals(self)

    def _load_content(self):
        contacts = Contacts(self._api)
        contacts_list = contacts.get()
        contacts_list_box = self.builder.get_object("contacts_list")
        for contact in contacts_list:
            contact_button = Gtk.Button(contact["author"]["name"])
            contact_button.connect("clicked", self._contact_clicked,
                                   contact["contactId"])
            contact_button.show()
            contacts_list_box.add(contact_button)

    def _contact_clicked(self, widget, contactId):
        GLib.idle_add(App().window.open_private_chat, contactId)
