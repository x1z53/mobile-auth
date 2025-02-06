%define app_id io.github.SokolovValy.MobileAuth

Name: mobile-auth
Version: 0.1.1
Release: alt1

Summary: Alt Mobile domain input tool
License: GPLv3+
Group: System/Configuration/Other
Url: https://github.com/SokolovValy/alt-mobile-auth
BuildArch: noarch

BuildRequires(pre): rpm-macros-meson
BuildRequires: meson
BuildRequires: rpm-build-python3
BuildRequires: rpm-macros-alterator
BuildRequires: libgtk4-devel
BuildRequires: libadwaita-devel
BuildRequires: python3-module-pygobject3-devel
BuildRequires: /usr/bin/appstreamcli desktop-file-utils blueprint-compiler
Requires: alterator-auth
Requires: alterator-manager
Requires: alterator-module-executor
Requires: python3

Source0: %name-%version.tar

%description
Alt Mobile domain input tool

%prep
%setup -q

%build
%meson
%meson_build

%install

mkdir -p \
	%buildroot%python3_sitelibdir/
cp -r mobileauth \
	%buildroot%python3_sitelibdir/

%meson_install
%find_lang %name

%files -f %name.lang
%_bindir/%name
%_datadir/metainfo/%app_id.metainfo.xml
%_alterator_datadir/backends/system/mobile_auth.backend
%_datadir/polkit-1/actions/ru.basealt.alterator.mobile-auth1.policy
%_desktopdir/%app_id.desktop
%_iconsdir/hicolor/*/apps/*.svg
%_datadir/locale/*/LC_MESSAGES/%name.mo
%python3_sitelibdir/mobileauth
%_datadir/%app_id/%app_id.gresource


%changelog
* Wed Sep 04 2024 Valentin Sokolov <sova@altlinux.org> 0.1.1-alt1
- Added desktop icon

* Wed Sep 04 2024 Valentin Sokolov <sova@altlinux.org> 0.1.0-alt1
- Initial build for Sisyphus
