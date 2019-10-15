#!/usr/bin/env bash
# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

# Script to copy Briar database from Android to Linux devices.
# Note that you must have started Briar GTK beforehand.
# It's also recommend to manually start adb before using this script.

set -e -x

# List devices
adb devices

# Switch to root mode
adb root

# Copy files
adb pull /data/data/org.briarproject.briar.android/app_db/db.mv.db ~/.briar/db/
adb pull /data/data/org.briarproject.briar.android/app_key/db.key ~/.briar/key/
adb pull /data/data/org.briarproject.briar.android/app_key/db.key.bak ~/.briar/key/
