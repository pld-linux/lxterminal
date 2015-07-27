#
# Conditional build:
%bcond_with		gtk3		# build GTK+3 disables GTK+2
%bcond_without		gtk2	# build with GTK+2

%if %{with gtk3}
%undefine	with_gtk2
%endif

Summary:	LXTerminal is the standard terminal emulator of LXDE
Name:		lxterminal
Version:	0.2.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
# Source0-md5:	e80ad1b6e26212f3d43908c2ad87ba4d
Patch0:		wordseps.patch
URL:		http://wiki.lxde.org/en/LXTerminal
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	gettext-tools
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 1:2.18.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
%{?with_gtk3:BuildRequires:	vte-devel}
%{?with_gtk2:BuildRequires:	vte0-devel}
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LXTerminal is the standard terminal emulator of LXDE.

%prep
%setup -q
%patch0 -p1
%{__sed} -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_gtk3:--enable-gtk3}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# duplicate of ur
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ur_PK
# unsupported by glibc
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/frp

mv $RPM_BUILD_ROOT%{_localedir}/tt{_RU,}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/lxterminal.1*
%{_desktopdir}/%{name}.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/lxterminal.png
