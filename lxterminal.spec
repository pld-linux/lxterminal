#
# Conditional build:
%bcond_with		gtk3		# build GTK+3 disables GTK+2
%bcond_without		gtk2	# build with GTK+2

%if %{with gtk3}
%undefine	with_gtk2
%endif

Summary:	LXTerminal is the standard terminal emulator of LXDE
Name:		lxterminal
Version:	0.1.11
Release:	6
License:	GPL v2
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
# Source0-md5:	fd9140b45c0f28d021253c4aeb8c4aea
Patch0:		wordseps.patch
URL:		http://wiki.lxde.org/en/LXTerminal
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
%{?with_gtk2:BuildRequires:	gtk+2-devel}
%{?with_gtk3:BuildRequires:	gtk+3-devel}
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
%{?with_gtk3:BuildRequires:	vte-devel}
%{?with_gtk2:BuildRequires:	vte0-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LXTerminal is the standard terminal emulator of LXDE.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__intltoolize}
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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/%{name}*
%{_pixmapsdir}/%{name}.png
%{_datadir}/%{name}
