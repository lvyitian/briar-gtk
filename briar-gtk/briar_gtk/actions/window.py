# Copyright (c) 2014-2020 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.2.20/lollypop/application_actions.py

from gi.repository import Gio, GLib

from briar_gtk.containers.main_window import MainWindowContainer
from briar_gtk.define import APP


# pylint: disable=too-few-public-methods
class WindowActions:

    def __init__(self):
        self._setup_actions()

    # pylint: disable=no-member
    def _setup_actions(self):
        back_to_sidebar_action = Gio.SimpleAction.new(
            "back-to-sidebar", None)
        back_to_sidebar_action.connect("activate", self._back_to_sidebar)
        APP().set_accels_for_action("win.back-to-sidebar", ["<Ctrl>w"])
        self.add_action(back_to_sidebar_action)

        open_add_contact_action = Gio.SimpleAction.new(
            "open-add-contact", None)
        open_add_contact_action.connect("activate", self._open_add_contact)
        self.add_action(open_add_contact_action)

        open_about_page_action = Gio.SimpleAction.new(
            "open-about-page", None)
        open_about_page_action.connect("activate", self._open_about_page)
        self.add_action(open_about_page_action)

        open_private_chat_action = Gio.SimpleAction.new(
            "open-private-chat", GLib.VariantType.new("i"))
        open_private_chat_action.connect("activate", self._open_private_chat)
        self.add_action(open_private_chat_action)

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
