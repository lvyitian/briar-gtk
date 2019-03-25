pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'briar')

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

install_subdir('briar/api', install_dir: moduledir)
install_subdir('briar/gtk', install_dir: moduledir)
