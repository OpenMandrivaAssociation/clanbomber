%define Summary A free (GPL) Bomberman-like multiplayer game

Summary:	%{Summary}
Name:		clanbomber
Version:	1.05
Release:	%mkrel 13
License:	GPL
Group:		Games/Arcade
URL:		http://clanbomber.sourceforge.net/
Source:		http://www.clanbomber.de/files/%{name}-%{version}.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch8:		clanbomber-1.02a-gcc-3.3.patch
Patch9:		%{name}-0.5-compile-without-xdisplay.patch
Patch10:        clanbomber-1.05-gcc3_4.patch
Patch11:	clanbomber-1.05-newer-make.patch
Patch12:	clanbomber-1.05-fix-build.patch
BuildRequires:	zlib-devel libhermes-devel clanlib0.6-devel libclanlib-mikmod
BuildRequires:	libmikmod-devel libclanlib-sound automake
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ClanBomber is a free (GPL) Bomberman-like multiplayer game that uses ClanLib, a
free multi platform C++ game SDK. First "ClanBomber" was only a working title
for a small game started in September 1998, that has only been started to learn
how to use ClanLib. But the ClanBomber project has grown into a real game. It
is fully playable and features Computer controlled bombers, however, it is
recommended to play ClanBomber with friends (3-8 players are really fun).

%prep

%setup -q
%patch8 -p1 -b .peroyvind
%patch9 -p1 -b .peroyvind
%patch10 -p1
%patch11 -p0
%patch12 -p0

%build
autoreconf -fi
# (gc) workaround g++ exception bug when -fomit-frame-pointer is set
export CFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer" CXXFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer"
%configure2_5x --bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
make

%install
rm -rf %{buildroot}

%makeinstall_std

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png


# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=ClanBomber
Comment=%{Summary}
Exec=soundwrapper %{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README
%{_gamesbindir}/*
%{_gamesdatadir}/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop


