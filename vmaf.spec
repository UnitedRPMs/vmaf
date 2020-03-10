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
#Patch:		libdir_fix.patch

BuildRequires:  make
BuildRequires:	gcc >= 5.1.1-2
BuildRequires:	gcc-c++
BuildRequires:	meson
BuildRequires:	doxygen

%description
Library for perceptual video quality assessment based on multi-method fusion.

%package -n	libvmaf
Summary:        Libs for vmaf
Obsoletes: 	%{name}-static >= %{version}

%description -n libvmaf
Libs for vmaf

%package -n	libvmaf-devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Obsoletes: 	vmaf-devel >= %{version}

%description -n libvmaf-devel
The libvmaf-devel package contains libraries and header files for
developing applications that use vmaf.


%prep
%autosetup -n %{name}-%{commit0} -p1

%build
pushd libvmaf/
%meson 

%meson_build 


%install
pushd libvmaf/
%meson_install

pushd %{buildroot}/%{_libdir}
gcc -shared -fPIC -Wl,-soname,libvmaf.so -o libvmaf.so.0.0.0
ln -s libvmaf.so.0.0.0 libvmaf.so.0
popd

pushd *-redhat-linux-gnu/tools
for _bin in moment ms_ssim psnr ssim
    do
        install -D -m755 "${_bin}" "%{buildroot}/%{_bindir}/vmaf-${_bin}"
    done
popd

# We don't need it 
rm -f %{buildroot}/%{_libdir}/libvmaf.a


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%{_bindir}/vmaf-*
%{_bindir}/vmafossexec
%{_datadir}/model

%files -n libvmaf
%{_libdir}/*.so.*

%files -n libvmaf-devel
%{_libdir}/libvmaf.so
%{_includedir}/libvmaf/libvmaf.h
%{_includedir}/libvmaf/version.h
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
