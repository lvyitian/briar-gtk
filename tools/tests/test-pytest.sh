#!/usr/bin/env bash
# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

PYTHONPATH=briar-gtk/briar_gtk pytest --cov=briar_gtk briar-gtk/tests/
