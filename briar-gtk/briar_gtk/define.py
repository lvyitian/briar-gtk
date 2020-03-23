# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2018 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/lollypop/define.py

from gi.repository import Gio

APPLICATION_ID = "app.briar.gtk"
APPLICATION_NAME = "Briar"
RESOURCES_DIR = "/app/briar/gtk/"
APPLICATION_STYLING_PATH = "resource://" + RESOURCES_DIR + "application.css"
BRIAR_HEADLESS_JAR = "/app/briar/briar-headless.jar"

APP = Gio.Application.get_default
