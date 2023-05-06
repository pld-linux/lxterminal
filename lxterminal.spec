#
# Conditional build:
%bcond_with	gtk3	# use GTK+3 instead of GTK+2

Summary:	LXTerminal - the standard terminal emulator of LXDE
Summary(pl.UTF-8):	LXTerminal - standardowy emulator terminala dla LXDE
Name:		lxterminal
Version:	0.4.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	https://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.xz
# Source0-md5:	7938dbd50e3826c11f4735a742b278d3
Patch0:		wordseps.patch
URL:		http://www.lxde.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.6.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 1:2.18.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
%{?with_gtk3:BuildRequires:	vte-devel >= 0.38}
%{!?with_gtk3:BuildRequires:	vte0-devel >= 0.20.0}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.6.0
%{!?with_gtk3:Requires:	gtk+2 >= 1:2.18.0}
Requires:	hicolor-icon-theme
%{!?with_gtk3:Requires:	vte0 >= 0.20.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LXTerminal is the standard terminal emulator of LXDE.

%description -l pl.UTF-8
LXTerminal to standardowy emulator terminala dla środowiska LXDE.

%prep
%setup -q
%patch0 -p1
%{__sed} -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,' configure.ac

%build
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_gtk3:--enable-gtk3}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# unify name
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{tt_RU,tt}
# unsupported by glibc
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/frp
# duplicate of ur
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ur_PK

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
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_bindir}/lxterminal
%{_mandir}/man1/lxterminal.1*
%{_desktopdir}/lxterminal.desktop
%{_datadir}/lxterminal
%{_iconsdir}/hicolor/128x128/apps/lxterminal.png
