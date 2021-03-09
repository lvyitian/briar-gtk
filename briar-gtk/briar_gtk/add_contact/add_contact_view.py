# Copyright (c) 2019-2021 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
import os
from gettext import gettext as _

from gi.repository import Gtk

from briar_wrapper.exception import BriarWrapperException
from briar_wrapper.exceptions.pending_already_exists_contact import \
    PendingContactAlreadyExistsContact
from briar_wrapper.exceptions.pending_already_exists_pending_contact import \
    PendingContactAlreadyExistsPendingContact
from briar_wrapper.exceptions.pending_invalid_link import \
    PendingContactInvalidLinkException
from briar_wrapper.exceptions.pending_invalid_public_key import \
    PendingContactInvalidPublicKeyException
from briar_wrapper.models.contacts import Contacts

from briar_gtk.add_contact.add_contact_actions import AddContactActions
from briar_gtk.actions.prefixes import ADD_CONTACT_PREFIX
from briar_gtk.define import APP, RESOURCES_DIR


class AddContactView(Gtk.Overlay):
    # TODO: Move more logic into AddContactPresenter

    ADD_CONTACT_UI = "add_contact.ui"
    STACK_NAME = "add_contact_flow_stack"
    HEADERS_NAME = "add_contact_flow_headers"

    def __init__(self):
        super().__init__()
        self.builder = Gtk.Builder()
        AddContactActions(self)
        self._setup_view()
        self._load_content()
        self.show_all()

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
        if self._link_is_empty():
            error_message = _("Please enter a link")
            self._show_error_links_page(error_message)
            return
        if self._links_match():
            error_message = _("Enter your contact's link, not your own")
            self._show_error_links_page(error_message)
            return
        link_error_label = self.builder.get_object("link_error_label")
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

    def _show_error_links_page(self, error_message):
        link_error_label = self.builder.get_object("link_error_label")
        link_error_label.set_label(error_message)
        link_error_label.show()

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
        alias = self.alias_entry.get_text()
        their_link = self.their_link_entry.get_text()
        try:
            contacts = Contacts(APP().api)
            contacts.add_pending(their_link, alias)
            APP().window.show_conversation_view()
        except PendingContactInvalidLinkException:
            self.show_links_page()
            error_message = _("Invalid link")
            self._show_error_links_page(error_message)
        except PendingContactInvalidPublicKeyException:
            self.show_links_page()
            error_message = _("Invalid link")
            self._show_error_links_page(error_message)
        except PendingContactAlreadyExistsContact as exception:
            self._handle_existing_contact(exception.remote_author_name, alias)
        except PendingContactAlreadyExistsPendingContact as exception:
            self._handle_existing_pending_contact(exception, alias, their_link)
        except BriarWrapperException:
            self.show_links_page()
            error_message = _("There was an error adding the contact")
            self._show_error_links_page(error_message)

    def _handle_existing_contact(self, existing_contact_name, alias):
        callback = lambda widget, response_id: \
            self._handle_existing_contact_same_person(
                widget, response_id, existing_contact_name, alias)
        self._show_same_link_dialog(existing_contact_name, alias, callback)

    def _handle_existing_contact_same_person(self, widget, response_id,
                                             existing_contact_name, alias):
        if response_id == Gtk.ResponseType.YES:
            message = _("Contact %s already exists") % existing_contact_name
            confirmation_dialog = Gtk.MessageDialog(
                transient_for=APP().window,
                flags=Gtk.DialogFlags.MODAL,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=message,
            )
            confirmation_dialog.connect("response", self._on_final_dialog)
            confirmation_dialog.show_all()
            widget.destroy()
        elif response_id == Gtk.ResponseType.NO:
            self._show_warning_dialog(existing_contact_name, alias)
            widget.destroy()

    def _handle_existing_pending_contact(self, exception, alias, link):
        callback = lambda widget, response_id: \
            self._handle_existing_pending_contact_same_person(
                widget, response_id, exception, alias, link)
        self._show_same_link_dialog(exception.pending_contact_alias, alias,
                                    callback)

    # pylint: disable=too-many-arguments
    def _handle_existing_pending_contact_same_person(self, widget, response_id,
                                                     exception, alias, link):
        if response_id == Gtk.ResponseType.YES:
            widget.destroy()
            message = _("Pending contact updated")
            try:
                contacts = Contacts(APP().api)
                contacts.delete_pending(exception.pending_contact_id)
                contacts.add_pending(link, alias)
            except BriarWrapperException:
                message = _(
                    "An error occurred while updating the pending contact")
            confirmation_dialog = Gtk.MessageDialog(
                transient_for=APP().window,
                flags=Gtk.DialogFlags.MODAL,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=message,
            )
            confirmation_dialog.connect("response", self._on_final_dialog)
            confirmation_dialog.show_all()
        elif response_id == Gtk.ResponseType.NO:
            self._show_warning_dialog(exception.pending_contact_alias, alias)
            widget.destroy()

    @staticmethod
    def _show_same_link_dialog(existing_name, alias_name, callback):
        confirmation_dialog = Gtk.MessageDialog(
            transient_for=APP().window,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Duplicate Link"),
        )
        message = _(
            "You already have a pending contact with this link: %s") % (
                      existing_name)
        message = message + "\n\n" + _("Are %s and %s the same person?") % (
            alias_name, existing_name)
        confirmation_dialog.format_secondary_text(message)

        confirmation_dialog.connect("response", callback)
        confirmation_dialog.show_all()

    def _show_warning_dialog(self, name1, name2):
        confirmation_dialog = Gtk.MessageDialog(
            transient_for=APP().window,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=_("Duplicate Link"),
        )
        message = _(
            "%s and %s sent you the same link.\n\nOne of them may be trying to discover who your contacts are.\n\nDon\'t tell them you received the same link from someone else.") % (name1, name2)  # noqa
        confirmation_dialog.format_secondary_text(message)

        confirmation_dialog.connect("response", self._on_final_dialog)
        confirmation_dialog.show_all()

    @staticmethod
    def _on_final_dialog(widget, response_id):
        widget.destroy()
        APP().window.show_conversation_view()
