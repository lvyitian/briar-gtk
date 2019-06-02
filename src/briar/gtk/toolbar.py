# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2019 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.12/lollypop/toolbar.py

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Toolbar(Gtk.HeaderBar):

    def __init__(self):
        super().__init__()
        self._builder = Gtk.Builder()
        self._builder.add_from_resource("/app/briar/gtk/ui/toolbar_start.ui")
        toolbar_start = self._builder.get_object("toolbar_start")
        self.set_title("Briar")
        self.pack_start(toolbar_start)

    def show_back_button(self, show, callback=None):
        back_button = self._builder.get_object("back_button")
        if not show:
            back_button.hide()
            return
        if callback is None:
            raise Exception("Callback needed when showing back button")
        back_button.show()
        back_button.connect("clicked", callback)

