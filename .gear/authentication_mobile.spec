Name: authentication_mobile
Version: 0.1.0
Release: alt1

Summary: Alt Mobile domain input tool
License: GPLv3+
Group: System/Configuration/Other
Url: https://github.com/SokolovValy/alt-mobile-auth
BuildArch: noarch

BuildRequires: rpm-build-python3
BuildRequires: rpm-macros-alterator
Requires: libgtk+3-devel
Requires: alterator-auth
Requires: python3-module-pygobject3
Requires: alterator-manager
Requires: alterator-module-executor
Requires: python3

Source0: %name-%version.tar

%description
Alt Mobile domain input tool

%prep
%setup -q

%install
mkdir -p %buildroot%python3_sitelibdir/%name/
cp -r %{name}.py %buildroot%python3_sitelibdir/%name

mkdir -p %buildroot%_alterator_datadir/backends/system/
install -Dm0644 %{name}.backend %buildroot%_alterator_datadir/backends/system

mkdir -p %buildroot%_datadir/polkit-1/actions/
install -Dm0644 ru.basealt.alterator.authentication_mobile1.policy %buildroot%_datadir/polkit-1/actions

mkdir -p %buildroot%_bindir/

ln -s %python3_sitelibdir/%name/%{name}.py \
         %buildroot%_bindir/%{name}.py


%files
%python3_sitelibdir/%name/%name.py
%_bindir/%{name}.py
%_alterator_datadir/backends/system/%{name}.backend
%_datadir/polkit-1/actions/ru.basealt.alterator.authentication_mobile1.policy



%changelog
* Wed Sep 04 2024 Valentin Sokolov <sova@altlinux.org> 0.1.0-alt1
- Initial build for Sisyphus

