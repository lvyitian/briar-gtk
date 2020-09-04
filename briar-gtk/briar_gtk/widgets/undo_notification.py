# Copyright (c) 2020 Nico Alt
# Copyright (c) 2014-2020 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/-/blob/1.3.6/lollypop/app_notification.py

from gettext import gettext as _
from gi.repository import Gtk, GLib, Pango


class UndoNotification(Gtk.Revealer):

    _TIMEOUT = 5000

    _execute_action = True

    def __init__(self, message, timeout_action):
        """
        Implementation of
        https://developer.gnome.org/hig/stable/in-app-notifications.html.en

        Parameters
        ==========
        message: str
        timeout_action: callback
        """
        Gtk.Revealer.__init__(self)
        widget = Gtk.Grid()
        widget.get_style_context().add_class("app-notification")
        widget.set_column_spacing(5)
        label = Gtk.Label.new(message)
        label.set_line_wrap_mode(Pango.WrapMode.WORD)
        label.set_line_wrap(True)
        widget.add(label)

        button = Gtk.Button.new()
        button.set_label(_("Undo"))
        button.connect("clicked", self._on_undo_clicked)
        button.set_property("valign", Gtk.Align.START)
        widget.add(button)
        widget.show_all()
        self.add(widget)
        self.set_property("halign", Gtk.Align.CENTER)
        self.set_property("valign", Gtk.Align.START)
        GLib.timeout_add(self._TIMEOUT, self._on_destroy, timeout_action)

    # pylint: disable=unused-argument
    def _on_undo_clicked(self, button, action=None):
        self._execute_action = False
        self.destroy()

    # pylint: disable=unused-argument
    def _on_destroy(self, action):
        if self._execute_action:
            action()
        self.destroy()
