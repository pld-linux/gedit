Summary:	gEdit - small but powerful text editor for X Window
Summary(pl):	gEdit - ma³y ale potê¿ny edytor tekstu dla X Window
Name:		gedit2
Version:	2.3.3
Release:	2
License:	GPL
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/gnome/sources/gedit/2.3/gedit-%{version}.tar.bz2
# Source0-md5:	e5db5597561219b87cafaee5fa63be52
URL:		http://gedit.sourceforge.net/
BuildRequires:	GConf2-devel >= 2.2.0
BuildRequires:	aspell-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	eel-devel >= 2.2.0
BuildRequires:	glib2-devel >= 2.2.0
BuildRequires:	gtksourceview-devel >= 0.4.0
BuildRequires:	intltool >= 0.25
BuildRequires:	libbonoboui-devel >= 2.2.0
BuildRequires:	libglade2-devel >= 2.0.1
BuildRequires:	libgnomeprintui-devel >= 2.2.1
BuildRequires:	libgnomeui-devel >= 2.2.0
BuildRequires:	libtool
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper >= 0.3.11
BuildRequires:	xft-devel >= 2.1.2
Requires(post,postun):	scrollkeeper
Requires:	libgnomeprintui >= 2.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	gedit-devel
Obsoletes:	gedit-plugins < 2.3.3-2

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
Requires:	%{name} = %{version}

%description devel
gEdit header files

%description devel -l pl
Pliki nag³ówkowe gEdit.

%prep
%setup -q -n gedit-%{version}

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}/%{name}

# Remove obsoleted *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/*.la

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
scrollkeeper-update
%gconf_schema_install
/sbin/ldconfig

%postun
scrollkeeper-update
/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog TODO AUTHORS THANKS
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/gedit-2
%dir %{_libdir}/gedit-2/plugins
%attr(755,root,root) %{_libdir}/bonobo/libgedit-control.so
%attr(755,root,root) %{_libdir}/gedit-2/plugins/*.so*
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_libdir}/bonobo/servers/*
%{_pixmapsdir}/*
%{_datadir}/application-registry/*
%{_desktopdir}/*
%{_datadir}/gedit-2
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/mime-info/*
%{_datadir}/idl/*
%{_omf_dest_dir}/%{name}
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/gedit-2.4
%{_pkgconfigdir}/gedit-2.4.pc
