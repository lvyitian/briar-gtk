# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2018 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/lollypop/application.py

from gi.repository import Gdk, Gio, GLib, Gtk

from briar.api.api import Api

from briar.gtk.window import Window


class Application(Gtk.Application):

    def __init__(self, version):
        GLib.set_application_name("Briar")
        GLib.set_prgname("Briar")
        super().__init__(application_id='app.briar.gtk')
        self.window = None
        self._set_version(version)

    # pylint: disable=arguments-differ
    def do_startup(self):
        Gtk.Application.do_startup(self)

        css_provider_file = Gio.File.new_for_uri(
            "resource:///app/briar/gtk/ui/application.css")
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(css_provider_file)
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.api = Api('/app/briar/briar-headless.jar')

    # pylint: disable=arguments-differ
    def do_activate(self):
        if self.window is None:
            self.window = Window()
            self.window.show()
        self.window.present()

    # pylint: disable=arguments-differ
    def quit(self):
        self.api.stop()
        self.window.hide()
        Gio.Application.quit(self)

    def _set_version(self, version):
        self._version = version
