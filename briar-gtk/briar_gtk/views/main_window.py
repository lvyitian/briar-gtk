# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

from gettext import gettext as _
from gi.repository import Gio, GLib, Gtk

from briar_wrapper.models.contacts import Contacts
from briar_wrapper.models.private_chat import PrivateChat

from briar_gtk.containers.private_chat import PrivateChatContainer
from briar_gtk.controllers.main_menu import MainMenuController
from briar_gtk.controllers.private_chat import PrivateChatController
from briar_gtk.controllers.sidebar import SidebarController
from briar_gtk.define import APP, NOTIFICATION_CONTACT_ADDED
from briar_gtk.define import NOTIFICATION_PRIVATE_MESSAGE
from briar_gtk.views.main_menu import MainMenuView
from briar_gtk.views.private_chat import PrivateChatView
from briar_gtk.views.sidebar import SidebarView
from briar_gtk.widgets.about_dialog import AboutDialogWidget
from briar_gtk.widgets.contact_row import ContactRowWidget
from briar_gtk.widgets.edit_dialog import EditDialog


class MainWindowView(Gtk.Overlay):

    _current_contact_id = 0
    _current_private_chat_widget = None

    def __init__(self, builder):
        super().__init__()
        self._builder = builder

        self._setup_view()

    @property
    def main_window_leaflet(self):
        return self._builder.get_object("main_window_leaflet")

    @property
    def contact_name_label(self):
        return self._builder.get_object("contact_name")

    @property
    def contacts_list_box(self):
        return self._builder.get_object("contacts_list_box")

    @property
    def main_content_stack(self):
        return self._builder.get_object("main_content_stack")

    @property
    def main_content_container(self):
        return self._builder.get_object("main_content_container")

    @property
    def chat_placeholder(self):
        return self.main_content_stack.get_child_by_name("chat_placeholder")

    @property
    def chat_view(self):
        return self.main_content_stack.get_child_by_name("chat_view")

    @property
    def history_container(self):
        return self._builder.get_object("history_container")

    @property
    def chat_entry(self):
        return self._builder.get_object("chat_entry")

    @staticmethod
    def open_about_page():
        about_dialog = AboutDialogWidget()
        about_dialog.show()

    def show_sidebar(self):
        self.main_window_leaflet.set_visible_child(
            self._builder.get_object("sidebar_box"))
        self.chat_view.hide()
        self.chat_placeholder.show()
        self._clear_history_container()
        self.contacts_list_box.unselect_all()
        self.contact_name_label.set_text("")
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
            self.contact_name_label.set_text(user_alias)
            self._refresh_contacts()

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

    def _delete_all_messages(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            private_chat = PrivateChat(APP().api, self._current_contact_id)
            private_chat.delete_all_messages()
            self._refresh_contacts()
            self.show_sidebar()
        widget.destroy()

    def _delete_contact(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            Contacts(APP().api).delete(self._current_contact_id)
            self._refresh_contacts()
            self.show_sidebar()
        widget.destroy()

    def _disconnect_chat_entry_signals(self):
        if not hasattr(self, "_chat_entry_signal_id"):
            return
        self.chat_entry.disconnect(self._chat_entry_signal_id)
        del self._chat_entry_signal_id

    def _clear_history_container(self):
        children = self.history_container.get_children()
        for child in children:
            child.destroy()
        if hasattr(self, "_selected_contact"):
            del self._selected_contact

    def _setup_view(self):
        self._setup_main_window_stack()
        self._setup_headerbar_stack_holder()

    def _setup_main_window_stack(self):
        main_window_stack = self._builder.get_object("main_window_stack")
        main_window_stack.show_all()
        self.add(main_window_stack)

    def _setup_headerbar_stack_holder(self):
        headerbar_stack_holder = self._builder.get_object(
            "headerbar_stack_holder")
        headerbar_stack_holder.show_all()
        APP().window.set_titlebar(headerbar_stack_holder)

    def _refresh_contacts(self):
        self._sidebar_controller.refresh_contacts()
