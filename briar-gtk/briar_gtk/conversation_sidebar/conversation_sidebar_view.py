# Copyright (c) 2020-2021 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.define import APP
from briar_gtk.conversation_sidebar.conversation_sidebar_presenter import \
    SidebarPresenter
from briar_gtk.conversation_sidebar.contact_row import ContactRowWidget


class SidebarView:

    def __init__(self, builder):
        self._builder = builder
        self.presenter = SidebarPresenter(self, APP().api)

    def show_contacts(self, contact_list, selected_contact):
        self._clear_contact_list()

        for contact in contact_list:
            contact_row = ContactRowWidget(contact)
            contacts_list_box = self._builder.get_object("contacts_list_box")
            contacts_list_box.add(contact_row)
            if contact["contactId"] == selected_contact:
                contacts_list_box.select_row(contact_row)

    def get_selected_row(self):
        contacts_list_box = self._builder.get_object("contacts_list_box")
        row = contacts_list_box.get_selected_row()
        if row is None:
            return -1
        return row.get_action_target_value().get_int32()

    def _clear_contact_list(self):
        contacts_list_box = self._builder.get_object("contacts_list_box")
        contacts_list_box_children = contacts_list_box.get_children()
        for child in contacts_list_box_children:
            child.destroy()
