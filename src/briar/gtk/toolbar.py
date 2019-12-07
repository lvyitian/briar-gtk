# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2019 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.12/lollypop/toolbar.py

from gi.repository import Gtk

from briar.gtk.define import APPLICATION_NAME


class Toolbar(Gtk.HeaderBar):

    TOOLBAR_UI = "/app/briar/gtk/ui/toolbar_start.ui"

    def __init__(self):
        super().__init__()
        self._setup_builder()
        self._setup_toolbar()

    def show_add_contact_button(self, show, callback=None):
        add_contact_button = self._builder.get_object("add_contact_button")
        if not show:
            add_contact_button.hide()
            return
        if callback is None:
            raise Exception("Callback needed when showing add contact button")
        add_contact_button.show()
        add_contact_button.connect("clicked", callback)

    def show_back_button(self, show, callback=None):
        back_button = self._builder.get_object("back_button")
        if not show:
            back_button.hide()
            return
        if callback is None:
            raise Exception("Callback needed when showing back button")
        back_button.show()
        back_button.connect("clicked", callback)

    def _setup_builder(self):
        self._builder = Gtk.Builder()

    def _setup_toolbar(self):
        self.set_title(APPLICATION_NAME)

        self._builder.add_from_resource(self.TOOLBAR_UI)
        toolbar_start = self._builder.get_object("toolbar_start")
        self.pack_start(toolbar_start)
