Summary:	gEdit - small but powerful text editor for X Window
Summary(pl):	gEdit - ma³y ale potê¿ny edytor tekstu dla X Window
Name:		gedit2
Version:	1.120.0
Release:	0.1
License:	GPL
Group:		X11/Applications/Editors
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://gedit.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	GConf2-devel
BuildRequires:	intltool >= 0.21.0
BuildRequires:	libgnomeui-devel >= 1.116.1
BuildRequires:	libglade2-devel >= 1.99.11
BuildRequires:	libgnomeprintui-devel >= 1.113.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	gedit-devel

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
gEdit is a small but powerful text editor for GTK+ and/or GNOME. It
includes such features as split-screen mode, a plugin API, which
allows gEdit to be extended to support many features while remaining
small at its core, multiple document editing and many more functions.

%description -l pl
gEdit jest ma³ym ale potê¿nym edytorem tekstu dla GTK+ i/lub GNOME.
Zawiera takie funkcje jak tryb podzielonego ekranu, API dla "wtyczek",
który umo¿liwia rozszerzenie funkcji gEdita o dodatkowe mo¿liwo¶ci,
nie zwiêkszaj±c rozmiarów samego programu, mo¿liwo¶æ edycji wielu
dokumentów naraz i wiele innych.

%prep
%setup -q -n gedit-%{version}

%build
rm -f missing acinclude.m4
libtoolize --copy --force
gettextize --copy --force
aclocal 
%{__autoconf}
sed -e 's/-ourdir/ourdir/' xmldocs.make >xmldocs.make.tmp
mv xmldocs.make.tmp xmldocs.make
%{__automake}
%configure 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT 


%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc FAQ README README.plugins ChangeLog TODO AUTHORS THANKS
%attr(755,root,root) %{_bindir}/gedit
%dir %{_libdir}/gedit
%dir %{_libdir}/gedit/plugins
%attr(755,root,root) %{_libdir}/gedit/plugins/*.so.*.*
%{_libdir}/gedit/plugins/*.so
%{_pixmapsdir}/*
%{_datadir}/gedit
%{_datadir}/mime-info/*
%{_applnkdir}/Office/Editors/gedit.desktop
%{_mandir}/man1/*
