# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.actions.actions import Actions
from briar_gtk.actions.prefixes import REGISTRATION_PREFIX


# pylint: disable=too-few-public-methods
class RegistrationActions(Actions):

    def __init__(self, widget):
        super().__init__(widget)
        self._setup_simple_action_group(REGISTRATION_PREFIX)
        self._setup_actions()

    def _setup_actions(self):
        self._setup_proceed_from_nickname_action()

    def _setup_proceed_from_nickname_action(self):
        self._setup_action("proceed-from-nickname", None,
                           self._proceed_from_nickname)

    # pylint: disable=unused-argument
    def _proceed_from_nickname(self, action, parameter):
        self.widget.proceed_from_nickname()
