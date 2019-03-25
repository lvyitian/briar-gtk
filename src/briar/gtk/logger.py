# Copyright (c) 2019 Nico Alt
# Copyright (c) 2014-2018 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# Copyright (c) 2017 Bilal Elmoussaoui <bil.elmoussaoui@gmail.com>
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
#
# Initial version based on GNOME Lollypop
# https://gitlab.gnome.org/World/lollypop/blob/1.0.2/lollypop/logger.py

import logging
import sys

from briar.gtk.define import App


class Logger:

    FORMAT = "[%(levelname)-s] %(asctime)s %(message)s"
    DATE = "%Y-%m-%d %H:%M:%S"
    __log = None
    APP = "app.briar.gtk"

    @staticmethod
    def get_default():
        if Logger.__log is None:
            logger = logging.getLogger(Logger.APP)

            handler = logging.StreamHandler(sys.stdout)
            formater = logging.Formatter(Logger.FORMAT, Logger.DATE)
            handler.setFormatter(formater)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

            Logger.__log = logging.getLogger(Logger.APP)
        return Logger.__log

    @staticmethod
    def warning(msg, *args):
        Logger.get_default().warning(msg, *args)

    @staticmethod
    def debug(msg, *args):
        if App().debug:
            Logger.get_default().debug(msg, *args)

    @staticmethod
    def info(msg, *args):
        Logger.get_default().info(msg, *args)

    @staticmethod
    def error(msg, *args):
        Logger.get_default().error(msg, *args)
