# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.actions.actions import Actions
from briar_gtk.actions.prefixes import REGISTRATION_PREFIX


class RegistrationActions(Actions):

    def __init__(self, widget):
        super().__init__(widget)
        self._setup_simple_action_group(REGISTRATION_PREFIX)
        self._setup_actions()

    def _setup_actions(self):
        self._setup_create_account_action()
        self._setup_proceed_from_nickname_action()
        self._setup_return_from_passwords_action()

    def _setup_create_account_action(self):
        self._setup_action("create-account", None,
                           self._create_account)

    def _setup_proceed_from_nickname_action(self):
        self._setup_action("proceed-from-nickname", None,
                           self._proceed_from_nickname)

    def _setup_return_from_passwords_action(self):
        self._setup_action("return-from-passwords", None,
                           self._return_from_passwords)

    # pylint: disable=unused-argument
    def _create_account(self, action, parameter):
        self.widget.on_create_account_pressed()

    # pylint: disable=unused-argument
    def _proceed_from_nickname(self, action, parameter):
        self.widget.proceed_from_nickname()

    # pylint: disable=unused-argument
    def _return_from_passwords(self, action, parameter):
        self.widget.show_nickname_page()
