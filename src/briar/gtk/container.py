# Copyright (c) 2019 Nico Alt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from briar.gtk.define import App
from briar.gtk.logger import Logger

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Container(Gtk.Overlay):

    def __init__(self):
        Gtk.Overlay.__init__(self)
        self.__setup_view()

    def __setup_view(self):
        Logger.debug("Api has account: %s", App().api.has_account())
        self.builder = Gtk.Builder()
        if not App().api.has_account():
            self.builder.add_from_resource("/app/briar/gtk/ui/setup.ui")
            self.add(self.builder.get_object("setup"))
        else:
            self.builder.add_from_resource("/app/briar/gtk/ui/login.ui")
            self.add(self.builder.get_object("login"))
        self.builder.connect_signals(self)

    def on_username_button_clicked(self, button):
        self.builder.get_object("username_grid").set_visible(False)
        self.builder.get_object("password_grid").set_visible(True)
        self.username = self.builder.get_object("username_entry").get_text()

    def on_password_button_clicked(self, button):
        password = self.builder.get_object("password_entry").get_text()
        App().api.register((self.username, password))  # TODO: callback

    def on_login_pressed(self, button):
        password = self.builder.get_object("password_entry").get_text()
        App().api.login(password)  # TODO: callback
