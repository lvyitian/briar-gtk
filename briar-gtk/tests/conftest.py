# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import pytest


@pytest.fixture()
def is_file(mocker):
    return mocker.patch('os.path.isfile')
