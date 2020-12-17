# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Fractal
# https://gitlab.gnome.org/GNOME/fractal/-/tags/4.2.2

from gi.repository import Gtk

from briar_gtk.define import APP


class MainWindowView(Gtk.Overlay):

    def __init__(self, builder, window):
        super().__init__()
        self._setup_view(builder, window)

    def _setup_view(self, builder, window):
        self._setup_main_window_stack(builder)
        self._setup_headerbar_stack_holder(builder, window)

    def _setup_main_window_stack(self, builder):
        main_window_stack = builder.get_object("main_window_stack")
        main_window_stack.show_all()
        self.add(main_window_stack)

    def _setup_headerbar_stack_holder(self, builder, window):
        headerbar_stack_holder = builder.get_object("headerbar_stack_holder")
        headerbar_stack_holder.show_all()
        window.set_titlebar(headerbar_stack_holder)
