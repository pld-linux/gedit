Summary:	gedit - small but powerful text editor for X Window
Summary(pl.UTF-8):	gedit - mały ale potężny edytor tekstu dla X Window
Name:		gedit
Version:	3.6.2
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gedit/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	7c336819c023a4772cfb48ebe95a7113
URL:		http://www.gnome.org/projects/gedit/
BuildRequires:	autoconf >= 2.63.2
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	enchant-devel >= 1.2.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.2.0
BuildRequires:	gtk+3-devel >= 3.6.0
BuildRequires:	gtksourceview3-devel >= 3.0.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	iso-codes >= 0.35
BuildRequires:	libpeas-devel >= 1.1.0
BuildRequires:	libpeas-gtk-devel >= 1.1.0
BuildRequires:	libsoup-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	libzeitgeist-devel >= 0.3.2
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.3
BuildRequires:	python-pygobject3-devel >= 3.0.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas >= 3.2.0
Requires:	gtk+3 >= 3.6.0
Requires:	iso-codes >= 0.35
Requires:	libpeas-loader-python >= 1.1.0
Requires:	python-pycairo
Requires:	python-pygobject3 >= 3.0.0
Obsoletes:	gedit-plugins < 2.3.3-2
# sr@Latn vs. sr@latin
Obsoletes:	gedit2
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	skip_post_check_so libgedit-private.so.0.0.0

%description
gedit is a small but powerful text editor for GTK+ and/or GNOME. It
includes such features as split-screen mode, a plugin API, which
allows gedit to be extended to support many features while remaining
small at its core, multiple document editing and many more functions.

%description -l pl.UTF-8
gedit jest małym ale potężnym edytorem tekstu dla GTK+ i/lub GNOME.
Zawiera takie funkcje jak tryb podzielonego ekranu, API dla "wtyczek",
który umożliwia rozszerzenie funkcji gedita o dodatkowe możliwości,
nie zwiększając rozmiarów samego programu, możliwość edycji wielu
dokumentów naraz i wiele innych.

%package devel
Summary:	gedit header files
Summary(pl.UTF-8):	Pliki nagłówkowe gedit
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtksourceview3-devel >= 3.0.0
Requires:	libpeas-devel >= 1.1.0
Requires:	libpeas-gtk-devel >= 1.1.0
Obsoletes:	gedit2-devel

%description devel
gedit header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe gedit.

%package apidocs
Summary:	gedit API documentation
Summary(pl.UTF-8):	Dokumentacja API gedit
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	gedit2-apidocs

%description apidocs
gedit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API gedit.

%prep
%setup -q

%build
%{__gtkdocize}
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-updater \
	--enable-gtk-doc \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gedit/plugins/*.la \
	$RPM_BUILD_ROOT%{_libdir}/gedit/plugins/*/*.py \
	$RPM_BUILD_ROOT%{_libdir}/gedit/*.la

%py_postclean

%find_lang gedit --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%glib_compile_schemas

%postun
%update_desktop_database_postun
%glib_compile_schemas

%files -f gedit.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS
%attr(755,root,root) %{_bindir}/gedit
%attr(755,root,root) %{_bindir}/gnome-text-editor
%dir %{_libdir}/gedit
%attr(755,root,root) %{_libdir}/gedit/libgedit-private.so
%dir %{_libdir}/gedit/plugins
%attr(755,root,root) %{_libdir}/gedit/gedit-bugreport.sh
%attr(755,root,root) %{_libdir}/gedit/plugins/*.so
%{_libdir}/gedit/plugins/*.plugin
%dir %{_libdir}/gedit/plugins/externaltools
%{_libdir}/gedit/plugins/externaltools/*.py[co]
%dir %{_libdir}/gedit/plugins/pythonconsole
%{_libdir}/gedit/plugins/pythonconsole/*.py[co]
%dir %{_libdir}/gedit/plugins/snippets
%{_libdir}/gedit/plugins/snippets/*.py[co]
%dir %{_libdir}/gedit/plugins/quickopen
%{_libdir}/gedit/plugins/quickopen/*.py[co]
%dir %{_libdir}/gedit/girepository-1.0
%{_libdir}/gedit/girepository-1.0/Gedit-3.0.typelib
%{_datadir}/gedit
%{_datadir}/GConf/gsettings/gedit.convert
%{_datadir}/dbus-1/services/org.gnome.gedit.service
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.externaltools.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.pythonconsole.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_desktopdir}/gedit.desktop
%{_mandir}/man1/gedit.1*
%{py_sitedir}/gi/overrides/*.py[co]

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-3.0
%{_pkgconfigdir}/gedit.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gedit
