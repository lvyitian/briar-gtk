# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import os

from gettext import gettext as _
from gi.repository import Gio, Gtk

from briar_gtk.actions.window import WindowActions
from briar_gtk.views.add_contact import AddContactView
from briar_gtk.presenters.main_window import MainWindowPresenter
from briar_gtk.views.main_window import MainWindowView
from briar_gtk.views.startup import StartupView
from briar_gtk.define import APP, APPLICATION_ID, APPLICATION_NAME
from briar_gtk.define import NOTIFICATION_CONTACT_ADDED
from briar_gtk.define import NOTIFICATION_PRIVATE_MESSAGE, RESOURCES_DIR


class Window(Gtk.ApplicationWindow):

    DEFAULT_WINDOW_SIZE = (900, 600)

    def __init__(self):
        self.main_window_presenter = None
        self._initialize_gtk_application_window()
        WindowActions(self)
        self._setup_content()
        self._setup_focus_listener()

    def show_main_window_view(self):
        self._current_view.destroy()
        self._setup_main_window_view()

    def show_add_contact_view(self):
        self._current_view.destroy()
        if self.main_window_presenter is not None:
            self.main_window_presenter = None
        self._setup_add_contact_view()

    # pylint: disable=arguments-differ,unused-argument
    def do_delete_event(self, event):
        settings = Gio.Settings.new(APPLICATION_ID)
        if settings.get_boolean("quit-dialog-shown"):
            return False  # closes the window
        settings.set_boolean("quit-dialog-shown", True)

        confirmation_dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=_("Are you sure you want to exit?")
        )
        confirmation_dialog.format_secondary_text(
            _("Once you close Briar, you'll no longer "
              "receive messages nor send pending ones. "
              "Keep Briar open to stay connected "
              "with your contacts.")
        )
        response = confirmation_dialog.run()
        confirmation_dialog.destroy()

        if response == Gtk.ResponseType.OK:
            return False  # closes the window

        return True  # keeps the window open

    def _initialize_gtk_application_window(self):
        Gtk.ApplicationWindow.__init__(self, application=APP(),
                                       title=APPLICATION_NAME,
                                       icon_name=APPLICATION_ID)

    def _setup_content(self):
        self._resize_window(self.DEFAULT_WINDOW_SIZE)
        self._setup_startup_view()

    def _setup_focus_listener(self):
        self.connect("focus-in-event", self._on_focus_change)
        self.connect("focus-out-event", self._on_focus_change)

    # pylint: disable=unused-argument
    @staticmethod
    def _on_focus_change(widget, event):
        APP().withdraw_notification(NOTIFICATION_CONTACT_ADDED)
        APP().withdraw_notification(NOTIFICATION_PRIVATE_MESSAGE)

    def _resize_window(self, size):
        if not Window._size_is_valid(size):
            raise Exception("Couldn't resize window; invalid size parameter")
        self.resize(size[0], size[1])

    @staticmethod
    def _size_is_valid(size):
        return len(size) == 2 and\
               isinstance(size[0], int) and\
               isinstance(size[1], int)

    def _setup_view(self, view):
        self._current_view = view
        self._current_view.show_all()
        self.add(self._current_view)

    def _setup_startup_view(self):
        self._setup_view(StartupView(self))

    def _setup_main_window_view(self):
        builder = self._setup_builder()
        main_window_view = MainWindowView(builder, self)
        self.main_window_presenter = MainWindowPresenter(
            main_window_view, builder)
        self._setup_view(main_window_view)
        builder.get_object("chat_menu_button").hide()  # TODO: Make default

    def _setup_add_contact_view(self):
        self._setup_view(AddContactView())

    def _setup_builder(self):
        builder = Gtk.Builder.new()
        builder.add_from_resource(
            os.path.join(RESOURCES_DIR, "main_menu.ui")
        )
        builder.add_from_resource(
            os.path.join(RESOURCES_DIR, "chat_menu.ui")
        )
        builder.add_from_resource(
            os.path.join(RESOURCES_DIR, "main_window.ui")
        )
        builder.connect_signals(self)
        return builder
