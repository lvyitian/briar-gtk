# Copyright (c) 2019 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md

PACKAGE_DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

python3 = import('python3')

conf = configuration_data()
conf.set('PACKAGE_URL', 'https://code.briarproject.org/briar/briar-gtk/blob/main/README.md')
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('PACKAGE_DATA_DIR', PACKAGE_DATA_DIR)

subdir('data')
subdir('po')

configure_file(
  input: 'briar-gtk.in',
  output: 'briar-gtk',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

install_subdir('briar_gtk', install_dir: PACKAGE_DATA_DIR)

meson.add_install_script('meson_post_install.py')
