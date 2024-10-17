
%define shortname graphlcd
%define name	%shortname-base
%define version	0.1.5
%define rel	6

%define drivers_major	1
%define graphics_major	2
%define drivers_libname	%mklibname glcddrivers %drivers_major
%define graphics_libname	%mklibname glcdgraphics %graphics_major
%define devname	%mklibname -d %{shortname}

Summary:	GraphLCD drivers and tools
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
License:	GPL
Group:		System/Kernel and hardware
URL:		https://graphlcd.berlios.de/
Source:		http://download.berlios.de/graphlcd/%name-%version.tar.bz2
Patch0:		graphlcd-base-01_libserdisp.dpatch
Patch1:		graphlcd-base-02_utf8.dpatch
Patch2:		graphlcd-base-03_gcc-43.dpatch
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	freetype2-devel
BuildRequires:	zlib-devel

%description
The GraphLCD base is a project to support graphical LC displays. It is
mainly used by the graphlcd plugin for the Video Disc Recorder to
display its information.

%package -n %drivers_libname
Summary:	GraphLCD shared driver library
Group:		System/Libraries
Provides:	libglcddrivers = %version-%release
Conflicts:	%{_lib}graphlcd1
# While the library doesn't use graphlcd-config directly, it is
# useless without the linked program using it.
# (Anssi) FIXME: What? If the above is true then this is bogus.
Requires:	%shortname-common >= %version

%description -n %drivers_libname
The GraphLCD base is a project to support graphical LC displays. It is
mainly used by the graphlcd plugin for the Video Disc Recorder to
display its information.

This package contains the driver library needed to run programs
dynamically linked with GraphLCD.

%package -n %devname
Summary:	Headers for graphlcd
Group:		Development/C++
Requires:	%drivers_libname = %version
Requires:	%graphics_libname = %version
Provides:	libglcddrivers-devel = %version-%release
Provides:	glcddrivers-devel = %version-%release
Provides:       libglcdgraphics-devel = %version-%release
Provides:       glcdgraphics-devel = %version-%release
Provides:	graphlcd-devel = %{version}-%{release}
Obsoletes:	%{_lib}glcddrivers1-devel < %{version}-%{release}
Obsoletes:	%{_lib}graphlcd1-devel < %{version}-%{release}
Obsoletes:      %{_lib}glcdgraphics2-devel < %{version}-%{release}

%description -n %devname
The GraphLCD base is a project to support graphical LC displays. It is
mainly used by the graphlcd plugin for the Video Disc Recorder to
display its information.

This package contains the headers that programmers will need to
develop applications which will use graphlcd-base.

%package -n %graphics_libname
Summary:	GraphLCD shared graphics library
Group:		System/Libraries
Provides:	libglcdgraphics = %version-%release
Conflicts:	%{_lib}graphlcd1
# While the library doesn't use graphlcd-config directly, it is
# useless without the linked program using it.
# (Anssi) FIXME: See previous fixme.
Requires:	%shortname-common >= %version

%description -n %graphics_libname
The GraphLCD base is a project to support graphical LC displays. It is
mainly used by the graphlcd plugin for the Video Disc Recorder to
display its information.

This package contains the graphics library needed to run programs
dynamically linked with GraphLCD.

%package -n %shortname-common
Summary:	GraphLCD configuration file and documentation
Group:		System/Kernel and hardware

%description -n %shortname-common
The GraphLCD base is a project to support graphical LC displays. It is
mainly used by the graphlcd plugin for the Video Disc Recorder to
display its information.

This package contains the GraphLCD configuration file and GraphLCD
documentation.

%package -n %shortname-tools
Summary:	GraphLCD tools
Group:		System/Kernel and hardware

%description -n %shortname-tools
The GraphLCD base is a project to support graphical LC displays. It is
mainly used by the graphlcd plugin for the Video Disc Recorder to
display its information.

This package contains tools to use with GraphLCD.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
# don't strip nor chmod to root
perl -pi -e 's,-o root -g root -s,,' $(find -name Makefile)

%build
%make all CFLAGS="%optflags -fPIC" CXXFLAGS="%optflags -fPIC"

%install
rm -rf %{buildroot}

%makeinstall_std BINDIR=%{buildroot}%{_bindir} LIBDIR=%{buildroot}%{_libdir} \
	INCDIR=%{buildroot}%{_includedir}

install -d -m755 %{buildroot}%{_sysconfdir}
install -m644 graphlcd.conf %{buildroot}%{_sysconfdir}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %graphics_libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %graphics_libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%post -n %drivers_libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %drivers_libname -p /sbin/ldconfig
%endif

%files -n %drivers_libname
%defattr(-,root,root)
%doc README
%{_libdir}/libglcddrivers.so.%{drivers_major}*

%files -n %devname
%defattr(-,root,root)
%doc README
%{_includedir}/glcddrivers
%{_includedir}/glcdgraphics
%{_libdir}/libglcddrivers.so
%{_libdir}/libglcdgraphics.so

%files -n %graphics_libname
%defattr(-,root,root)
%doc README
%{_libdir}/libglcdgraphics.so.%{graphics_major}*

%files -n %shortname-common
%doc README HISTORY docs
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/graphlcd.conf

%files -n %shortname-tools
%defattr(-,root,root)
%doc README docs/README.*
%{_bindir}/*




%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.5-6mdv2011.0
+ Revision: 610982
- rebuild

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.1.5-5mdv2010.1
+ Revision: 437811
- rebuild

* Sat Feb 28 2009 Anssi Hannula <anssi@mandriva.org> 0.1.5-4mdv2009.1
+ Revision: 345910
- fix dlopening libserdisp (P0 from e-tobi)
- add UTF-8 support (P1 from e-tobi)
- fix build with gcc 4.3 (P2 from e-tobi)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Feb 08 2008 Anssi Hannula <anssi@mandriva.org> 0.1.5-3mdv2008.1
+ Revision: 164197
- new devel policy
- merge devel packages
- relax versioned requires

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.1.5-2mdv2008.1
+ Revision: 140738
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Mar 02 2007 Anssi Hannula <anssi@mandriva.org> 0.1.5-1mdv2007.0
+ Revision: 131124
- 0.1.5
- split libraries
- new major
- drop patch0, fixed upstream
- Import graphlcd-base

* Sun Sep 10 2006 Anssi Hannula <anssi@mandriva.org> 0.1.3-2mdv2007.0
- fix build

* Mon Aug 14 2006 Anssi Hannula <anssi@mandriva.org> 0.1.3-1mdv2007.0
- initial Mandriva release

