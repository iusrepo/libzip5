%bcond_without tests

Name:    libzip5
Version: 1.7.3
Release: 2%{?dist}
Summary: C library for reading, creating, and modifying zip archives

License: BSD
URL:     https://libzip.org/
Source0: https://libzip.org/download/libzip-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:  xz-devel
BuildRequires:  cmake3 >= 3.0.2
# Needed to run the test suite
# find regress/ -type f | /usr/lib/rpm/perl.req
# find regress/ -type f | /usr/lib/rpm/perl.prov
BuildRequires:  perl-interpreter
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.


%package devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Conflicts/#_compat_package_conflicts
Conflicts: libzip-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package tools
Summary:  Command line tools from %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package provides command line tools split off %{name}:
- %{name}-zipcmp
- %{name}-zipmerge
- %{name}-ziptool


%prep
%autosetup -n libzip-%{version} -p1

# unwanted in package documentation
rm INSTALL.md

# change cmake invocations to cmake3
sed -e 's/ cmake / cmake3 /' -i CMakeLists.txt regress/CMakeLists.txt

# drop skipped test which make test suite fails (cmake issue ?)
sed -e '/clone-fs-/d' \
    -i regress/CMakeLists.txt


%build
%cmake3 \
  -DENABLE_COMMONCRYPTO:BOOL=OFF \
  -DENABLE_GNUTLS:BOOL=OFF \
  -DENABLE_MBEDTLS:BOOL=OFF \
  -DENABLE_OPENSSL:BOOL=ON \
  -DENABLE_WINDOWS_CRYPTO:BOOL=OFF \
  -DENABLE_BZIP2:BOOL=ON \
  -DENABLE_LZMA:BOOL=ON \
  -DBUILD_TOOLS:BOOL=ON \
  -DBUILD_REGRESS:BOOL=ON \
  -DBUILD_EXAMPLES:BOOL=OFF \
  -DBUILD_DOC:BOOL=ON \
  .

%cmake3_build


%install
%cmake3_install

# rename tools for parallel installation
mv %{buildroot}%{_bindir}/{,%{name}-}zipcmp
mv %{buildroot}%{_bindir}/{,%{name}-}zipmerge
mv %{buildroot}%{_bindir}/{,%{name}-}ziptool
mv %{buildroot}%{_mandir}/man1/{,%{name}-}zipcmp.1
mv %{buildroot}%{_mandir}/man1/{,%{name}-}zipmerge.1
mv %{buildroot}%{_mandir}/man1/{,%{name}-}ziptool.1


%check
%if %{with tests}
%ctest3
%else
: Test suite disabled
%endif


%ldconfig_scriptlets


%files
%license LICENSE
%{_libdir}/libzip.so.5*

%files tools
%{_bindir}/%{name}-zipcmp
%{_bindir}/%{name}-zipmerge
%{_bindir}/%{name}-ziptool
%{_mandir}/man1/%{name}-zipcmp.1*
%{_mandir}/man1/%{name}-zipmerge.1*
%{_mandir}/man1/%{name}-ziptool.1*

%files devel
%doc AUTHORS THANKS *.md
%{_includedir}/zip.h
%{_includedir}/zipconf*.h
%{_libdir}/libzip.so
%{_libdir}/pkgconfig/libzip.pc
%{_libdir}/cmake/libzip
%{_mandir}/man3/libzip*
%{_mandir}/man3/zip*
%{_mandir}/man3/ZIP*


%changelog
* Tue Jul 21 2020 Rex Dieter <rdieter@fedoraproject.org> - 1.7.3-2
- use %%cmake3_build, %%cmake3_install, %%ctest3

* Wed Jul 15 2020 Remi Collet <remi@remirepo.net> - 1.7.3-1
- update to 1.7.3
- drop patch merged upstream

* Mon Jul 13 2020 Remi Collet <remi@remirepo.net> - 1.7.2-1
- update to 1.7.2
- fix installation layout using merged patch from
  https://github.com/nih-at/libzip/pull/190

* Mon Jun 15 2020 Remi Collet <remi@remirepo.net> - 1.7.1-1
- update to 1.7.1

* Sat Jun 06 2020 Carl George <carl@george.computer> - 1.7.0-2
- Initial libzip5 package based on Fedora's libzip

* Fri Jun  5 2020 Remi Collet <remi@remirepo.net> - 1.7.0-1
- update to 1.7.0
- patch zipconf.h to re-add missing LIBZIP_VERSION_* macros

