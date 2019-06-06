# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from os.path import isfile
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from briar.api.constants import BASE_HTTP_URL, BRIAR_AUTH_TOKEN, BRIAR_DB
from briar.api.models.socket_listener import SocketListener


class Api:

    auth_token = None
    socket_listener = None

    _process = None

    def __init__(self, headless_jar):
        self._command = ["java", "-jar", headless_jar]

        self.socket_listener = SocketListener(self)

    @staticmethod
    def has_account():
        return isfile(BRIAR_DB)

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
                urlopen(BASE_HTTP_URL)
                sleep(0.1)
            except HTTPError as http_error:
                if http_error.code == 404:
                    self._load_auth_token()
                    callback(True)
                    return
            except URLError as url_error:
                if not isinstance(url_error.reason, ConnectionRefusedError):
                    raise url_error
        callback(False)

    def _login(self, password):
        if not self.is_running():
            raise Exception("Can't login; API not running")
        self._process.communicate(("%s\n" % password).encode("utf-8"))

    def _register(self, credentials):
        if not self.is_running():
            raise Exception("Can't register; API not running")
        self._process.communicate((credentials[0] + '\n' +
                                   credentials[1] + '\n' +
                                   credentials[1] + '\n').encode("utf-8"))

    def _load_auth_token(self):
        if not Api.has_account():
            raise Exception("Can't load authentication token")
        with open(BRIAR_AUTH_TOKEN, 'r') as file:
            self.auth_token = file.read()
