%global debug_package %{nil}

Name:           vmaf
Version:        1.3.1
Release:        1%{?dist}
Summary:        Library for perceptual video quality assessment based on multi-method fusion

License:        ASL 2.0
URL:            https://github.com/netflix/vmaf/

Source0:  	https://github.com/Netflix/%{name}/archive/v%{version}.tar.gz
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
%autosetup -p1

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

* Mon Dec 18 2017 David Vásquez <davidva AT tutanota DOT com> - 1.3.1-1
- Initial build
