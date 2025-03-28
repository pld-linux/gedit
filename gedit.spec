#
# Conditional build:
%bcond_without	apidocs	# plugins API documentation

Summary:	gedit - small but powerful text editor for X Window
Summary(pl.UTF-8):	gedit - mały ale potężny edytor tekstu dla X Window
Name:		gedit
Version:	48.1
Release:	3
License:	GPL v2+
Group:		X11/Applications/Editors
Source0:	https://download.gnome.org/sources/gedit/48/%{name}-%{version}.tar.xz
# Source0-md5:	1aa72a59d51be4597490220af3ad0421
URL:		https://gedit-technology.github.io/apps/gedit/
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.18
BuildRequires:	glib2-devel >= 1:2.76
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gspell-devel >= 1.0
BuildRequires:	gtk+3-devel >= 3.22.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.0}
BuildRequires:	libgedit-amtk-devel >= 5.8
BuildRequires:	libgedit-gtksourceview-devel >= 299
BuildRequires:	libgedit-tepl-devel >= 6.12
BuildRequires:	libpeas-devel >= 1.14.1
BuildRequires:	libpeas-gtk-devel >= 1.14.1
BuildRequires:	meson >= 0.59
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.2.3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.76
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.76
Requires:	gspell >= 1.0
Requires:	gsettings-desktop-schemas >= 3.2.0
Requires:	gtk+3 >= 3.22.0
Requires:	hicolor-icon-theme
Requires:	iso-codes >= 0.35
Requires:	libpeas-loader-python3 >= 1.14.1
Requires:	python3-libs >= 1:3.2.3
Requires:	python3-pycairo
Requires:	python3-pygobject3 >= 3.0.0
Obsoletes:	gedit-plugins < 2.3.3-2
Obsoletes:	gedit2 < 3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		api_ver		48.1

%define		py3_gi_overridesdir	%{py3_sitescriptdir}/gi/overrides

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
Requires:	glib2 >= 1:2.76
Requires:	gtk+3 >= 3.22.0
Requires:	libgedit-amtk >= 5.8
Requires:	libgedit-tepl >= 6.12
Requires:	libpeas >= 1.14.1
Requires:	libpeas-gtk >= 1.14.1

%description libs
gedit shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona gedit.

%package devel
Summary:	gedit header files
Summary(pl.UTF-8):	Pliki nagłówkowe gedit
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.76
Requires:	gtk+3-devel >= 3.22.0
Requires:	libgedit-amtk-devel >= 5.8
Requires:	libgedit-tepl-devel >= 6.12
Requires:	libpeas-devel >= 1.14.1
Requires:	libpeas-gtk-devel >= 1.14.1
Obsoletes:	gedit2-devel < 3
Obsoletes:	vala-gedit < 45

%description devel
gedit header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe gedit.

%package apidocs
Summary:	gedit API documentation
Summary(pl.UTF-8):	Dokumentacja API gedit
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	gedit2-apidocs < 3
BuildArch:	noarch

%description apidocs
gedit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API gedit.

%prep
%setup -q

%build
%meson \
	%{?with_apidocs:-Dgtk_doc=true}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%py3_comp $RPM_BUILD_ROOT%{py3_gi_overridesdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_gi_overridesdir}

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

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
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/gedit
%dir %{_libdir}/gedit/plugins
%attr(755,root,root) %{_libdir}/gedit/plugins/*.so
%{_libdir}/gedit/plugins/*.plugin
%{py3_gi_overridesdir}/Gedit.py
%{py3_gi_overridesdir}/__pycache__/Gedit.cpython-*.py[co]
%{_datadir}/dbus-1/services/org.gnome.gedit.service
%{_datadir}/gedit/plugins
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.spell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_datadir}/metainfo/org.gnome.gedit.metainfo.xml
%{_desktopdir}/org.gnome.gedit.desktop
%{_iconsdir}/hicolor/*x*/apps/org.gnome.gedit.png
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.gedit-symbolic.svg
%{_mandir}/man1/gedit.1*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/gedit
%attr(755,root,root) %{_libdir}/gedit/libgedit-%{api_ver}.so
%dir %{_libdir}/gedit/girepository-1.0
%{_libdir}/gedit/girepository-1.0/Gedit-3.0.typelib
%dir %{_datadir}/gedit

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-%{api_ver}
%dir %{_datadir}/gedit/gir-1.0
%{_datadir}/gedit/gir-1.0/Gedit-3.0.gir
%{_pkgconfigdir}/gedit.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gedit
%endif
