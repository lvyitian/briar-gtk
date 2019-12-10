# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gettext import gettext as _

from gi.repository import GLib

from briar.api.models.contacts import Contacts
from briar.gtk.container import Container
from briar.gtk.define import APP


class AddContactContainer(Container):

    ADD_CONTACT_UI = "/app/briar/gtk/ui/add_contact.ui"
    STACK_NAME = "add_contact_flow_stack"
    HEADERS_NAME = "add_contact_flow_headers"

    def __init__(self, window):
        super().__init__()
        self._window = window
        self._setup_view()
        self._load_content()

    def _setup_view(self):
        self.builder.add_from_resource(self.ADD_CONTACT_UI)
        self.builder.connect_signals(self)

        self._setup_add_contact_flow_stack()
        self._setup_add_contact_flow_headers()
        self._setup_link_keystroke_listener()

    def _load_content(self):
        contacts = Contacts(APP().api)
        own_link = contacts.get_link()
        self.builder.get_object("own_link_entry").set_text(own_link)

    def _setup_add_contact_flow_stack(self):
        self.add_contact_flow_stack = self.builder.get_object(self.STACK_NAME)
        self.add_contact_flow_stack.show_all()
        self.add(self.add_contact_flow_stack)

    def _setup_add_contact_flow_headers(self):
        add_contact_flow_headers = self.builder.get_object(self.HEADERS_NAME)
        add_contact_flow_headers.show_all()
        self._window.set_titlebar(add_contact_flow_headers)

    def _setup_link_keystroke_listener(self):
        their_link_entry = self.builder.get_object("their_link_entry")
        their_link_entry.connect("key-press-event",
                                 self._link_keystroke)

    # pylint: disable=unused-argument
    def _link_keystroke(self, widget, event):
        if event.hardware_keycode != 36 and event.hardware_keycode != 104:
            return
        self.on_links_next_pressed(None)

    # pylint: disable=unused-argument
    def on_link_back_pressed(self, button):
        self._back_to_main_window()

    # pylint: disable=unused-argument
    def on_links_next_pressed(self, button):
        link_error_label = self.builder.get_object("link_error_label")
        if self._link_is_empty():
            link_error_label.set_label(_("Please enter a link"))
            link_error_label.show()
            return
        if self._their_link_is_ours():
            link_error_label.show()
            link_error_label.set_label(
                _("Enter your contact's link, not your own"))
            return
        link_error_label.hide()
        self._show_alias_page()

    def _their_link_is_ours(self):
        their_link = self.builder.get_object("their_link_entry").get_text()
        own_link = self.builder.get_object("own_link_entry").get_text()
        return their_link == own_link

    def _link_is_empty(self):
        their_link = self.builder.get_object("their_link_entry").get_text()
        return len(their_link) == 0

    def _show_alias_page(self):
        alias_page = self.builder.get_object("alias_page")
        self.add_contact_flow_stack.set_visible_child(alias_page)

        self._focus_alias_entry()
        self._setup_alias_keystroke_listener()

    def _focus_alias_entry(self):
        alias_entry = self.builder.get_object("alias_entry")
        alias_entry.grab_focus()

    def _setup_alias_keystroke_listener(self):
        alias_entry = self.builder.get_object("alias_entry")
        alias_entry.connect("key-press-event", self._alias_keystroke)

    # pylint: disable=unused-argument
    def _alias_keystroke(self, widget, event):
        if event.hardware_keycode != 36 and event.hardware_keycode != 104:
            return
        self.on_add_contact_pressed(None)

    # pylint: disable=unused-argument
    def on_alias_back_pressed(self, button):
        self._show_links_page()

    def _show_links_page(self):
        links_page = self.builder.get_object("links_page")
        self.add_contact_flow_stack.set_visible_child(links_page)

    # pylint: disable=unused-argument
    def on_add_contact_pressed(self, button):
        alias_error_label = self.builder.get_object(
            "alias_error_label")
        if self._alias_is_empty():
            alias_error_label.show()
            return
        alias_error_label.hide()
        self._add_contact()
        self._back_to_main_window()

    def _alias_is_empty(self):
        alias = self.builder.get_object("alias_entry").get_text()
        return len(alias) == 0

    def _add_contact(self):
        contacts = Contacts(APP().api)
        their_link = self.builder.get_object("their_link_entry").get_text()
        alias = self.builder.get_object("alias_entry").get_text()
        contacts.add_pending(their_link, alias)

    def _back_to_main_window(self):
        GLib.idle_add(self._window.back_to_main, None)
