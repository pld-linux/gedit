Summary:	gedit - small but powerful text editor for X Window
Summary(pl.UTF-8):	gedit - mały ale potężny edytor tekstu dla X Window
Name:		gedit2
Version:	2.19.92
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gedit/2.19/gedit-%{version}.tar.bz2
# Source0-md5:	780644ec80be0938b6860de1d220d684
URL:		http://gedit.sourceforge.net/
BuildRequires:	GConf2-devel >= 2.19.1
BuildRequires:	ORBit2-devel >= 1:2.14.8
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	enchant-devel >= 1.2.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.18.0
BuildRequires:	gnome-doc-utils >= 0.11.2
BuildRequires:	gnome-menus-devel >= 2.19.90
BuildRequires:	gnome-vfs2-devel >= 2.19.91
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	gtk+2-devel >= 2:2.11.6
BuildRequires:	gtksourceview2-devel >= 1.90.4
BuildRequires:	intltool >= 0.36.1
BuildRequires:	iso-codes
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libgnomeprintui-devel >= 2.18.0
BuildRequires:	libgnomeui-devel >= 2.19.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.3
BuildRequires:	python-gtksourceview2-devel >= 1.90.4
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper >= 0.3.12
Requires(post,preun):	GConf2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	libgnomeprintui >= 2.18.0
Requires:	libgnomeui >= 2.19.1
Requires:	python-gnome-desktop-gtksourceview >= 2.18.0
Requires:	gnome-vfs2 >= 2.19.91
Suggests:	python-vte
Obsoletes:	gedit-devel
Obsoletes:	gedit-plugins < 2.3.3-2
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
Requires:	gtksourceview2-devel >= 1.90.4
Requires:	libglade2-devel >= 1:2.6.2
Requires:	libgnomeprintui-devel >= 2.18.0
Requires:	libgnomeui-devel >= 2.19.1

%description devel
gedit header files

%description devel -l pl.UTF-8
Pliki nagłówkowe gedit.

%prep
%setup -q -n gedit-%{version}
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
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--with-omf-dir=%{_omf_dest_dir}/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# Remove obsoleted *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.py
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*/*.py

%find_lang gedit --with-gnome

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
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/gedit-2
%dir %{_libdir}/gedit-2/plugins
%dir %{_libdir}/gedit-2/plugins/externaltools
%dir %{_libdir}/gedit-2/plugins/pythonconsole
%dir %{_libdir}/gedit-2/plugins/snippets
%attr(755,root,root) %{_libdir}/gedit-2/gedit-bugreport.sh
%attr(755,root,root) %{_libdir}/gedit-2/plugins/*.so
%{_libdir}/gedit-2/plugins/externaltools/*.glade
%{_libdir}/gedit-2/plugins/externaltools/*.py[co]
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_libdir}/gedit-2/plugins/pythonconsole/*.py[co]
%{_libdir}/gedit-2/plugins/snippets/*.glade
%{_libdir}/gedit-2/plugins/snippets/*.py[co]
%{_datadir}/gedit-2
%{_desktopdir}/*.desktop
%{_mandir}/man1/*
%{_omf_dest_dir}/%{name}
%{_omf_dest_dir}/gedit

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-*
%{_pkgconfigdir}/gedit-*.pc
%{_gtkdocdir}/gedit
