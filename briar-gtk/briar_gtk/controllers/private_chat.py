# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.controllers.chat_menu import ChatMenuController
from briar_gtk.views.chat_menu import ChatMenuView


class PrivateChatController():

    def __init__(self, private_chat_view, api):
        self._private_chat_view = private_chat_view
        self._api = api

        self._chat_menu_view = ChatMenuView()
        self._chat_menu_controller = ChatMenuController(
            self._chat_menu_view, api)

        self._load_content()

    def _load_content(self):
        pass
