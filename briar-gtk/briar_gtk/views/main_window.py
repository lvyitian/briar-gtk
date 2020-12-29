# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

import os

from gi.repository import Gtk

from briar_gtk.define import RESOURCES_DIR
from briar_gtk.presenters.main_window import MainWindowPresenter


class MainWindowView(Gtk.Overlay):

    def __init__(self, window):
        super().__init__()
        builder = self._setup_builder()
        self.presenter = MainWindowPresenter(self, builder)
        self._setup_view(builder, window)
        self.show_all()
        builder.get_object("chat_menu_button").hide()  # TODO: Make default

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

    def _setup_view(self, builder, window):
        self._setup_main_window_stack(builder)
        self._setup_headerbar_stack_holder(builder, window)

    def _setup_main_window_stack(self, builder):
        main_window_stack = builder.get_object("main_window_stack")
        main_window_stack.show_all()
        self.add(main_window_stack)
        builder.get_object("chat_menu_button").hide()

    @staticmethod
    def _setup_headerbar_stack_holder(builder, window):
        headerbar_stack_holder = builder.get_object("headerbar_stack_holder")
        headerbar_stack_holder.show_all()
        window.set_titlebar(headerbar_stack_holder)
