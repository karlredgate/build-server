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

# Many of these come from the yum 'development' group
Requires: ant
Requires: autoconf
Requires: automake
Requires: babel
Requires: binutils
Requires: bison
Requires: byacc
Requires: bzr
Requires: chrpath
Requires: cmake
Requires: crash
Requires: cscope
Requires: ctags
Requires: dejagnu
Requires: diffstat
Requires: doxygen
Requires: elfutils
Requires: expect
Requires: flex
Requires: gcc
Requires: gcc-c++
Requires: gcc-gnat
Requires: gdb
Requires: gettext
Requires: git
Requires: glibc-utils
Requires: imake
Requires: indent
Requires: inotify-tools
Requires: intltool
Requires: jpackage-utils
Requires: jq
Requires: kexec-tools
Requires: latrace
Requires: libtool
Requires: lslk
Requires: ltrace
Requires: make
Requires: mercurial
Requires: nasm
Requires: npm
Requires: patch
Requires: patchutils
Requires: pkgconfig
Requires: protobuf-compiler
Requires: protobuf-c
Requires: protobuf-c-devel
Requires: rpm-build
Requires: rpmdevtools
Requires: rpmlint
Requires: strace
Requires: subversion
Requires: system-rpm-config
Requires: texinfo
Requires: valgrind

%description
Config and scripts to make an Amazon micro image into a build
server.

%prep
%build

%install
%{__install} --directory --mode=755 $RPM_BUILD_ROOT/usr/libexec/build-server/setup
%{__install} --mode=755 %{srcdir}/libexec/build-server/setup/* $RPM_BUILD_ROOT/usr/libexec/build-server/setup/

%{__install} --directory --mode=755 $RPM_BUILD_ROOT/usr/bin
%{__install} --mode=755 %{srcdir}/bin/* $RPM_BUILD_ROOT/usr/bin/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
/usr/bin/create-server
/usr/bin/get-ec2-instance-id
/usr/libexec/build-server/

%pre
# create users here that are required for the installation of files in
# this package.

%post
[ "$1" -gt 1 ] && {
    : Upgrading
}

[ "$1" = 1 ] && {
    : New install
}

/usr/libexec/build-server/setup/create-users
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

* Fri Oct 31 2014 Karl Redgate <redgates.com>
- Initial release

# vim:autoindent expandtab sw=4
