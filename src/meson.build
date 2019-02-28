pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'briar_gtk')

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'briar-gtk.in',
  output: 'briar-gtk',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

briar_gtk_sources = [
  '__init__.py',
  'main.py',
  'ui/gi_composites.py',
  'ui/setup.py',
]

install_data(briar_gtk_sources, install_dir: moduledir)
