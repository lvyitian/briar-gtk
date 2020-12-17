# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gettext import gettext as _
from gi.repository import Gtk

from briar_wrapper.models.contacts import Contacts
from briar_wrapper.models.private_chat import PrivateChat

from briar_gtk.private_chat_container import PrivateChatContainer
from briar_gtk.define import APP
from briar_gtk.widgets.edit_dialog import EditDialog


class PrivateChatController:
    _current_contact_id = 0

    def __init__(self, private_chat_view, sidebar_controller, builder, api):
        self._private_chat_view = private_chat_view
        self._sidebar_controller = sidebar_controller
        self._builder = builder
        self._api = api

    def close_private_chat(self):  # formerly `show_sidebar`
        main_window_leaflet = self._builder.get_object("main_window_leaflet")
        main_window_leaflet.set_visible_child(
            self._builder.get_object("sidebar_box"))

        main_content_stack = self._builder.get_object("main_content_stack")
        chat_view = main_content_stack.get_child_by_name("chat_view")
        chat_view.hide()

        chat_placeholder = main_content_stack.get_child_by_name(
            "chat_placeholder")
        chat_placeholder.show()

        self._clear_history_container()

        contacts_list_box = self._builder.get_object("contacts_list_box")
        contacts_list_box.unselect_all()

        contact_name_label = self._builder.get_object("contact_name")
        contact_name_label.set_text("")

        self._current_contact_id = 0
        self._builder.get_object("chat_menu_button").hide()

    def open_change_contact_alias_dialog(self):
        if self._current_contact_id == 0:
            raise Exception("Can't change contact alias with ID 0")

        confirmation_dialog = EditDialog(
            parent=APP().window,
            flags=Gtk.DialogFlags.MODAL,
            placeholder=self._get_contact_name(self._current_contact_id)
        )

        confirmation_dialog.set_title(_("Change contact name"))

        response = confirmation_dialog.run()
        user_alias = confirmation_dialog.get_entry().get_text()
        confirmation_dialog.destroy()
        if (response == Gtk.ResponseType.OK) and (user_alias != ''):
            Contacts(APP().api).set_alias(self._current_contact_id, user_alias)
            contact_name_label = self._builder.get_object("contact_name")
            contact_name_label.set_text(user_alias)
            self._sidebar_controller.refresh_contacts()

    def open_delete_all_messages_dialog(self):
        if self._current_contact_id == 0:
            raise Exception("Can't delete all messages with contact ID 0")

        confirmation_dialog = Gtk.MessageDialog(
            transient_for=APP().window,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=_("Confirm Message Deletion"),
        )
        confirmation_dialog.format_secondary_text(
            _("Are you sure that you want to delete all messages?")
        )

        confirmation_dialog.connect("response", self._delete_all_messages)
        confirmation_dialog.show_all()

    def open_delete_contact_dialog(self):
        if self._current_contact_id == 0:
            raise Exception("Can't delete contact with ID 0")

        confirmation_dialog = Gtk.MessageDialog(
            transient_for=APP().window,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=_("Confirm Contact Deletion"),
        )
        confirmation_dialog.format_secondary_text(
            _("Are you sure that you want to remove this contact and "
              "all messages exchanged with this contact?")
        )

        confirmation_dialog.connect("response", self._delete_contact)
        confirmation_dialog.show_all()

    def open_private_chat(self, contact_id):
        contact_name = self._get_contact_name(contact_id)
        self._prepare_chat_view(contact_name)
        self._setup_private_chat_widget(contact_name, contact_id)
        self._current_contact_id = contact_id

    @staticmethod
    def _get_contact_name(contact_id):
        name = ""
        for contact in Contacts(APP().api).get():
            if contact["contactId"] == contact_id:
                name = contact["author"]["name"]
                if "alias" in contact:
                    name = contact["alias"]
                break
        return name

    def _delete_all_messages(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            private_chat = PrivateChat(APP().api, self._current_contact_id)
            private_chat.delete_all_messages()
            self._sidebar_controller.refresh_contacts()
            self.close_private_chat()
        widget.destroy()

    def _delete_contact(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            Contacts(APP().api).delete(self._current_contact_id)
            self._sidebar_controller.refresh_contacts()
            self.close_private_chat()
        widget.destroy()

    def _prepare_chat_view(self, contact_name):
        main_content_stack = self._builder.get_object("main_content_stack")
        chat_placeholder = main_content_stack.get_child_by_name(
            "chat_placeholder")
        if self._no_chat_opened():
            chat_placeholder.hide()
        else:
            self._clear_history_container()

        chat_view = main_content_stack.get_child_by_name("chat_view")
        chat_view.show()
        main_window_leaflet = self._builder.get_object("main_window_leaflet")
        main_content_container = self._builder.get_object(
            "main_content_container")
        main_window_leaflet.set_visible_child(main_content_container)
        contact_name_label = self._builder.get_object("contact_name")
        contact_name_label.set_text(contact_name)
        self._builder.get_object("chat_menu_button").show()

    def _no_chat_opened(self):
        main_content_stack = self._builder.get_object("main_content_stack")
        chat_placeholder = main_content_stack.get_child_by_name(
            "chat_placeholder")
        return chat_placeholder.get_visible()

    def _clear_history_container(self):
        history_container = self._builder.get_object("history_container")
        children = history_container.get_children()
        for child in children:
            child.destroy()

    def _setup_private_chat_widget(self, contact_name, contact_id):
        self._current_private_chat_widget = PrivateChatContainer(
            contact_name, contact_id)
        history_container = self._builder.get_object("history_container")
        history_container.add(self._current_private_chat_widget)
        history_container.show_all()

        self._disconnect_chat_entry_signals()
        chat_entry = self._builder.get_object("chat_entry")
        self._chat_entry_signal_id = chat_entry.connect(
            "activate", self._on_chat_entry_activate
        )
        chat_entry.grab_focus()

    def _disconnect_chat_entry_signals(self):
        if not hasattr(self, "_chat_entry_signal_id"):
            return
        chat_entry = self._builder.get_object("chat_entry")
        chat_entry.disconnect(self._chat_entry_signal_id)
        del self._chat_entry_signal_id

    def _on_chat_entry_activate(self, widget):
        if len(widget.get_text()) == 0:
            return
        self._current_private_chat_widget.send_message(widget)
        self._sidebar_controller.refresh_contacts()
