# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gtk

from briar_gtk.views.login import LoginView
from briar_gtk.views.registration import RegistrationView
from briar_gtk.define import APP


class StartupView(Gtk.Overlay):

    def __init__(self, window):
        super().__init__()
        self._setup_view(window)

    def _setup_view(self, window):
        container = RegistrationView(window)
        if APP().api.has_account():
            container = LoginView(window)

        self.add(container)