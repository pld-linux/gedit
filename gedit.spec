Summary:	gedit - small but powerful text editor for X Window
Summary(pl.UTF-8):	gedit - mały ale potężny edytor tekstu dla X Window
Name:		gedit
Version:	3.14.2
Release:	1
License:	GPL v2+
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gedit/3.14/%{name}-%{version}.tar.xz
# Source0-md5:	38a1ac40cf2f042cadf1dbdb65adde80
URL:		http://www.gnome.org/projects/gedit/
BuildRequires:	autoconf >= 2.63.2
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	enchant-devel >= 1.2.0
BuildRequires:	gettext-tools >= 0.18
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.2.0
BuildRequires:	gtk+3-devel >= 3.14.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gtksourceview3-devel >= 3.14.0
BuildRequires:	intltool >= 0.50.1
BuildRequires:	iso-codes >= 0.35
BuildRequires:	libpeas-devel >= 1.7.0
BuildRequires:	libpeas-gtk-devel >= 1.7.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 3.2.3
BuildRequires:	python3-pygobject3-devel >= 3.0.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
BuildRequires:	zeitgeist-devel >= 0.9.12
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.40.0
Requires:	enchant >= 1.2.0
Requires:	glib2 >= 1:2.40.0
Requires:	gsettings-desktop-schemas >= 3.2.0
Requires:	gtk+3 >= 3.14.0
Requires:	gtksourceview3 >= 3.14.0
Requires:	iso-codes >= 0.35
Requires:	libpeas-loader-python3 >= 1.7.0
Requires:	python3-pycairo
Requires:	python3-pygobject3 >= 3.0.0
Requires:	zeitgeist-libs >= 0.9.12
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
# doesn't require base
Requires:	glib2-devel >= 1:2.40.0
Requires:	gtk+3-devel >= 3.14.0
Requires:	gtksourceview3-devel >= 3.14.0
Requires:	libpeas-devel >= 1.7.0
Requires:	libpeas-gtk-devel >= 1.7.0
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
gedit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API gedit.

%package -n vala-gedit
Summary:	gedit API for Vala language
Summary(pl.UTF-8):	API gedit dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala

%description -n vala-gedit
gedit API for Vala language.

%description -n vala-gedit -l pl.UTF-8
API gedit dla języka Vala.

%prep
%setup -q

%build
%{__gtkdocize}
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4 -I libgd
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--disable-updater \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gedit/plugins/*.la \
	$RPM_BUILD_ROOT%{_libdir}/gedit/*.la

%find_lang gedit --with-gnome

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
%doc AUTHORS BUGS ChangeLog MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/gedit
%attr(755,root,root) %{_bindir}/gnome-text-editor
%dir %{_libdir}/gedit
%attr(755,root,root) %{_libdir}/gedit/libgedit.so
%dir %{_libdir}/gedit/plugins
%attr(755,root,root) %{_libdir}/gedit/gedit-bugreport.sh
%attr(755,root,root) %{_libdir}/gedit/plugins/*.so
%{_libdir}/gedit/plugins/*.plugin
%{_libdir}/gedit/plugins/externaltools
%{_libdir}/gedit/plugins/pythonconsole
%{_libdir}/gedit/plugins/snippets
%{_libdir}/gedit/plugins/quickopen
%dir %{_libdir}/gedit/girepository-1.0
%{_libdir}/gedit/girepository-1.0/Gedit-3.0.typelib
%{_datadir}/appdata/org.gnome.gedit.appdata.xml
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
%{_desktopdir}/org.gnome.gedit.desktop
%{_mandir}/man1/gedit.1*
%{py3_sitedir}/gi/overrides/*.py
%{py3_sitedir}/gi/overrides/__pycache__/*.py[co]

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-3.12
%{_pkgconfigdir}/gedit.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gedit

%files -n vala-gedit
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gedit.deps
%{_datadir}/vala/vapi/gedit.vapi
