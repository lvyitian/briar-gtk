#!/usr/bin/env bash
# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

set -e -x

tools/tests/test-pycodestyle.sh
tools/tests/test-pylint.sh
# tools/tests/test-pytest.sh
