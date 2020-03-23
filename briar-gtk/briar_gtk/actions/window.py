# Copyright (c) 2014-2020 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.2.20/lollypop/application_actions.py

from gi.repository import GLib

from briar_gtk.action import Actions
from briar_gtk.containers.main_window import MainWindowContainer
from briar_gtk.define import APP


# pylint: disable=too-few-public-methods
class WindowActions(Actions):

    def __init__(self):
        self._setup_actions()

    def _setup_actions(self):
        self._setup_back_to_sidebar_action()
        self._setup_open_about_page_action()
        self._setup_open_add_contact_action()
        self._setup_open_private_chat_action()

    def _setup_back_to_sidebar_action(self):
        self._setup_action("back-to-sidebar", None, self._back_to_sidebar)
        APP().set_accels_for_action("win.back-to-sidebar", ["<Ctrl>w"])

    def _setup_open_about_page_action(self):
        self._setup_action("open-about-page", None, self._open_about_page)

    def _setup_open_add_contact_action(self):
        self._setup_action("open-add-contact", None, self._open_add_contact)

    def _setup_open_private_chat_action(self):
        self._setup_action("open-private-chat", GLib.VariantType.new("i"),
                           self._open_private_chat)

    # pylint: disable=unused-argument
    def _back_to_sidebar(self, action, parameter):
        if isinstance(self.current_container, MainWindowContainer):
            self.current_container.show_sidebar()

    # pylint: disable=unused-argument
    def _open_about_page(self, action, parameter):
        self.current_container.open_about_page()

    # pylint: disable=unused-argument
    def _open_add_contact(self, action, parameter):
        self.show_add_contact_container()

    # pylint: disable=unused-argument
    def _open_private_chat(self, action, contact_id):
        self.current_container.open_private_chat(contact_id.get_int32())
