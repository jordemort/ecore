# Conditional build stuff; from rpm 4.4 /usr/lib/rpm/macros.
# bcond_without defaults to WITH, and vice versa.  Yes, it's
# ass-backward.  Blame PLD.
# from KainX's changes to evas... 
%if %{!?with:1}0
%define with() %{expand:%%{?with_%{1}:1}%%{!?with_%{1}:0}}
%endif
%if %{!?without:1}0
%define without() %{expand:%%{?with_%{1}:0}%%{!?with_%{1}:1}}
%endif
%if %{!?bcond_with:1}0
%define bcond_with() %{expand:%%{?_with_%{1}:%%global with_%{1} 1}}
%endif
%if %{!?bcond_without:1}0
%define bcond_without() %{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}
%endif

## disabled features
%bcond_with lib_ecore_directfb
%bcond_with lib_ecore_sdl

## enabled features
##%bcond_without module_engine_software_x11
%bcond_without lib_ecore_fb
%bcond_without lib_ecore_imf

# This just keeps a missing doxygen from killing the build.
%define _missing_doc_files_terminate_build 0

%define breq_lib_ecore_directfb     %{?with_lib_ecore_directfb:DirectFB}
%define breq_lib_ecore_sdl          %{?with_lib_ecore_sdl:SDL-devel}

%define ac_with_lib_ecore_directfb  --%{?with_lib_ecore_directfb:en}%{!?with_lib_ecore_directfb:dis}able-ecore-directfb
%define ac_with_lib_ecore_fb        --%{?with_lib_ecore_fb:en}%{!?with_lib_ecore_fb:dis}able-ecore-fb
%define ac_with_lib_ecore_imf       --%{?with_lib_ecore_imf:en}%{!?with_lib_ecore_imf:dis}able-ecore-imf
%define ac_with_lib_ecore_sdl       --%{?with_lib_ecore_sdl:en}%{!?with_lib_ecore_sdl:dis}able-ecore-sdl

%{!?_rel:%{expand:%%global _rel 0.enl%{?dist}}}

Summary: Enlightened Core X interface library
Name: ecore
Version: 1.7.7
Release: %{_rel}
License: BSD
Group: User Interface/X
Source: %{name}-%{version}.tar.gz
URL: http://www.enlightenment.org
Packager: %{?_packager:%{_packager}}%{!?_packager:Michael Jennings <mej@eterm.org>}
Vendor: %{?_vendorinfo:%{_vendorinfo}}%{!?_vendorinfo:The Enlightenment Project (http://www.enlightenment.org/)}
Distribution: %{?_distribution:%{_distribution}}%{!?_distribution:%{_vendor}}
#BuildSuggests: xorg-x11-devel, XFree86-devel, libX11-devel, c-ares-devel
BuildRequires: libjpeg-devel, openssl-devel %{?breq_lib_ecore_directfb}
BuildRequires: curl-devel, evas-devel, eet-devel %{?breq_lib_ecore_sdl}
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
Ecore is the event/X abstraction layer that makes doing selections,
Xdnd, general X stuff, event loops, timeouts and idle handlers fast,
optimized, and convenient. It's a separate library so anyone can make
use of the work put into Ecore to make this job easy for applications.

%package devel
Summary: Ecore headers and development libraries.
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: curl-devel, openssl-devel, evas-devel, eet-devel
Requires: ecore-con, ecore-evas, ecore-file, ecore-ipc
Requires: ecore-x %{?with_lib_ecore_fb:ecore-fb} %{?with_lib_ecore_directfb:ecore-directfb}

%description devel
Ecore development files

%package con
Summary: Ecore Connection Library
Group: Development/Libraries
Requires: %{name} = %{version}

%description con
Ecore Connection Library

%if %{with lib_ecore_directfb}
%package directfb
Summary: Ecore DirectFB system functions
Group: Development/Libraries
Requires: %{name} = %{version}
%description directfb
Ecore DirectFB system functions
%endif

%package evas
Summary: Ecore Evas Wrapper Library
Group: Development/Libraries
Requires: %{name} = %{version}

%description evas
Ecore Evas Wrapper Library

%if %{with lib_ecore_fb}
%package fb
Summary: Ecore frame buffer system functions
Group: Development/Libraries
Requires: %{name} = %{version}
%description fb
Ecore frame buffer system functions
%endif

%package file
Summary: Ecore File Library
Group: Development/Libraries
Requires: %{name} = %{version}

%description file
Ecore File Library

%if %{with lib_ecore_imf}
%package imf
Summary: Ecore IMF functions
Group: Development/Libraries
Requires: %{name} = %{version}
%description imf
Ecore IMF functions
%endif

%package input
Summary: Ecore input functions
Group: Development/Libraries
Requires: %{name} = %{version}

%description input
Ecore input functions

%package ipc
Summary: Ecore inter-process communication functions
Group: Development/Libraries
Requires: %{name} = %{version}

%description ipc
Ecore inter-process communication functions

%package x
Summary: Ecore functions for dealing with the X Windows System
Group: Development/Libraries
Requires: %{name} = %{version}

%description x
Ecore functions for dealing with the X Windows System

%prep
%setup -q

%build
CFLAGS="-I/usr/kerberos/include -I/usr/X11R6/include/X11/extensions"
LDFLAGS="-L/usr/kerberos/lib -L/usr/X11R6/%{_lib}"
export CFLAGS LDFLAGS
%{configure} --prefix=%{_prefix} \
    %{?ac_with_lib_ecore_directfb} \
    %{?ac_with_lib_ecore_fb} \
    %{?ac_with_lib_ecore_imf} \
    %{?ac_with_lib_ecore_sdl}

%{__make} %{?_smp_mflags} %{?mflags}

%install
%{__make} %{?mflags_install} DESTDIR=$RPM_BUILD_ROOT install
%{find_lang} %{name}

%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :

%clean
test "x$RPM_BUILD_ROOT" != "x/" && rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING* README*
%{_libdir}/libecore*.so.*

%files devel
%defattr(-, root, root)
%doc doc/html
%{_libdir}/*.so
%{_libdir}/ecore/immodules/*.so
%{_libdir}/ecore/immodules/*.la
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
#%{_datadir}/aclocal/*
%{_includedir}/ecore-1/*.h

%files con
%defattr(-, root, root)
%{_libdir}/libecore_con*.so.*

%if %{with lib_ecore_directfb}
%files directfb
%defattr(-, root, root)
%{_libdir}/libecore_directfb*.so.*
%endif

%files evas
%defattr(-, root, root)
%{_libdir}/libecore_evas*.so.*

%if %{with lib_ecore_fb}
%files fb
%defattr(-, root, root)
%{_libdir}/libecore_fb*.so.*
%endif

%files file
%defattr(-, root, root)
%{_libdir}/libecore_file*.so.*

%if %{with lib_ecore_imf}
%files imf
%defattr(-, root, root)
%{_libdir}/libecore_imf*.so.*
%endif

%files input
%defattr(-, root, root)
%{_libdir}/libecore_input*.so.*

%files ipc
%defattr(-, root, root)
%{_libdir}/libecore_ipc*.so.*

%files x
%defattr(-, root, root)
%{_libdir}/libecore_x*.so.*
