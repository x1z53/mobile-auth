project(
    'mobile-auth',
    version: '0.1.1',
    meson_version: '>= 0.65.0',
    license: 'GPL-3.0-or-later',
)

gnome = import('gnome')
i18n  = import('i18n')
python = import('python')

py_installation = python.find_installation('python3')
if not py_installation.found()
    error('No valid python3 binary found')
endif

APPLICATION_ID = 'io.guthub.SokolovValy.MobileAuth'
PYTHON_DIR = py_installation.get_path('purelib')
DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'))
PKGDATA_DIR = join_paths(DATA_DIR, APPLICATION_ID)
PKGLIB_DIR = join_paths(get_option('prefix'), get_option('libdir'), APPLICATION_ID)

# Dependencies
dependency('glib-2.0', version: '>= 2.67.1')
dependency('gtk4', version: '>= 4.14.0')
dependency('libadwaita-1', version: '>= 1.5')
dependency('pygobject-3.0', version: '>= 3.47.0')

subdir('data')
subdir('po')

install_subdir(
    'mobileauth',
    install_dir: py_installation.get_install_dir()
)

bin_config = configuration_data()
bin_config.set('application_id', APPLICATION_ID)
bin_config.set('pkgdatadir', PKGDATA_DIR)
bin_config.set('localedir', join_paths(DATA_DIR, 'locale'))
bin_config.set('pythondir', PYTHON_DIR)
bin_config.set('version', meson.project_version())

configure_file(
    input: 'mobile-auth.in',
    output: 'mobile-auth',
    configuration: bin_config,
    install: true,
    install_dir: get_option('bindir')
)

gnome.post_install(
    gtk_update_icon_cache: true,
    update_desktop_database: true
)
