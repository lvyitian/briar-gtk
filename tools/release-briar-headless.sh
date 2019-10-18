#!/usr/bin/env bash
# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

set -e -x

cd ../briar-android

./gradlew --configure-on-demand briar-headless:jar

cd briar-headless/build/libs

sha256sum briar-headless.jar > sha256sum.txt
git log | head -n 1 > commit.txt

echo "To sign, call 'for file in \$(ls); do gpg -b \"\$file\"; done'"

xdg-open .
