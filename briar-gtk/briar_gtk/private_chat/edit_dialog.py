# Copyright (c) 2020 Jan Luttermann
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from gettext import gettext as _
from gi.repository import Gtk


class EditDialogWidget(Gtk.Dialog):

    def __init__(self, parent: "Gtk.Window", flags: "Gtk.DialogFlags",
                 placeholder: str, text: str = ""):
        Gtk.Dialog.__init__(
            self,
            transient_for=parent,
            flags=flags
        )
        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            _("Change"),
            Gtk.ResponseType.OK
        )
        self.set_default_size(150, 100)

        self._alias_entry = Gtk.Entry()
        self._alias_entry.set_text(placeholder)
        self._alias_entry.set_size_request(250, 0)

        dialog_box = self.get_content_area()

        dialog_text = Gtk.Label(label=text)
        dialog_box.add(dialog_text)

        dialog_box.add(self._alias_entry)
        self.show_all()

    def get_entry(self) -> "Gtk.Entry":
        return self._alias_entry
