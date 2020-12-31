# Copyright (c) 2019-2021 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

import os

from gi.repository import Gtk

from briar_gtk.define import RESOURCES_DIR
from briar_gtk.conversation.conversation_presenter import MainWindowPresenter


class MainWindowView(Gtk.Overlay):

    def __init__(self, window):
        super().__init__()
        self.builder = self._setup_builder()
        self.presenter = MainWindowPresenter(self)
        self._setup_view(window)

    def _setup_builder(self):
        builder = Gtk.Builder.new()
        builder.add_from_resource(
            os.path.join(RESOURCES_DIR, "main_menu.ui")
        )
        builder.add_from_resource(
            os.path.join(RESOURCES_DIR, "chat_menu.ui")
        )
        builder.add_from_resource(
            os.path.join(RESOURCES_DIR, "main_window.ui")
        )
        builder.connect_signals(self)
        return builder

    def _setup_view(self, window):
        self._setup_main_window_stack()
        self._setup_header_bar_stack_holder(window)

    def _setup_main_window_stack(self):
        main_window_stack = self.builder.get_object("main_window_stack")
        main_window_stack.show_all()
        self.add(main_window_stack)
        self.show_all()

    def _setup_header_bar_stack_holder(self, window):
        header_bar_stack_holder = self.builder.get_object(
            "headerbar_stack_holder")
        header_bar_stack_holder.show_all()
        self.builder.get_object("chat_menu_button").hide()
        window.set_titlebar(header_bar_stack_holder)
