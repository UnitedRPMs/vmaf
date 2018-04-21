%global debug_package %{nil}
%global gitdate 20180420
%global commit0 7848c7df526c75485deac11975629f7c9619dadb
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           vmaf
Version:        1.3.1
Release:        2%{?gver}%{dist}
Summary:        Library for perceptual video quality assessment based on multi-method fusion

License:        ASL 2.0
URL:            https://github.com/netflix/vmaf/

Source0:  	https://github.com/Netflix/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch:		libdir_fix.patch

BuildRequires:  make
BuildRequires:	gcc >= 5.1.1-2
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
%{_libdir}/libsvm.so.2

%files static
%{_libdir}/libvmaf.a

%files devel
%{_includedir}/libvmaf.h
%{_libdir}/pkgconfig/libvmaf.pc


%changelog

* Fri Apr 20 2018 David Vásquez <davidva AT tutanota DOT com> - 1.3.1-2.git7848c7d
- Updated to 1.3.1-2.git7848c7d

* Mon Dec 18 2017 David Vásquez <davidva AT tutanota DOT com> - 1.3.1-1
- Initial build
