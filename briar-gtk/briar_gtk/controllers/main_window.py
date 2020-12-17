# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.controllers.main_menu import MainMenuController
from briar_gtk.controllers.private_chat import PrivateChatController
from briar_gtk.controllers.sidebar import SidebarController
from briar_gtk.define import APP
from briar_gtk.views.main_menu import MainMenuView
from briar_gtk.views.private_chat import PrivateChatView
from briar_gtk.views.sidebar import SidebarView


class MainWindowController():

    def __init__(self, main_window_view, builder):
        self._main_window_view = main_window_view
        self._builder = builder

        self._setup_children()

    def _setup_children(self):
        self._sidebar_view = SidebarView(self._builder)
        self._sidebar_controller = SidebarController(
            self._sidebar_view, APP().api)

        self._private_chat_view = PrivateChatView(self._builder)
        self._private_chat_controller = PrivateChatController(
            self._private_chat_view, APP().api)

        self._main_menu_view = MainMenuView()
        self._main_menu_controller = MainMenuController(
            self._main_menu_view, APP().api)
