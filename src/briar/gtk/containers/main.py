# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.models.contacts import Contacts
from briar.gtk.container import Container
from briar.gtk.define import App

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, GObject, Gtk


class MainContainer(Container):

    def __init__(self):
        super().__init__()
        self._api = App().api
        self._register_signals()
        self._setup_view()
        self._load_content()

    def _register_signals(self):
        GObject.signal_new("briar_open_private_chat", Gtk.Overlay,
                           GObject.SignalFlags.RUN_LAST, GObject.TYPE_BOOLEAN,
                           (GObject.TYPE_STRING,))

    def _setup_view(self):
        self.builder.add_from_resource("/app/briar/gtk/ui/main.ui")
        self.add(self.builder.get_object("contacts_list"))
        self.builder.connect_signals(self)

    def _load_content(self):
        contacts = Contacts(self._api)
        contacts_list = contacts.get()
        contacts_list_box = self.builder.get_object("contacts_list")
        for contact in contacts_list:
            contact_label = Gtk.Button(contact["author"]["name"])
            contact_label.connect("clicked", self._contact_clicked)
            contact_label.show()
            contacts_list_box.add(contact_label)

    def _contact_clicked(self, contact):
        GLib.idle_add(self.emit, "briar_open_private_chat", (contact,))
