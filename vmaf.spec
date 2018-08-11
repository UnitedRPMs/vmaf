%global debug_package %{nil}
%global gitdate 20180811
%global commit0 1b1d75db6bf44b62e9755121559c951c03199b2c
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           vmaf
Version:        1.3.9
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

%{S:1} -c %{commit0}
%autosetup -T -D -n %{name}-%{shortcommit0} -p1

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
%{_libdir}/libsvm.so.2

%files static
%{_libdir}/libvmaf.a

%files devel
%{_includedir}/libvmaf.h
%{_libdir}/pkgconfig/libvmaf.pc


%changelog

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
