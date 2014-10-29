%define revcount %(git rev-list HEAD | wc -l)
%define treeish %(git rev-parse --short HEAD)
%define localmods %(git diff-files --exit-code --quiet  || date +.m%%j%%H%%M%%S)

%define srcdir   %{getenv:PWD}

Summary: Redgate Build Server
Name: build-server
Version: 1.0
Release: %{revcount}.%{treeish}%{localmods}
Distribution: Redgate/Services
Group: System Environment/Daemons
License: Proprietary
Vendor: Karl Redgate
Packager: Karl Redgate <karl.redgate@gmail.com>
BuildArch: noarch

%define _topdir %(echo $PWD)/rpm
BuildRoot: %{_topdir}/BUILDROOT

Requires: development
Requires: git
Requires(preun): chkconfig
Requires(post): chkconfig

%description
Config and scripts to make an Amazon micro image into a build
server.

%prep
%build

%install
%{__install} --directory --mode=755 $RPM_BUILD_ROOT/usr/libexec/build-server
%{__install} --mode=755 %{srcdir}/libexec/build-server/* $RPM_BUILD_ROOT/usr/libexec/build-server/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
/usr/libexec/build-server/

%pre
/usr/libexec/build-server/setup/create-users

%post
[ "$1" -gt 1 ] && {
    : Upgrading
}

[ "$1" = 1 ] && {
    : New install
}

/usr/libexec/build-server/setup/install-node-syslog | logger --tag %{name}

: ignore test return value

%preun
[ "$1" = 0 ] && {
    : cleanup
}

: ignore test return value

%postun

[ "$1" = 0 ] && {
    : This is really an uninstall
}

: ignore test errs

%changelog

* Fri Sep 12 2014 Karl Redgate <redgates..com>
- Initial release

# vim:autoindent expandtab sw=4
