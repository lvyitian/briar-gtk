# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

from gi.repository import GLib

from briar_wrapper.models.contacts import Contacts

from briar_gtk.container import Container
from briar_gtk.containers.private_chat import PrivateChatContainer
from briar_gtk.define import APP
from briar_gtk.widgets.about_dialog import AboutDialogWidget
from briar_gtk.widgets.contact_row import ContactRowWidget


class MainWindowContainer(Container):

    CONTAINER_UI = "main_window.ui"
    MENU_UI = "main_menu.ui"

    def __init__(self):
        super().__init__()
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

    def show_sidebar(self):
        self.main_window_leaflet.set_visible_child(
            self.builder.get_object("sidebar_box"))
        self.chat_view.hide()
        self.chat_placeholder.show()
        self._clear_history_container()
        self.contacts_list_box.unselect_all()
        self.contact_name_label.set_text("")

    def _prepare_chat_view(self, contact_name):
        if self._no_chat_opened():
            self.chat_placeholder.hide()
        else:
            self._clear_history_container()

        self.chat_view.show()
        self.main_window_leaflet.set_visible_child(
            self.main_content_container)
        self.contact_name_label.set_text(contact_name)

    def _setup_private_chat_widget(self, contact_name, contact_id):
        private_chat_widget = PrivateChatContainer(contact_name, contact_id)
        self.history_container.add(private_chat_widget)
        self.history_container.show_all()

        self._disconnect_chat_entry_signals()
        self._chat_entry_signal_id = self.chat_entry.connect(
            "activate", private_chat_widget.send_message
        )
        self.chat_entry.grab_focus()

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
            if contact["contactId"] is contact_id:
                name = contact["author"]["name"]
                if "alias" in contact:
                    name = contact["alias"]
                break
        return name

    def _clear_history_container(self):
        children = self.history_container.get_children()
        for child in children:
            self.history_container.remove(child)

    def _setup_view(self):
        self._add_from_resource(self.MENU_UI)
        self._add_from_resource(self.CONTAINER_UI)
        self.builder.connect_signals(self)

        self._setup_main_window_stack()
        self._setup_headerbar_stack_holder()
        self.contact_name_label.set_text("")

    def _setup_main_window_stack(self):
        main_window_stack = self.builder.get_object("main_window_stack")
        main_window_stack.show_all()
        self.add(main_window_stack)

    def _setup_headerbar_stack_holder(self):
        headerbar_stack_holder = self.builder.get_object(
            "headerbar_stack_holder")
        headerbar_stack_holder.show_all()
        APP().window.set_titlebar(headerbar_stack_holder)

    def _load_content(self):
        self._contacts = Contacts(APP().api)
        self._load_contacts()
        self._contacts.watch_contacts(self._refresh_contacts_async)

    def _load_contacts(self):
        self.contacts_list = self._contacts.get()
        for contact in self.contacts_list:
            contact_row = ContactRowWidget(contact)
            self.contacts_list_box.add(contact_row)

    def _refresh_contacts_async(self):
        GLib.idle_add(self._refresh_contacts)

    def _refresh_contacts(self):
        self._clear_contact_list()
        self._load_contacts()

    def _clear_contact_list(self):
        contacts_list_box_children = self.contacts_list_box.get_children()
        for child in contacts_list_box_children:
            self.contacts_list_box.remove(child)
