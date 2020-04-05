# Copyright (c) 2014-2020 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.2.20/lollypop/application_actions.py

from briar_gtk.actions.actions import Actions
from briar_gtk.actions.prefixes import APPLICATION_PREFIX


class ApplicationActions(Actions):

    def __init__(self, widget):
        super().__init__(widget)
        self._setup_global_action_group()
        self._setup_actions()

    def _setup_actions(self):
        self._setup_quit_action()

    def _setup_quit_action(self):
        self._setup_action("quit", None, self._quit)
        self.widget.set_accels_for_action(
            f"{APPLICATION_PREFIX}.quit", ["<Ctrl>q"]
        )

    # pylint: disable=unused-argument
    def _quit(self, action, parameter):
        self.widget.quit()
