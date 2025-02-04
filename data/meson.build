desktop_conf = configuration_data()
desktop_conf.set('icon', APPLICATION_ID)
i18n.merge_file(
  type: 'desktop',
  input: '@0@.desktop.in'.format(APPLICATION_ID),
  output: '@0@.desktop'.format(APPLICATION_ID),
  po_dir: join_paths(meson.project_source_root(), 'po'),
  install: true,
  install_dir: join_paths(DATA_DIR, 'applications')
)

desktop_file_validate = find_program('desktop-file-validate', required:false)
if desktop_file_validate.found()
  test (
    'Validate desktop file',
    desktop_file_validate,
    args: join_paths(meson.current_build_dir (), APPLICATION_ID + '.desktop')
  )
endif

metainfo_file = i18n.merge_file(
  input: '@0@.metainfo.xml.in'.format(APPLICATION_ID),
  output: '@0@.metainfo.xml'.format(APPLICATION_ID),
  po_dir: join_paths(meson.project_source_root(), 'po'),
  install: true,
  install_dir: join_paths(DATA_DIR, 'metainfo')
)

appstreamcli = find_program('appstreamcli', required: false)
if (appstreamcli.found())
  test('Validate metainfo file',
    appstreamcli,
    args: ['validate', '--no-net', '--explain', metainfo_file],
    workdir: meson.current_build_dir()
  )
endif

install_data('org.altlinux.alterator.authentication_mobile1.policy',
  install_dir: join_paths(DATA_DIR, 'polkit-1/actions/')
)

install_data('authentication_mobile.backend',
  install_dir: join_paths(DATA_DIR, 'alterator/backends/system/')
)

blueprints = custom_target('blueprints',
  input: files(
    'ui/admin-dialog.blp',
    'ui/welcome-dialog.blp',
    'ui/window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources(
  APPLICATION_ID,
  '@0@.gresource.xml'.format(APPLICATION_ID),
  gresource_bundle: true,
  dependencies: blueprints,
  source_dir: meson.current_build_dir(),
  install_dir: PKGDATA_DIR,
  install: true
)

subdir('icons')
