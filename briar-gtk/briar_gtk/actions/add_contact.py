# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar_gtk.actions.actions import Actions
from briar_gtk.actions.prefixes import ADD_CONTACT_PREFIX


class AddContactActions(Actions):

    def __init__(self, widget):
        super().__init__(widget)
        self._setup_simple_action_group(ADD_CONTACT_PREFIX)
        self._setup_actions()

    def _setup_actions(self):
        self._setup_add_contact_action()
        self._setup_proceed_from_links_action()
        self._setup_return_from_alias_action()

    def _setup_add_contact_action(self):
        self._setup_action("add-contact", None, self._add_contact)

    def _setup_proceed_from_links_action(self):
        self._setup_action("proceed-from-links", None,
                           self._proceed_from_links)

    def _setup_return_from_alias_action(self):
        self._setup_action("return-from-alias", None, self._return_from_alias)

    # pylint: disable=unused-argument
    def _add_contact(self, action, parameter):
        self.widget.on_add_contact_pressed()

    # pylint: disable=unused-argument
    def _proceed_from_links(self, action, parameter):
        self.widget.proceed_from_links()

    # pylint: disable=unused-argument
    def _return_from_alias(self, action, parameter):
        self.widget.show_links_page()
