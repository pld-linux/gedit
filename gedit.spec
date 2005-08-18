Summary:	gEdit - small but powerful text editor for X Window
Summary(pl):	gEdit - ma³y ale potê¿ny edytor tekstu dla X Window
Name:		gedit2
Version:	2.11.91
Release:	2
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/gnome/sources/gedit/2.11/gedit-%{version}.tar.bz2
# Source0-md5:	1401595bdfe004fee3f3a567b6c356e0
Patch0:		%{name}-use_default_font.patch
Patch1:		%{name}-desktop.patch
URL:		http://gedit.sourceforge.net/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	ORBit2-devel
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	eel-devel >= 2.10.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.8.0-2
BuildRequires:	gtksourceview-devel >= 1.3.91
BuildRequires:	intltool >= 0.33
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeprintui-devel >= 2.10.2
BuildRequires:	libgnomeui-devel >= 2.11.2-2
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper >= 0.3.12
BuildRequires:	xft-devel >= 2.1.2
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	GConf2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	libgnomeprintui >= 2.10.2
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
Requires:	eel-devel >= 2.10.0
Requires:	gtksourceview-devel >= 1.2.0
Requires:	libglade2-devel >= 1:2.5.1
Requires:	libgnomeprintui-devel >= 2.10.2
Requires:	libgnomeui-devel >= 2.10.0-2

%description devel
gEdit header files

%description devel -l pl
Pliki nag³ówkowe gEdit.

%prep
%setup -q -n gedit-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__gnome_doc_common}
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
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

rm -r $RPM_BUILD_ROOT%{_datadir}/{application-registry,mime-info}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install gedit.schemas
%scrollkeeper_update_post
%update_desktop_database_post

%preun
%gconf_schema_uninstall gedit.schemas

%postun
/sbin/ldconfig
%scrollkeeper_update_postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog TODO AUTHORS THANKS
%{_sysconfdir}/gconf/schemas/gedit.schemas
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/gedit-2
%dir %{_libdir}/gedit-2/plugins
%attr(755,root,root) %{_libdir}/gedit-2/plugins/*.so*
%{_libdir}/bonobo/servers/*
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_datadir}/gedit-2
%{_datadir}/idl/*
%{_desktopdir}/*
%{_mandir}/man1/*
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-*
%{_pkgconfigdir}/gedit-*.pc
