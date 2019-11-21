Summary:	gedit - small but powerful text editor for X Window
Summary(pl.UTF-8):	gedit - mały ale potężny edytor tekstu dla X Window
Name:		gedit
Version:	3.34.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gedit/3.34/%{name}-%{version}.tar.xz
# Source0-md5:	4bca1d0a13db186cd84619b4bff42238
Patch0:		%{name}-gtkdocdir.patch
URL:		https://wiki.gnome.org/Apps/Gedit
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.18
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gspell-devel >= 0.2.5
BuildRequires:	gsettings-desktop-schemas-devel >= 3.2.0
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gtksourceview4-devel >= 4.0.2
BuildRequires:	iso-codes >= 0.35
BuildRequires:	libpeas-devel >= 1.14.1
BuildRequires:	libpeas-gtk-devel >= 1.14.1
BuildRequires:	libsoup-devel >= 2.60.0
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	meson >= 0.46.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.2.3
BuildRequires:	python3-pygobject3-devel >= 3.0.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.25.1
BuildRequires:	vala-gtksourceview4 >= 4.0.2
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.44.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.44.0
Requires:	gspell >= 0.2.5
Requires:	gsettings-desktop-schemas >= 3.2.0
Requires:	gtk+3 >= 3.22.0
Requires:	gtksourceview4 >= 4.0.2
Requires:	hicolor-icon-theme
Requires:	iso-codes >= 0.35
Requires:	libpeas-loader-python3 >= 1.14.1
Requires:	libsoup >= 2.60.0
Requires:	libxml2 >= 1:2.6.31
Requires:	python3-libs >= 1:3.2.3
Requires:	python3-pycairo
Requires:	python3-pygobject3 >= 3.0.0
Obsoletes:	gedit-plugins < 2.3.3-2
Obsoletes:	gedit2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package libs
Summary:	gedit shared library
Summary(pl.UTF-8):	Biblioteka współdzielona gedit
Group:		Libraries

%description libs
gedit shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona gedit.

%package devel
Summary:	gedit header files
Summary(pl.UTF-8):	Pliki nagłówkowe gedit
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44.0
Requires:	gtk+3-devel >= 3.22.0
Requires:	gtksourceview4-devel >= 4.0.2
Requires:	libpeas-devel >= 1.14.1
Requires:	libpeas-gtk-devel >= 1.14.1
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
Requires:	vala >= 2:0.25.1
Requires:	vala-gtksourceview4 >= 4.0.2
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-gedit
gedit API for Vala language.

%description -n vala-gedit -l pl.UTF-8
API gedit dla języka Vala.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	-Ddocumentation=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%find_lang gedit --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database_post
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%update_desktop_database_postun
%glib_compile_schemas

%files -f gedit.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/gedit
%dir %{_libdir}/gedit/plugins
%attr(755,root,root) %{_libdir}/gedit/plugins/*.so
%{_libdir}/gedit/plugins/*.plugin
%{_libdir}/gedit/plugins/externaltools
%{_libdir}/gedit/plugins/pythonconsole
%{_libdir}/gedit/plugins/snippets
%{_libdir}/gedit/plugins/quickopen
%{py3_sitedir}/gi/overrides/Gedit.py
%{py3_sitedir}/gi/overrides/__pycache__/Gedit.cpython-*.py[co]
%{_datadir}/dbus-1/services/org.gnome.gedit.service
%{_datadir}/gedit/plugins
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.externaltools.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.pythonconsole.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.spell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_datadir}/metainfo/org.gnome.gedit.appdata.xml
%{_desktopdir}/org.gnome.gedit.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.gedit.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.gedit-symbolic.svg
%{_mandir}/man1/gedit.1*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/gedit
%attr(755,root,root) %{_libdir}/gedit/libgedit-3.14.so
%dir %{_libdir}/gedit/girepository-1.0
%{_libdir}/gedit/girepository-1.0/Gedit-3.0.typelib
%dir %{_datadir}/gedit

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-3.14
%dir %{_datadir}/gedit/gir-1.0
%{_datadir}/gedit/gir-1.0/Gedit-3.0.gir
%{_pkgconfigdir}/gedit.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gedit

%files -n vala-gedit
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gedit.deps
%{_datadir}/vala/vapi/gedit.vapi
