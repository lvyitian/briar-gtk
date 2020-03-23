# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gio


class Actions:

    # pylint: disable=no-member
    def _setup_action(self, key, parameter, callback):
        action = Gio.SimpleAction.new(key, parameter)
        action.connect("activate", callback)
        self.add_action(action)
