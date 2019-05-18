# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.gtk.container import Container


class MainContainer(Container):

    def __init__(self):
        super().__init__()
        self.__setup_view()
        self.__register_signals()

    def __setup_view(self):
        self.builder.add_from_resource("/app/briar/gtk/ui/main.ui")
        self.add(self.builder.get_object("main"))
        self.builder.connect_signals(self)