# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

from gettext import gettext as _
from gi.repository import GLib, Gtk

from briar_wrapper.models.contacts import Contacts

from briar_gtk.container import Container
from briar_gtk.containers.private_chat import PrivateChatContainer
from briar_gtk.define import APP
from briar_gtk.widgets.about_dialog import AboutDialogWidget
from briar_gtk.widgets.contact_row import ContactRowWidget


class MainWindowContainer(Container):

    CONTAINER_UI = "main_window.ui"
    MAIN_MENU_UI = "main_menu.ui"
    CHAT_MENU_UI = "chat_menu.ui"

    _current_contact_id = 0
    _current_private_chat_widget = None

    def __init__(self):
        super().__init__()
        self._signals = list()
        self._setup_view()
        self._load_content()

    @property
    def main_window_leaflet(self):
        return self.builder.get_object("main_window_leaflet")

    @property
    def contact_name_label(self):
        return self.builder.get_object("contact_name")

    @property
    def contacts_list_box(self):
        return self.builder.get_object("contacts_list_box")

    @property
    def main_content_stack(self):
        return self.builder.get_object("main_content_stack")

    @property
    def main_content_container(self):
        return self.builder.get_object("main_content_container")

    @property
    def chat_placeholder(self):
        return self.main_content_stack.get_child_by_name("chat_placeholder")

    @property
    def chat_view(self):
        return self.main_content_stack.get_child_by_name("chat_view")

    @property
    def history_container(self):
        return self.builder.get_object("history_container")

    @property
    def chat_entry(self):
        return self.builder.get_object("chat_entry")

    @staticmethod
    def open_about_page():
        about_dialog = AboutDialogWidget()
        about_dialog.show()

    def open_private_chat(self, contact_id):
        contact_name = self._get_contact_name(contact_id)
        self._prepare_chat_view(contact_name)
        self._setup_private_chat_widget(contact_name, contact_id)
        self._current_contact_id = contact_id

    def show_sidebar(self):
        self.main_window_leaflet.set_visible_child(
            self.builder.get_object("sidebar_box"))
        self.chat_view.hide()
        self.chat_placeholder.show()
        self._clear_history_container()
        self.contacts_list_box.unselect_all()
        self.contact_name_label.set_text("")
        self._current_contact_id = 0

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

    def _delete_contact(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            Contacts(APP().api).delete(self._current_contact_id)
            self._refresh_contacts()
            self.show_sidebar()
        widget.destroy()

    def _prepare_chat_view(self, contact_name):
        if self._no_chat_opened():
            self.chat_placeholder.hide()
        else:
            self._clear_history_container()

        self.chat_view.show()
        self.main_window_leaflet.set_visible_child(
            self.main_content_container)
        self.contact_name_label.set_text(contact_name)
        self.builder.get_object("chat_menu_button").show()

    def _setup_private_chat_widget(self, contact_name, contact_id):
        self._current_private_chat_widget = PrivateChatContainer(
            contact_name, contact_id)
        self.history_container.add(self._current_private_chat_widget)
        self.history_container.show_all()

        self._disconnect_chat_entry_signals()
        self._chat_entry_signal_id = self.chat_entry.connect(
            "activate", self._on_chat_entry_activate
        )
        self.chat_entry.grab_focus()

    def _on_chat_entry_activate(self, widget):
        self._current_private_chat_widget.send_message(widget)
        self._refresh_contacts()

    def _disconnect_chat_entry_signals(self):
        if not hasattr(self, "_chat_entry_signal_id"):
            return
        self.chat_entry.disconnect(self._chat_entry_signal_id)
        del self._chat_entry_signal_id

    def _no_chat_opened(self):
        return self.chat_placeholder.get_visible()

    def _get_contact_name(self, contact_id):
        name = ""
        for contact in self.contacts_list:
            if contact["contactId"] == contact_id:
                name = contact["author"]["name"]
                if "alias" in contact:
                    name = contact["alias"]
                break
        return name

    def _clear_history_container(self):
        children = self.history_container.get_children()
        for child in children:
            child.destroy()
        if hasattr(self, "_selected_contact"):
            del self._selected_contact

    def _setup_view(self):
        self._add_from_resource(self.MAIN_MENU_UI)
        self._add_from_resource(self.CHAT_MENU_UI)
        self._add_from_resource(self.CONTAINER_UI)
        self.builder.connect_signals(self)

        self._setup_main_window_stack()
        self._setup_headerbar_stack_holder()
        self.contact_name_label.set_text("")
        self.builder.get_object("chat_menu_button").hide()
        self._setup_destroy_listener()

    def _setup_main_window_stack(self):
        main_window_stack = self.builder.get_object("main_window_stack")
        main_window_stack.show_all()
        self.add(main_window_stack)

    def _setup_headerbar_stack_holder(self):
        headerbar_stack_holder = self.builder.get_object(
            "headerbar_stack_holder")
        headerbar_stack_holder.show_all()
        APP().window.set_titlebar(headerbar_stack_holder)

    def _setup_destroy_listener(self):
        self.connect("destroy", self._on_destroy)

    # pylint: disable=unused-argument
    def _on_destroy(self, widget):
        self._disconnect_signals()

    def _disconnect_signals(self):
        for signal in self._signals:
            APP().api.socket_listener.disconnect(signal)

    # pylint: disable=no-member
    def _load_content(self):
        self._contacts = Contacts(APP().api)
        self._load_contacts()
        socket_listener = APP().api.socket_listener
        self._setup_contact_added_listeners(socket_listener)
        self._setup_message_received_listeners(socket_listener)
        self._setup_contact_connection_listener(socket_listener)

    def _load_contacts(self):
        self.contacts_list = self._contacts.get()

        selected_contact = -1
        if hasattr(self, "_selected_contact"):
            selected_contact = self._selected_contact

        for contact in self.contacts_list:
            contact_row = ContactRowWidget(contact)
            self.contacts_list_box.add(contact_row)
            if contact["contactId"] == selected_contact:
                self.contacts_list_box.select_row(contact_row)

    def _setup_contact_added_listeners(self, socket_listener):
        signal_id = socket_listener.connect("ContactAddedEvent",
                                            self._refresh_contacts_async)
        self._signals.append(signal_id)
        signal_id = socket_listener.connect("ContactAddedEvent",
                                            self._notify_contact_added)
        self._signals.append(signal_id)

    def _setup_message_received_listeners(self, socket_listener):
        signal_id = socket_listener.connect("ConversationMessageReceivedEvent",
                                            self._refresh_contacts_async)
        self._signals.append(signal_id)
        signal_id = socket_listener.connect("ConversationMessageReceivedEvent",
                                            self._notify_message_received)
        self._signals.append(signal_id)

    def _setup_contact_connection_listener(self, socket_listener):
        callback = self._refresh_contact_connection_state
        signal_ids = self._contacts.watch_connections(callback)
        self._signals.extend(signal_ids)

    # pylint: disable=unused-argument
    def _refresh_contacts_async(self, message):
        GLib.idle_add(self._refresh_contacts)

    # pylint: disable=unused-argument
    def _refresh_contact_connection_state(self, contact_id, connected):
        self._refresh_contacts_async(None)

    # pylint: disable=unused-argument
    def _notify_contact_added(self, message):
        self._notify()

    # pylint: disable=unused-argument
    def _notify_message_received(self, message):
        self._notify()

    @staticmethod
    def _notify():
        APP().window.set_urgency_hint(True)

    def _refresh_contacts(self):
        self._save_selected_row()
        self._clear_contact_list()
        self._load_contacts()

    def _save_selected_row(self):
        row = self.contacts_list_box.get_selected_row()
        if row is None:
            return
        self._selected_contact = row.get_action_target_value().get_int32()

    def _clear_contact_list(self):
        contacts_list_box_children = self.contacts_list_box.get_children()
        for child in contacts_list_box_children:
            child.destroy()
