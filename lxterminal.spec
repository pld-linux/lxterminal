Summary:	LXTerminal is the standard terminal emulator of LXDE
Name:		lxterminal
Version:	0.1.8
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
# Source0-md5:	97874f553493cbca5082b8d9ef99072e
URL:		http://wiki.lxde.org/en/LXTerminal
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
BuildRequires:	vte-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LXTerminal is the standard terminal emulator of LXDE.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__intltoolize}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{frp,ur_PK}

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
