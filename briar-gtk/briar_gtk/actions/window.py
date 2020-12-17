# Copyright (c) 2014-2020 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.2.20/lollypop/application_actions.py

from gi.repository import GLib

from briar_gtk.actions.actions import Actions
from briar_gtk.actions.prefixes import WINDOW_PREFIX
from briar_gtk.views.main_window import MainWindowView
from briar_gtk.define import APP


class WindowActions(Actions):

    def __init__(self, widget):
        super().__init__(widget)
        self._setup_global_action_group()
        self._setup_actions()

    def _setup_actions(self):
        self._setup_back_to_sidebar_action()
        self._setup_delete_all_messages_action()
        self._setup_delete_contact_action()
        self._setup_change_alias_contact_action()
        self._setup_open_about_page_action()
        self._setup_open_add_contact_action()
        self._setup_open_main_window_action()
        self._setup_open_private_chat_action()

    def _setup_back_to_sidebar_action(self):
        self._setup_action("back-to-sidebar", None, self._back_to_sidebar)
        APP().set_accels_for_action(
            f"{WINDOW_PREFIX}.back-to-sidebar", ["<Ctrl>w"]
        )

    def _setup_delete_all_messages_action(self):
        self._setup_action("delete-all-messages-dialog", None,
                           self._delete_all_messages_dialog)

    def _setup_delete_contact_action(self):
        self._setup_action("delete-contact-dialog", None,
                           self._delete_contact_dialog)

    def _setup_change_alias_contact_action(self):
        self._setup_action("change-alias-contact-dialog", None,
                           self._change_alias_contact_dialog)

    def _setup_open_about_page_action(self):
        self._setup_action("open-about-dialog", None, self._open_about_page)

    def _setup_open_add_contact_action(self):
        self._setup_action("open-add-contact", None, self._open_add_contact)

    def _setup_open_main_window_action(self):
        self._setup_action("open-main-window", None, self._open_main_window)

    def _setup_open_private_chat_action(self):
        self._setup_action("open-private-chat", GLib.VariantType.new("i"),
                           self._open_private_chat)

    # pylint: disable=unused-argument
    def _back_to_sidebar(self, action, parameter):
        if isinstance(self.widget.current_container, MainWindowView):
            self.widget.current_container.show_sidebar()

    # pylint: disable=unused-argument
    def _delete_all_messages_dialog(self, action, parameter):
        self.widget.current_container.open_delete_all_messages_dialog()

    # pylint: disable=unused-argument
    def _delete_contact_dialog(self, action, parameter):
        self.widget.current_container.open_delete_contact_dialog()

    # pylint: disable=unused-argument
    def _change_alias_contact_dialog(self, action, parameter):
        self.widget.current_container.open_change_contact_alias_dialog()

    # pylint: disable=unused-argument
    def _open_about_page(self, action, parameter):
        self.widget.current_controller.open_about_page()

    # pylint: disable=unused-argument
    def _open_add_contact(self, action, parameter):
        self.widget.show_add_contact_container()

    # pylint: disable=unused-argument
    def _open_main_window(self, action, parameter):
        self.widget.show_main_container()

    # pylint: disable=unused-argument
    def _open_private_chat(self, action, contact_id):
        self.widget.current_controller.open_private_chat(contact_id.get_int32())
