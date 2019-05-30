# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from briar.api.constants import Constants

from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


class Api:

    auth_token = None
    _process = None

    def __init__(self, headless_jar):
        self._command = ['java', '-jar', headless_jar]
        self.constants = Constants()
        self._load_auth_token()

    def has_account(self):
        from pathlib import Path
        home = str(Path.home())
        from os.path import isdir, join
        return isdir(join(home, ".briar", "db"))

    def is_running(self):
        return (self._process is not None) and (self._process.poll() is None)

    def login(self, password, callback):
        self._start_and_watch(callback)
        startup_thread = Thread(target=self._login, args=(password,),
                                daemon=True)
        startup_thread.start()

    def register(self, credentials, callback):
        if len(credentials) != 2:
            raise Exception("Can't process credentials")
        self._start_and_watch(callback)
        startup_thread = Thread(target=self._register, args=(credentials,),
                                daemon=True)
        startup_thread.start()

    def stop(self):
        if not self.is_running():
            raise Exception("Nothing to stop")
        self._process.terminate()

    def _start_and_watch(self, callback):
        if self.is_running():
            raise Exception("API already running")
        self._process = Popen(self._command, stdin=PIPE,
                              stdout=PIPE, stderr=STDOUT)
        watch_thread = Thread(target=self._watch_thread, args=(callback,),
                              daemon=True)
        watch_thread.start()

    def _watch_thread(self, callback):
        while self.is_running():
            try:
                sleep(0.1)
                print(urlopen(self.constants.get_base_url()).getcode())
            except HTTPError as e:
                if(e.code == 404):
                    self._load_auth_token()
                    callback(True)
                    return
            except URLError as e:
                if not isinstance(e.reason, ConnectionRefusedError):
                    raise e
        callback(False)

    def _login(self, password):
        if not self.is_running():
            raise Exception("Can't login; API not running")
        self._process.communicate((password + '\n').encode("utf-8"))

    def _register(self, credentials):
        if not self.is_running():
            raise Exception("Can't register; API not running")
        self._process.communicate((credentials[0] + '\n' +
                                   credentials[1] + '\n' +
                                   credentials[1] + '\n').encode("utf-8"))

    def _load_auth_token(self):
        if not self.has_account():
            return
        with open(self.constants.get_auth_token(), 'r') as file:
            self.auth_token = file.read()

