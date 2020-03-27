# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import os

from gettext import gettext as _

from gi.repository import Gtk

from briar_gtk.define import APP, RESOURCES_DIR


# pylint: disable=too-few-public-methods
class AboutDialogWidget():

    ABOUT_UI = "about_dialog.ui"

    def __init__(self):
        self._about_dialog = self._load_from_builder()
        self._extend_about_dialog()

    def show(self):
        self._about_dialog.show()

    def _load_from_builder(self):
        builder = Gtk.Builder()
        builder.add_from_resource(os.path.join(RESOURCES_DIR, self.ABOUT_UI))
        return builder.get_object("about_dialog")

    def _extend_about_dialog(self):
        self._about_dialog.set_transient_for(APP().window)
        self._add_code_section()
        self._add_briar_section()
        self._about_dialog.connect("response", self._on_about_response)

    def _add_code_section(self):
        code_use_title = _("Using code by")
        code_use_list = [
            "GNOME Fractal https://wiki.gnome.org/Apps/Fractal",
            "GNOME Lollypop https://wiki.gnome.org/Apps/Lollypop",
        ]
        self._about_dialog.add_credit_section(
            code_use_title, code_use_list
        )

    # pylint: disable=line-too-long
    def _add_briar_section(self):
        briar_functionality_title = _("Briar functionality by")
        briar_functionality_list = [
            "Briar REST API https://code.briarproject.org/briar/briar/tree/master/briar-headless",  # noqa
            "Briar Python Wrapper https://code.briarproject.org/briar/python-briar-wrapper",  # noqa
        ]
        self._about_dialog.add_credit_section(
            briar_functionality_title, briar_functionality_list
        )

    @staticmethod
    # pylint: disable=unused-argument
    def _on_about_response(dialog, response_id):
        dialog.destroy()
