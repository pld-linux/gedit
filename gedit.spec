Summary:	gedit - small but powerful text editor for X Window
Summary(pl.UTF-8):	gedit - mały ale potężny edytor tekstu dla X Window
Name:		gedit2
Version:	2.27.5
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gedit/2.27/gedit-%{version}.tar.bz2
# Source0-md5:	f567d96a10490c9bade811b94e855e67
URL:		http://www.gnome.org/projects/gedit/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	enchant-devel >= 1.2.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	gtksourceview2-devel >= 2.4.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	iso-codes >= 0.35
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.3
BuildRequires:	python-gtksourceview2-devel >= 2.2.0
BuildRequires:	python-pygobject-devel >= 2.16.0
BuildRequires:	python-pygtk-devel >= 2:2.12.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper >= 0.3.12
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	python-gtksourceview2 >= 2.2.0
Requires:	python-pygobject >= 2.16.0
Suggests:	python-vte
Obsoletes:	gedit-devel
Obsoletes:	gedit-plugins < 2.3.3-2
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
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

%package devel
Summary:	gedit header files
Summary(pl.UTF-8):	Pliki nagłówkowe gedit
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtksourceview2-devel >= 2.4.0

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
rm po/ca@valencia.po
sed -i s#^ca@valencia## po/LINGUAS

sed -i 's/codegen.py/codegen.pyc/' configure.ac
sed -i 's/h2def.py/h2def.pyc/' configure.ac

%build
%{__gnome_doc_common}
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-install \
	--disable-scrollkeeper \
	--enable-python \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# Remove obsoleted *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/{plugins,plugin-loaders}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.py
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*/*.py
rm -rf $RPM_BUILD_ROOT%{_localedir}/la

%find_lang gedit --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install gedit-file-browser.schemas
%gconf_schema_install gedit.schemas
%scrollkeeper_update_post
%update_desktop_database_post

%preun
%gconf_schema_uninstall gedit-file-browser.schemas
%gconf_schema_uninstall gedit.schemas

%postun
/sbin/ldconfig
%scrollkeeper_update_postun
%update_desktop_database_postun

%files -f gedit.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS
%{_sysconfdir}/gconf/schemas/gedit.schemas
%{_sysconfdir}/gconf/schemas/gedit-file-browser.schemas
%attr(755,root,root) %{_bindir}/gedit
%attr(755,root,root) %{_bindir}/gnome-text-editor
%dir %{_libdir}/gedit-2
%dir %{_libdir}/gedit-2/plugin-loaders
%attr(755,root,root) %{_libdir}/gedit-2/plugin-loaders/*.so
%dir %{_libdir}/gedit-2/plugins
%dir %{_libdir}/gedit-2/plugins/externaltools
%dir %{_libdir}/gedit-2/plugins/pythonconsole
%dir %{_libdir}/gedit-2/plugins/quickopen
%dir %{_libdir}/gedit-2/plugins/snippets
%attr(755,root,root) %{_libdir}/gedit-2/gedit-bugreport.sh
%attr(755,root,root) %{_libdir}/gedit-2/plugins/*.so
%{_libdir}/gedit-2/plugins/externaltools/*.py[co]
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_libdir}/gedit-2/plugins/pythonconsole/*.py[co]
%{_libdir}/gedit-2/plugins/quickopen/*.py[co]
%{_libdir}/gedit-2/plugins/snippets/*.py[co]
%{_datadir}/gedit-2
%{_desktopdir}/gedit.desktop
%{_mandir}/man1/gedit.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-2.20
%{_pkgconfigdir}/gedit-2.20.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gedit
