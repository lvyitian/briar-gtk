# Copyright (c) 2019-2021 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gi.repository import Gtk

from briar_gtk.startup.login_view import LoginView
from briar_gtk.startup.registration_view import RegistrationView
from briar_gtk.define import APP


class StartupView(Gtk.Overlay):

    def __init__(self, window):
        super().__init__()
        self._setup_view(window)
        self.show_all()

    def _setup_view(self, window):
        container = RegistrationView(window)
        if APP().api.has_account():
            container = LoginView(window)

        self.add(container)
