Summary:	gEdit - small but powerful text editor for X Window
Summary(pl):	gEdit - ma³y ale potê¿ny edytor tekstu dla X Window
Name:		gedit2
Version:	2.7.1
Release:	1
License:	GPL
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/gnome/sources/gedit/2.7/gedit-%{version}.tar.bz2
# Source0-md5:	e908e378977660772df6b16c354d1a1b
Patch0:		%{name}-use_default_font.patch
Patch1:		%{name}-locale-names.patch
URL:		http://gedit.sourceforge.net/
BuildRequires:	GConf2-devel >= 2.7.1
BuildRequires:	ORBit2-devel
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	eel-devel >= 2.7.1
BuildRequires:	gnome-common >= 2.4.0
BuildRequires:	gtksourceview-devel >= 1.0.1
BuildRequires:	intltool >= 0.29
BuildRequires:	libglade2-devel >= 1:2.4.0
BuildRequires:	libgnomeprintui-devel >= 2.7.0
BuildRequires:	libgnomeui-devel >= 2.7.1
BuildRequires:	libtool
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper >= 0.3.12
BuildRequires:	xft-devel >= 2.1.2
Requires(post):	GConf2
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	scrollkeeper
Requires:	libgnomeprintui >= 2.7.0
Obsoletes:	gedit-devel
Obsoletes:	gedit-plugins < 2.3.3-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package devel
Summary:	gEdit header files
Summary(pl):	pliki nag³ówkowe gEdit
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	eel-devel >= 2.7.1
Requires:	gtksourceview-devel >= 1.0.1
Requires:	libglade2-devel >= 1:2.4.0
Requires:	libgnomeprintui-devel >= 2.7.0
equires:	libgnomeui-devel >= 2.7.1

%description devel
gEdit header files

%description devel -l pl
Pliki nag³ówkowe gEdit.

%prep
%setup -q -n gedit-%{version}
%patch0 -p1
%patch1 -p1

mv po/{no,nb}.po

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}/%{name} \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# Remove obsoleted *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/*.la

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
scrollkeeper-update
%gconf_schema_install
/sbin/ldconfig

%postun
scrollkeeper-update
/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog TODO AUTHORS THANKS
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/gedit-2
%dir %{_libdir}/gedit-2/plugins
%attr(755,root,root) %{_libdir}/bonobo/libgedit-control.so
%attr(755,root,root) %{_libdir}/gedit-2/plugins/*.so*
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_libdir}/bonobo/servers/*
%{_pixmapsdir}/*
%{_datadir}/application-registry/*
%{_desktopdir}/*
%{_datadir}/gedit-2
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/mime-info/*
%{_datadir}/idl/*
%{_omf_dest_dir}/%{name}
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-*
%{_pkgconfigdir}/gedit-*.pc
