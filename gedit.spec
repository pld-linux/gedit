Summary:	gedit - small but powerful text editor for X Window
Summary(pl):	gedit - ma³y ale potê¿ny edytor tekstu dla X Window
Name:		gedit2
Version:	2.16.1
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/gnome/sources/gedit/2.16/gedit-%{version}.tar.bz2
# Source0-md5:	989bf8c2726d12fb825014f3b2d7e587
Patch0:		%{name}-use_default_font.patch
Patch1:		%{name}-desktop.patch
URL:		http://gedit.sourceforge.net/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	ORBit2-devel >= 1:2.14.3
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	eel-devel >= 2.16.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gnome-doc-utils >= 0.8.0
BuildRequires:	gnome-menus-devel >= 2.16.0
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	gtksourceview-devel >= 1.8.1
BuildRequires:	intltool >= 0.35
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeprintui-devel >= 2.12.1
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-gnome-desktop-devel >= 2.16.0
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper >= 0.3.12
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	libgnomeprintui >= 2.12.1
Requires:	libgnomeui >= 2.16.0
Requires:	python-gnome-desktop-gtksourceview >= 2.16.0
Requires:	gnome-vfs2 >= 2.16.1
Obsoletes:	gedit-devel
Obsoletes:	gedit-plugins < 2.3.3-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gedit is a small but powerful text editor for GTK+ and/or GNOME. It
includes such features as split-screen mode, a plugin API, which
allows gedit to be extended to support many features while remaining
small at its core, multiple document editing and many more functions.

%description -l pl
gedit jest ma³ym ale potê¿nym edytorem tekstu dla GTK+ i/lub GNOME.
Zawiera takie funkcje jak tryb podzielonego ekranu, API dla "wtyczek",
który umo¿liwia rozszerzenie funkcji gedita o dodatkowe mo¿liwo¶ci,
nie zwiêkszaj±c rozmiarów samego programu, mo¿liwo¶æ edycji wielu
dokumentów naraz i wiele innych.

%package devel
Summary:	gedit header files
Summary(pl):	pliki nag³ówkowe gedit
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	eel-devel >= 2.16.0
Requires:	gtksourceview-devel >= 1.8.1
Requires:	libglade2-devel >= 1:2.6.0
Requires:	libgnomeprintui-devel >= 2.12.1
Requires:	libgnomeui-devel >= 2.16.0

%description devel
gedit header files

%description devel -l pl
Pliki nag³ówkowe gedit.

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
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--with-omf-dir=%{_omf_dest_dir}/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
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
%doc README ChangeLog TODO AUTHORS
%{_sysconfdir}/gconf/schemas/gedit.schemas
%{_sysconfdir}/gconf/schemas/gedit-file-browser.schemas
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/gedit-2
%dir %{_libdir}/gedit-2/plugins
%dir %{_libdir}/gedit-2/plugins/externaltools
%dir %{_libdir}/gedit-2/plugins/pythonconsole
%dir %{_libdir}/gedit-2/plugins/snippets
%attr(755,root,root) %{_libdir}/gedit-2/plugins/*.so
%{_libdir}/gedit-2/plugins/externaltools/*.glade
%{_libdir}/gedit-2/plugins/externaltools/*.py[co]
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_libdir}/gedit-2/plugins/*.py[co]
%{_libdir}/gedit-2/plugins/pythonconsole/*.py[co]
%{_libdir}/gedit-2/plugins/snippets/*.glade
%{_libdir}/gedit-2/plugins/snippets/*.py[co]
%{_datadir}/gedit-2
%{_desktopdir}/*
%{_mandir}/man1/*
%{_omf_dest_dir}/%{name}
%{_omf_dest_dir}/gedit

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-*
%{_pkgconfigdir}/gedit-*.pc
%{_gtkdocdir}/gedit
