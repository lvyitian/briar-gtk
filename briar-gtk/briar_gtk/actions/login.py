# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.actions.actions import Actions


# pylint: disable=too-few-public-methods
class LoginActions(Actions):

    ACTIONS_PREFIX = "login"

    def __init__(self, widget):
        super().__init__(widget)
        self._setup_simple_action_group(self.ACTIONS_PREFIX)
        self._setup_actions()

    def _setup_actions(self):
        self._setup_login_action()

    def _setup_login_action(self):
        self._setup_action("login", None, self._login)

    # pylint: disable=unused-argument
    def _login(self, action, parameter):
        self.widget._on_login_pressed()
