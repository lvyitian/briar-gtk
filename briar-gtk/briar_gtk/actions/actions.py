# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gio


# pylint: disable=too-few-public-methods
class Actions:

    def __init__(self, widget):
        self.widget = widget

    @staticmethod
    def _create_action(key, parameter, callback):
        action = Gio.SimpleAction.new(key, parameter)
        action.connect("activate", callback)
        return action

    def _setup_action(self, key, parameter, callback):
        action = self._create_action(key, parameter, callback)
        self.actions.add_action(action)

    def _setup_global_action_group(self):
        self.actions = self.widget

    def _setup_simple_action_group(self, name):
        self.actions = Gio.SimpleActionGroup.new()
        self.widget.insert_action_group(name, self.actions)
