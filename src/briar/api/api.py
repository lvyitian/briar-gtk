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

from subprocess import Popen, PIPE


class Api:

    def __init__(self, headless_jar, debug=False):
        self.headless_jar = headless_jar

    def has_account(self):
        from pathlib import Path
        home = str(Path.home())
        from os.path import isdir, join
        return isdir(join(home, ".briar", "db"))

    def login(self, password):
        p = Popen(['java', '-jar', self.headless_jar, '-v'],
                  stdin=PIPE, universal_newlines=True)
        p.communicate(password + '\n')

    def register(self, credentials):
        p = Popen(['java', '-jar', self.headless_jar, '-v'],
                  stdin=PIPE, universal_newlines=True)
        p.communicate(credentials[0] + '\n' + credentials[1] +
                      '\n' + credentials[1] + '\n')

    def stop(self):
        pass
