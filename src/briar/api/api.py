# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from subprocess import Popen, PIPE


class Api:

    def __init__(self, headless_jar, debug=False):
        self.headless_jar = headless_jar

    def has_account(self):
        from pathlib import Path
        home = str(Path.home())
        from os.path import isdir, join
        return isdir(join(home, ".briar", "db"))

    def login(self, password, callback):
        p = Popen(['java', '-jar', self.headless_jar, '-v'],
                  stdin=PIPE, universal_newlines=True)
        p.communicate(password + '\n')
        callback()

    def register(self, credentials, callback):
        p = Popen(['java', '-jar', self.headless_jar, '-v'],
                  stdin=PIPE, universal_newlines=True)
        p.communicate(credentials[0] + '\n' + credentials[1] +
                      '\n' + credentials[1] + '\n')
        callback()

    def stop(self):
        pass
