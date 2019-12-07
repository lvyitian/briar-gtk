# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import GLib

from briar.api.models.contacts import Contacts
from briar.gtk.container import Container
from briar.gtk.define import APP


class AddContactContainer(Container):

    CONTAINER_UI = "/app/briar/gtk/ui/add_contact.ui"

    def __init__(self):
        super().__init__()
        self._api = APP().api
        self._setup_view()
        self._load_content()

    def _setup_view(self):
        self.builder.add_from_resource(self.CONTAINER_UI)
        self.add(self.builder.get_object("add_contact"))
        self.builder.connect_signals(self)

    def _load_content(self):
        contacts = Contacts(self._api)
        own_link = contacts.get_link()
        self.builder.get_object("own_link_entry").set_text(own_link)

    # pylint: disable=unused-argument
    def on_link_button_clicked(self, button):
        self.builder.get_object("link_grid").set_visible(False)
        self.builder.get_object("alias_grid").set_visible(True)

    # pylint: disable=unused-argument
    def on_add_contact_button_clicked(self, button):
        their_link = self.builder.get_object("their_link_entry").get_text()
        alias = self.builder.get_object("alias_entry").get_text()
        contacts = Contacts(self._api)
        contacts.add_pending(their_link, alias)
        GLib.idle_add(APP().window.back_to_main, None)
