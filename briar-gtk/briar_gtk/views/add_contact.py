# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
import os
from gettext import gettext as _
from gi.repository import Gtk

from briar_wrapper.models.contacts import Contacts

from briar_gtk.actions.add_contact import AddContactActions
from briar_gtk.actions.prefixes import ADD_CONTACT_PREFIX
from briar_gtk.define import APP, RESOURCES_DIR


class AddContactView(Gtk.Overlay):

    ADD_CONTACT_UI = "add_contact.ui"
    STACK_NAME = "add_contact_flow_stack"
    HEADERS_NAME = "add_contact_flow_headers"

    def __init__(self):
        super().__init__()
        self.builder = Gtk.Builder()
        AddContactActions(self)
        self._setup_view()
        self._load_content()

    @property
    def alias_entry(self):
        return self.builder.get_object("alias_entry")

    @property
    def own_link_entry(self):
        return self.builder.get_object("own_link_entry")

    @property
    def their_link_entry(self):
        return self.builder.get_object("their_link_entry")

    def proceed_from_links(self):
        link_error_label = self.builder.get_object("link_error_label")
        if self._link_is_empty():
            link_error_label.set_label(_("Please enter a link"))
            link_error_label.show()
            return
        if self._links_match():
            link_error_label.show()
            link_error_label.set_label(
                _("Enter your contact's link, not your own"))
            return
        link_error_label.hide()
        self._show_alias_page()

    def show_links_page(self):
        links_page = self.builder.get_object("links_page")
        self.add_contact_flow_stack.set_visible_child(links_page)

    def on_add_contact_pressed(self):
        alias_error_label = self.builder.get_object(
            "alias_error_label")
        if self._alias_is_empty():
            alias_error_label.show()
            return
        alias_error_label.hide()
        self._add_contact()
        APP().window.show_main_window_view()

    def _setup_view(self):
        self._add_from_resource(self.ADD_CONTACT_UI)
        self.builder.connect_signals(self)

        self._setup_add_contact_flow_stack()
        self._setup_add_contact_flow_headers()
        self._setup_link_enter_listener()

    def _add_from_resource(self, ui_filename):
        self.builder.add_from_resource(
            os.path.join(RESOURCES_DIR, ui_filename)
        )

    def _load_content(self):
        contacts = Contacts(APP().api)
        own_link = contacts.get_link()
        self.own_link_entry.set_text(own_link)

    def _setup_add_contact_flow_stack(self):
        self.add_contact_flow_stack = self.builder.get_object(self.STACK_NAME)
        self.add_contact_flow_stack.show_all()
        self.add(self.add_contact_flow_stack)

    def _setup_add_contact_flow_headers(self):
        add_contact_flow_headers = self.builder.get_object(self.HEADERS_NAME)
        add_contact_flow_headers.show_all()
        add_contact_flow_headers.insert_action_group(
            ADD_CONTACT_PREFIX, self.get_action_group(ADD_CONTACT_PREFIX)
        )
        APP().window.set_titlebar(add_contact_flow_headers)

    def _setup_link_enter_listener(self):
        self.their_link_entry.connect("activate", self._on_link_enter)

    # pylint: disable=unused-argument
    def _on_link_enter(self, widget):
        self.proceed_from_links()

    def _links_match(self):
        their_link = self.their_link_entry.get_text()
        own_link = self.own_link_entry.get_text()
        return their_link == own_link

    def _link_is_empty(self):
        their_link = self.their_link_entry.get_text()
        return len(their_link) == 0

    def _show_alias_page(self):
        alias_page = self.builder.get_object("alias_page")
        self.add_contact_flow_stack.set_visible_child(alias_page)

        self.alias_entry.grab_focus()
        self._setup_alias_enter_listener()

    def _setup_alias_enter_listener(self):
        self.alias_entry.connect("activate", self._on_alias_enter)

    # pylint: disable=unused-argument
    def _on_alias_enter(self, widget):
        self.on_add_contact_pressed()

    def _alias_is_empty(self):
        alias = self.alias_entry.get_text()
        return len(alias) == 0

    def _add_contact(self):
        contacts = Contacts(APP().api)
        their_link = self.their_link_entry.get_text()
        alias = self.alias_entry.get_text()
        contacts.add_pending(their_link, alias)
