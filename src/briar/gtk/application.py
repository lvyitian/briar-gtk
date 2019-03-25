# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2018 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/lollypop/application.py

from briar.api.api import Api

from briar.gtk.window import Window

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gio, GLib, Gtk


class Application(Gtk.Application):

    def __init__(self, version):
        super().__init__(application_id='app.briar.gtk',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.__version = version
        self.set_property("register-session", True)
        self.window = None
        self.debug = True  # TODO: Change this in production
        GLib.set_application_name("Briar")
        GLib.set_prgname("briar-gtk")
        self.api = Api('/app/briar/briar-headless.jar', self.debug)
        self.connect("activate", self.__on_activate)
        self.register(None)

    def init(self):
        cssProviderFile = Gio.File.new_for_uri(
            "resource:///app/briar/gtk/ui/application.css")
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_file(cssProviderFile)
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        if self.window is None:
            self.init()
            self.window = Window()
            self.window.show()

    def quit(self):
        self.api.stop()
        self.window.hide()
        Gio.Application.quit(self)

    def __on_activate(self, application):
        pass

