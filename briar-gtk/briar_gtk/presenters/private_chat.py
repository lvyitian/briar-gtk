# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import time

from gettext import gettext as _
from gi.repository import Gdk, Gtk, GLib

from briar_wrapper.models.contacts import Contacts
from briar_wrapper.models.private_chat import PrivateChat

from briar_gtk.define import APP
from briar_gtk.widgets.edit_dialog import EditDialog


# pylint: disable=too-many-arguments
class PrivateChatPresenter:

    def __init__(self, private_chat_view, sidebar_presenter):
        self._signals = list()

        # TODO: Move whole sidebar presenter logic into briar_wrapper by
        # notifying sidebar about changes to private chat from model
        self._sidebar_presenter = sidebar_presenter

        self._view = private_chat_view

        self._open_private_chat()

    def open_change_contact_alias_dialog(self):
        if self._view.contact_id == 0:
            raise Exception("Can't change contact alias with ID 0")

        confirmation_dialog = EditDialog(
            parent=APP().window,
            flags=Gtk.DialogFlags.MODAL,
            placeholder=self._get_contact_name(self._view.contact_id)
        )

        confirmation_dialog.set_title(_("Change contact name"))

        response = confirmation_dialog.run()
        user_alias = confirmation_dialog.get_entry().get_text()
        confirmation_dialog.destroy()
        if (response == Gtk.ResponseType.OK) and (user_alias != ''):
            Contacts(APP().api).set_alias(self._view.contact_id, user_alias)
            self._set_contact_name_label(user_alias)
            self._sidebar_presenter.refresh_contacts()
            # TODO: Update name in chat history

    def open_delete_all_messages_dialog(self):
        if self._view.contact_id == 0:
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
        if self._view.contact_id == 0:
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

    def open_emoji_menu(self):
        chat_input = self._view.builder.get_object("chat_input")
        chat_input.emit("insert-emoji")

    def close_private_chat(self):  # formerly `show_sidebar`
        main_content_stack = self._view.builder.get_object(
            "main_content_stack")
        self._hide_chat_view(main_content_stack)
        self._show_chat_placeholder(main_content_stack)
        self._show_sidebar_box()
        self._clear_history_container()
        self._unselect_contact()
        self._set_contact_name_label("")
        self._view.contact_id = 0
        self._hide_chat_menu_button()
        self._disconnect_chat_input_signals()

    def disconnect_signals(self):
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)

    def _open_private_chat(self):
        contact_name = self._get_contact_name(self._view.contact_id)
        self._prepare_chat_view(contact_name)
        self._load_content(contact_name)

    @staticmethod
    def _get_contact_name(contact_id):  # TODO: Move into briar_wrapper
        name = ""
        for contact in Contacts(APP().api).get():
            if contact["contactId"] == contact_id:
                name = contact["author"]["name"]
                if "alias" in contact:
                    name = contact["alias"]
                break
        return name

    def _prepare_chat_view(self, contact_name):
        main_content_stack = self._view.builder.get_object(
            "main_content_stack")

        self._hide_chat_placeholder(main_content_stack)
        self._show_chat_view(main_content_stack)
        self._show_main_content_container()
        self._set_contact_name_label(contact_name)
        self._show_chat_menu_button()

    @staticmethod
    def _hide_chat_placeholder(main_content_stack):
        chat_placeholder = main_content_stack.get_child_by_name(
            "chat_placeholder")
        chat_placeholder.hide()

    @staticmethod
    def _show_chat_view(main_content_stack):
        chat_view = main_content_stack.get_child_by_name("chat_view")
        chat_view.show()

    def _show_main_content_container(self):
        main_window_leaflet = self._view.builder.get_object(
            "main_window_leaflet")
        main_content_container = self._view.builder.get_object(
            "main_content_container")
        main_window_leaflet.set_visible_child(main_content_container)

    def _set_contact_name_label(self, contact_name):
        contact_name_label = self._view.builder.get_object("contact_name")
        contact_name_label.set_text(contact_name)

    def _show_chat_menu_button(self):
        chat_menu_button = self._view.builder.get_object("chat_menu_button")
        chat_menu_button.show()

    def _load_content(self, contact_name):
        private_chat = PrivateChat(APP().api, self._view.contact_id)
        messages = private_chat.get()

        self._view.setup_view(contact_name)
        self._view.show_messages(messages)
        self._setup_message_listener()
        self._mark_messages_read(messages, private_chat)
        self._setup_history_container()
        self._setup_chat_input()

    def _setup_message_listener(self):
        # TODO: Move into briar_wrapper by adding function to PrivateChatModel
        socket_listener = APP().api.socket_listener
        signal_id = socket_listener.connect("ConversationMessageReceivedEvent",
                                            self._view.add_message_async)
        self._signals.append(signal_id)

    @staticmethod
    def _mark_messages_read(messages, private_chat):
        for message in messages:
            if message.get("read", True) is False:
                GLib.idle_add(private_chat.mark_read, message["id"])

    def _setup_history_container(self):
        history_container = self._view.builder.get_object("history_container")
        history_container.add(self._view)
        history_container.show_all()

    def _setup_chat_input(self):
        chat_input = self._view.builder.get_object("chat_input")
        self._chat_input_signal_id = chat_input.connect(
            "key-press-event", self._on_chat_input_activate
        )
        # TODO: Activate vscrollbar only if needed (to save space)
        # https://github.com/dino/dino/blob/231df1/main/src/ui/chat_input/chat_text_view.vala#L51
        chat_input.grab_focus()

    @staticmethod
    def _hide_chat_view(main_content_stack):
        chat_view = main_content_stack.get_child_by_name("chat_view")
        chat_view.hide()

    @staticmethod
    def _show_chat_placeholder(main_content_stack):
        chat_placeholder = main_content_stack.get_child_by_name(
            "chat_placeholder")
        chat_placeholder.show()

    def _unselect_contact(self):
        contacts_list_box = self._view.builder.get_object("contacts_list_box")
        contacts_list_box.unselect_all()

    def _hide_chat_menu_button(self):
        chat_menu_button = self._view.builder.get_object("chat_menu_button")
        chat_menu_button.hide()

    def _show_sidebar_box(self):
        main_window_leaflet = self._view.builder.get_object(
            "main_window_leaflet")
        sidebar_box = self._view.builder.get_object("sidebar_box")
        main_window_leaflet.set_visible_child(sidebar_box)

    def _delete_all_messages(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            private_chat = PrivateChat(APP().api, self._view.contact_id)
            private_chat.delete_all_messages()
            self._sidebar_presenter.refresh_contacts()
            self.close_private_chat()
        widget.destroy()

    def _delete_contact(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            Contacts(APP().api).delete(self._view.contact_id)
            self._sidebar_presenter.refresh_contacts()
            self.close_private_chat()
        widget.destroy()

    def _clear_history_container(self):
        history_container = self._view.builder.get_object("history_container")
        children = history_container.get_children()
        for child in children:
            child.destroy()

    def _disconnect_chat_input_signals(self):
        if not hasattr(self, "_chat_input_signal_id"):
            return
        chat_input = self._view.builder.get_object("chat_input")
        chat_input.disconnect(self._chat_input_signal_id)
        del self._chat_input_signal_id

    def _on_chat_input_activate(self, widget, event):
        # Return is pressed
        if Gdk.keyval_name(event.keyval) != 'Return':
            return False
        # Shift is not pressed
        if (event.state & Gdk.ModifierType.SHIFT_MASK) == Gdk.ModifierType.SHIFT_MASK:  # noqa
            return False
        # Text does not only contain whitespace
        if len(self._get_text_from_text_view(widget).strip()) == 0:
            return False
        self._send_message(widget)
        self._sidebar_presenter.refresh_contacts()
        return True

    @staticmethod
    def _get_text_from_text_view(widget):
        text_buffer = widget.get_buffer()
        start_iter = text_buffer.get_start_iter()
        end_iter = text_buffer.get_end_iter()
        return text_buffer.get_text(start_iter, end_iter, True)

    def _send_message(self, widget):
        message = self._get_text_from_text_view(widget)
        private_chat = PrivateChat(APP().api, self._view.contact_id)
        private_chat.send(message)

        # TODO: Move into briar_wrapper by emitting event on private_chat.send
        self._view.add_message(
            {
                "text": message,
                "local": True,
                "sent": False,
                "seen": False,

                # TODO: Remove once web events updating is implemented
                "no_stored_indicator": True,

                "timestamp": int(round(time.time() * 1000))
            })
        widget.get_buffer().set_text("")
        GLib.idle_add(self._view.scroll_to_bottom)
