#!/usr/bin/env bash
# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

PYTHONPATH=src pytest --cov=src tests/
