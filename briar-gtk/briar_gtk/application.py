# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2018 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/lollypop/application.py

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gdk, Gio, GLib, Gtk, Handy

from briar_wrapper.api import Api

from briar_gtk.actions.application import ApplicationActions
from briar_gtk.define import APPLICATION_ID, APPLICATION_NAME
from briar_gtk.define import APPLICATION_STYLING_PATH, get_briar_headless_jar
from briar_gtk.window import Window


class Application(Gtk.Application):

    def __init__(self):
        Application._set_application_name(APPLICATION_NAME)
        super().__init__(application_id=APPLICATION_ID)
        ApplicationActions(self)

    # pylint: disable=arguments-differ
    def do_startup(self):
        Gtk.Application.do_startup(self)
        Application._setup_styling(APPLICATION_STYLING_PATH)
        Handy.init()
        self._setup_api()

    # pylint: disable=arguments-differ
    def do_activate(self):
        self._setup_window()

    # pylint: disable=arguments-differ
    def do_shutdown(self):
        self.api.stop()
        self.window.hide()
        Gio.Application.do_shutdown(self)

    @staticmethod
    def _set_application_name(name):
        GLib.set_application_name(name)
        GLib.set_prgname(name)

    @staticmethod
    def _setup_styling(styling_path):
        css_provider_file = Gio.File.new_for_uri(styling_path)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(css_provider_file)

        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def _setup_api(self):
        self.api = Api(get_briar_headless_jar())

    # pylint: disable=access-member-before-definition
    def _setup_window(self):
        if not hasattr(self, "window") or self.window is None:
            self.window = Window()
            self.window.show()
        self.window.present()
