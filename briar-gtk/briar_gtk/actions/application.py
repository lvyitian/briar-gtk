# Copyright (c) 2014-2020 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.2.20/lollypop/application_actions.py

from gi.repository import Gio


# pylint: disable=too-few-public-methods
class ApplicationActions:

    def __init__(self):
        self._setup_actions()

    # pylint: disable=no-member
    def _setup_actions(self):

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self._quit)
        self.set_accels_for_action("app.quit", ["<Ctrl>q"])
        self.add_action(quit_action)

    # pylint: disable=unused-argument
    def _quit(self, action, parameter):
        self.quit()
