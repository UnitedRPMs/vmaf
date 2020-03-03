%global debug_package %{nil}
%global gitdate 20200302
%global commit0 35c6044d8483a3ab9528f1cc81f75738efe4f4c0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           vmaf
Version:        1.5.1
Release:        1%{?gver}%{dist}
Summary:        Library for perceptual video quality assessment based on multi-method fusion

License:        ASL 2.0
URL:            https://github.com/netflix/vmaf/

Source0:  	https://github.com/Netflix/vmaf/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:	%{name}-snapshot
Patch:		libdir_fix.patch

BuildRequires:  make
BuildRequires:	gcc >= 5.1.1-2
BuildRequires:	gcc-c++
BuildRequires:	git
Requires:       %{name}-static = %{version}-%{release}
Provides:	libvmaf = %{version}-%{release}

%description
Library for perceptual video quality assessment based on multi-method fusion.

%package        static
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    static
The package contains static libraries that use vmaf.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use vmaf.


%prep

#{S:1} -c #{commit0}
%autosetup -n %{name}-%{commit0} -p1

%build

pushd libsvm/
make PREFIX='/usr' lib
popd

make PREFIX='/usr' all


%install
%make_install PREFIX='/usr'

%ifarch x86_64 
sed -i 's|@libdir@|lib64|g' %{buildroot}/%{_libdir}/pkgconfig/libvmaf.pc
%else
sed -i 's|@libdir@|lib|g' %{buildroot}/%{_libdir}/pkgconfig/libvmaf.pc
%endif

install -m 644 libsvm/libsvm.so.2 %{buildroot}/%{_libdir}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%{_datadir}/model
%{_libdir}/libsvm.so.*

%files static
%{_libdir}/libvmaf.a

%files devel
%{_includedir}/libvmaf.h
%{_libdir}/pkgconfig/libvmaf.pc


%changelog

* Mon Mar 02 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.5.1-1.git35c6044
- Updated to 1.5.1

* Wed Sep 11 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.15-1.gite434247
- Updated to 1.3.15

* Sat Apr 06 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.14-1.gita0e7289
- Updated to 1.3.14

* Tue Feb 26 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.13-1.gita0e7289
- Updated to 1.3.13

* Tue Aug 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.9-2.git8bd9a6c
- Updated to current commit

* Sat Aug 11 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.9-1.git1b1d75d
- Updated to 1.3.9-1.git1b1d75d

* Sat Jul 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.7-1.git9605229
- Updated to 1.3.7-1.git9605229

* Wed May 30 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.3.5-1.gita6957a0 
- Updated to 1.3.5-1.gita6957a0
- Added sub-module missed

* Wed May 09 2018 David Vásquez <davidva AT tutanota DOT com> - 1.3.4-1.gitf1225dc
- Updated to 1.3.4-1.gitf1225dc

* Fri Apr 20 2018 David Vásquez <davidva AT tutanota DOT com> - 1.3.1-2.git7848c7d
- Updated to 1.3.1-2.git7848c7d

* Mon Dec 18 2017 David Vásquez <davidva AT tutanota DOT com> - 1.3.1-1
- Initial build
