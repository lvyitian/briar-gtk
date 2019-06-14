#!/usr/bin/env bash

set -e -x

tools/tests/test-pycodestyle.sh
tools/tests/test-pylint.sh
tools/tests/test-pytest.sh