* Mon Feb  3 2020 Remi Collet <remi@remirepo.net> - 1.6.1-1
- update to 1.6.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Remi Collet <remi@remirepo.net> - 1.6.0-1
- update to 1.6.0
- enable lzma support

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Remi Collet <remi@remirepo.net> - 1.5.2-1
- update to 1.5.2
- add all explicit cmake options to ensure openssl is used
  even in local build with other lilbraries available

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 11 2018 Remi Collet <remi@remirepo.net> - 1.5.1-1
- update to 1.5.1
- drop dependency on zlib-devel and bzip2-devel no more
  referenced in libzip.pc
- drop rpath patch merged upstream

* Thu Mar 15 2018 Remi Collet <remi@remirepo.net> - 1.5.0-2
- add dependency on zlib-devel and bzip2-devel #1556068

* Mon Mar 12 2018 Remi Collet <remi@remirepo.net> - 1.5.0-1
- update to 1.5.0
- use openssl for cryptography instead of bundled custom AES implementation

* Tue Feb 20 2018 Remi Collet <remi@remirepo.net> - 1.4.0-5
- missing BR on C compiler
- use ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan  5 2018 Remi Collet <remi@remirepo.net> - 1.4.0-3
- add upstream patch and drop multilib hack

* Tue Jan  2 2018 Remi Collet <remi@remirepo.net> - 1.4.0-2
- re-add multilib hack #1529886

* Sat Dec 30 2017 Remi Collet <remi@remirepo.net> - 1.4.0-1
- update to 1.4.0
- switch to cmake
- add upstream patch for lib64

* Mon Nov 20 2017 Remi Collet <remi@remirepo.net> - 1.3.2-1
- update to 1.3.2
- drop multilib header hack
- change URL to https://libzip.org/
- test suite now ok on all arch

* Wed Sep 06 2017 Pavel Raiskup <praiskup@redhat.com> - 1.3.0-2
- use multilib-rpm-config for multilib hacks

* Mon Sep  4 2017 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0
- add dependency on bzip2 library
- ignore 3 tests failing on 32-bit

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- soname bump to 5

* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> - 1.2.0-0
- update to 1.2.0
- soname bump to 5
- temporarily keep libzip.so.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2
- add BR on perl(Getopt::Long)

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1-1
- update to 1.1
- new ziptool command
- add fix for undefined optopt in ziptool.c (upstream)

* Fri Dec  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- fix libzip-tools summary #1288424

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May  5 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- soname bump from .2 to .4
- drop ziptorrent
- create "tools" sub package

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.2-5
- actually apply patch (using %%autosetup)

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.2-4
- CVE-2015-2331: integer overflow when processing ZIP archives (#1204676,#1204677)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 19 2013 Remi Collet <remi@fedoraproject.org> - 0.11.2-1
- update to 0.11.2
- run test during build

* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-3
- replace php patch with upstream one

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-2
- include API-CHANGES and LICENSE in package doc

* Wed Aug 21 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-1
- update to 0.11.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Remi Collet <remi@fedoraproject.org> - 0.10.1-5
- fix typo in multiarch (#866171)

* Wed Sep 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.1-4
- Warning about conflicting contexts for /usr/lib64/libzip/include/zipconf.h versus /usr/include/zipconf-64.h (#853954)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.1-2
- spec cleanup, better multilib fix

* Wed Mar 21 2012 Remi Collet <remi@fedoraproject.org> - 0.10.1-1
- update to 0.10.1 (security fix only)
- fixes for CVE-2012-1162 and CVE-2012-1163

* Sun Mar 04 2012 Remi Collet <remi@fedoraproject.org> - 0.10-2
- try to fix ARM issue (#799684)

* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> - 0.10-1
- update to 0.10
- apply patch with changes from php bundled lib (thanks spot)
- handle multiarch headers (ex from MySQL)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.9.3-2
- Cleaned up pkgconfig deps which are now automatically handled by RPM.

* Thu Feb 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.9.3-1
- Updated to libzip 0.9.3

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.9-4
- Use bzipped upstream tarball.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.9-1
- libzip-0.9

* Sat Feb 09 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.8-5
- rebuild for new gcc-4.3

* Fri Jan 11 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 0.8-4
- use better workaround for removing rpaths

* Tue Nov 20 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-3
- require pkgconfig in devel subpkg
- move api description to devel subpkg
- keep timestamps in %%install
- avoid lib64 rpaths 

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-2
- Change License to BSD

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-1
- Initial version for Fedora
