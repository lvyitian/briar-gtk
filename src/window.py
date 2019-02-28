# window.py
#
# Copyright 2019 Nico Alt
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk
from .gi_composites import GtkTemplate


@GtkTemplate(ui='/app/briar/gtk/window.ui')
class BriarGtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'BriarGtkWindow'

    username_grid = GtkTemplate.Child()
    username_entry = GtkTemplate.Child()

    password_grid = GtkTemplate.Child()
    password_entry = GtkTemplate.Child()
    password_confirm_entry = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

    def on_username_button_clicked(self, button):
        self.username_grid.set_visible(False)
        self.password_grid.set_visible(True)
        self.username = self.username_entry.get_text()

    def on_password_button_clicked(self, button):
        self.password = self.password_entry.get_text()
