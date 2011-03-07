Summary:	gedit - small but powerful text editor for X Window
Summary(pl.UTF-8):	gedit - mały ale potężny edytor tekstu dla X Window
Name:		gedit2
Version:	2.91.8
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gedit/2.91/gedit-%{version}.tar.bz2
# Source0-md5:	d72bc4ce5267dd7f3cf404887ad9d37a
URL:		http://www.gnome.org/projects/gedit/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.10
BuildRequires:	docbook-dtd412-xml
BuildRequires:	enchant-devel >= 1.2.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gtk+3-devel >= 3.0.2
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	gtksourceview3-devel >= 2.10.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	iso-codes >= 0.35
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.3
#BuildRequires:	python-gtksourceview2-devel >= 2.10.0
#BuildRequires:	python-pygobject-devel >= 2.27.91
#BuildRequires:	python-pygtk-devel >= 2:2.12.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper >= 0.3.12
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	libpeas-devel >= 0.7.2
BuildRequires:	libpeas-gtk-devel >= 0.7.2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	libpeas-loader-python
Suggests:	python-vte
Obsoletes:	gedit-devel
Obsoletes:	gedit-plugins < 2.3.3-2
# sr@Latn vs. sr@latin
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
Requires:	gtksourceview2-devel >= 2.9.7

%description devel
gedit header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe gedit.

%package apidocs
Summary:	gedit API documentation
Summary(pl.UTF-8):	Dokumentacja API gedit
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
gedit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API gedit.

%prep
%setup -q -n gedit-%{version}
sed -i 's/^en@shaw//' po/LINGUAS
%{__rm} po/en@shaw.po

%build
%{__gtkdocize}
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-scrollkeeper \
	--disable-silent-rules \
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
	$RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang gedit --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%scrollkeeper_update_post
%update_desktop_database_post

%postun
/sbin/ldconfig
%scrollkeeper_update_postun
%update_desktop_database_postun

%files -f gedit.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS
%attr(755,root,root) %{_bindir}/gedit
%attr(755,root,root) %{_bindir}/gnome-text-editor
%attr(755,root,root) %{_libdir}/libgedit-private.so.*.*.*
%ghost %{_libdir}/libgedit-private.so.0
%dir %{_libdir}/gedit
%dir %{_libdir}/gedit/plugins
%dir %{_libdir}/gedit/plugins/pythonconsole
%dir %{_libdir}/gedit/plugins/quickopen
%attr(755,root,root) %{_libdir}/gedit/gedit-bugreport.sh
%attr(755,root,root) %{_libdir}/gedit/plugins/*.so
%{_libdir}/gedit/plugins/*.plugin
%{_libdir}/gedit/plugins/pythonconsole/*.py[co]
%{_libdir}/gedit/plugins/quickopen/*.py[co]
%dir %{_libdir}/gedit/girepository-1.0
%{_libdir}/gedit/girepository-1.0/Gedit-3.0.typelib
%{_datadir}/gedit
%{_datadir}/GConf/gsettings/gedit.convert
%{_datadir}/dbus-1/services/org.gnome.gedit.service
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.pythonconsole.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_desktopdir}/gedit.desktop
%{_mandir}/man1/gedit.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgedit-private.so
%{_includedir}/gedit-3.0
%{_pkgconfigdir}/gedit.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gedit
