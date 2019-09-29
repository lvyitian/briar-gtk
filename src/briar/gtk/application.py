# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2018 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/lollypop/application.py

from gi.repository import Gdk, Gio, GLib, Gtk

from briar.api.api import Api

from briar.gtk.define import APPLICATION_ID, APPLICATION_NAME
from briar.gtk.define import BRIAR_HEADLESS_JAR
from briar.gtk.window import Window


class Application(Gtk.Application):

    def __init__(self):
        Application._set_application_name()
        super().__init__(application_id=APPLICATION_ID)

    # pylint: disable=arguments-differ
    def do_startup(self):
        Gtk.Application.do_startup(self)
        Application._setup_styling()
        self._setup_api()

    # pylint: disable=arguments-differ
    def do_activate(self):
        self._setup_window()

    # pylint: disable=arguments-differ
    def quit(self):
        self.api.stop()
        self.window.hide()
        Gio.Application.quit(self)

    @staticmethod
    def _set_application_name():
        GLib.set_application_name(APPLICATION_NAME)
        GLib.set_prgname(APPLICATION_NAME)

    @staticmethod
    def _setup_styling():
        css_provider_file = Gio.File.new_for_uri(
            "resource:///app/briar/gtk/ui/application.css")
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(css_provider_file)

        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def _setup_api(self):
        self.api = Api(BRIAR_HEADLESS_JAR)

    # pylint: disable=access-member-before-definition
    def _setup_window(self):
        if not hasattr(self, "window") or self.window is None:
            self.window = Window()
            self.window.show()
        self.window.present()
