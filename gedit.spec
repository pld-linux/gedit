Summary:	gEdit - small but powerful text editor for X Window
Summary(pl):	gEdit - ma�y ale pot�ny edytor tekstu dla X Window
Name:		gedit2
Version:	2.13.1
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/gnome/sources/gedit/2.13/gedit-%{version}.tar.bz2
# Source0-md5:	9606f4af2c751a9c1ccca11a17b12a38
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
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	gnome-menus-devel >= 2.12.0
BuildRequires:	gtksourceview-devel >= 1.3.91
BuildRequires:	intltool >= 0.33
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeprintui-devel >= 2.10.2
BuildRequires:	libgnomeui-devel >= 2.11.2-2
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	python-gnome-extras-devel >= 2.8.0
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper >= 0.3.12
BuildRequires:	xft-devel >= 2.1.2
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	GConf2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	libgnomeprintui >= 2.10.2
#Suggests:	python-gnome-extras-gtksourceview >= 2.10.0
Obsoletes:	gedit-devel
Obsoletes:	gedit-plugins < 2.3.3-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gEdit is a small but powerful text editor for GTK+ and/or GNOME. It
includes such features as split-screen mode, a plugin API, which
allows gEdit to be extended to support many features while remaining
small at its core, multiple document editing and many more functions.

%description -l pl
gEdit jest ma�ym ale pot�nym edytorem tekstu dla GTK+ i/lub GNOME.
Zawiera takie funkcje jak tryb podzielonego ekranu, API dla "wtyczek",
kt�ry umo�liwia rozszerzenie funkcji gEdita o dodatkowe mo�liwo�ci,
nie zwi�kszaj�c rozmiar�w samego programu, mo�liwo�� edycji wielu
dokument�w naraz i wiele innych.

%package devel
Summary:	gEdit header files
Summary(pl):	pliki nag��wkowe gEdit
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
Pliki nag��wkowe gEdit.

%prep
%setup -q -n gedit-%{version}
%patch0 -p1
%patch1 -p1
sed -i 's/codegen.py/codegen.pyc/' configure.ac

%build
%{__gnome_doc_common}
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--disable-scrollkeeper \
	--enable-python \
	--with-omf-dir=%{_omf_dest_dir}/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# Remove obsoleted *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.la
rm -r $RPM_BUILD_ROOT%{_datadir}/{application-registry,mime-info}
rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.py

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
%attr(755,root,root) %{_libdir}/gedit-2/plugins/*.so
%attr(755,root,root) %{_libdir}/gedit-2/plugins/*.py[co]
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_datadir}/gedit-2
%{_desktopdir}/*
%{_mandir}/man1/*
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-*
%{_pkgconfigdir}/gedit-*.pc
