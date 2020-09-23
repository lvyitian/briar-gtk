# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

import gettext


# pylint: disable=unused-argument
def pgettext(context, message):
    """
    Backport of `gettext.pgettext` which is only available in Python 3.8+
    """
    return gettext.gettext(message)
