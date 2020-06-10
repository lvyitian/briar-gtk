# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2018 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/lollypop/define.py

import os
import pathlib

from gi.repository import Gio

APPLICATION_ID = "app.briar.gtk"
APPLICATION_NAME = "Briar"
RESOURCES_DIR = os.path.join("/app", "briar", "gtk")
APPLICATION_STYLING_PATH = "resource:///app/briar/gtk/application.css"

APP = Gio.Application.get_default


def get_briar_headless_jar():
    flatpak_path = "/app/share/java/briar-headless.jar"
    if os.path.isfile(flatpak_path):
        return flatpak_path

    debian_path = "/usr/share/java/briar-headless.jar"
    if os.path.isfile(debian_path):
        return debian_path

    local_path = os.path.join(
        pathlib.Path.home(),
        ".local", "share", "java",
        "briar-headless.jar"
    )
    if os.path.isfile(local_path):
        return local_path

    raise FileNotFoundError("Couldn't find briar-headless.jar")
