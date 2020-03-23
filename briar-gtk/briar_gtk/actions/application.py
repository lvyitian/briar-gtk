# Copyright (c) 2014-2020 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.2.20/lollypop/application_actions.py

from briar_gtk.action import Actions


# pylint: disable=too-few-public-methods
class ApplicationActions(Actions):

    def __init__(self):
        self._setup_actions()

    def _setup_actions(self):
        self._setup_quit_action()

    # pylint: disable=no-member
    def _setup_quit_action(self):
        self._setup_action("quit", None, self._quit)
        self.set_accels_for_action("app.quit", ["<Ctrl>q"])

    # pylint: disable=unused-argument
    def _quit(self, action, parameter):
        self.quit()
