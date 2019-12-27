#!/usr/bin/env python3
# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

from os import environ, path
from subprocess import call

PREFIX = environ.get('MESON_INSTALL_PREFIX', '/usr/local')
DATA_DIR = path.join(PREFIX, 'share')
DESTINATION_DIR = environ.get('DESTDIR', '')

# Package managers set this so we don't need to run
if not DESTINATION_DIR:
    print('Updating icon cache...')
    call(['gtk-update-icon-cache', '-qtf',
          path.join(DATA_DIR, 'icons', 'hicolor')])

    print('Updating desktop database...')
    call(['update-desktop-database', '-q',
          path.join(DATA_DIR, 'applications')])

    print('Compiling GSettings schemas...')
    call(['glib-compile-schemas', path.join(DATA_DIR, 'glib-2.0', 'schemas')])
