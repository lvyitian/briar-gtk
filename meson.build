# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

project(
  'briar-gtk',
  version: '0.1.0',
  meson_version: '>= 0.40.0',
)

i18n = import('i18n')

subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('src/meson_post_install.py')
