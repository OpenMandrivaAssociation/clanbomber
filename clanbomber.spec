%define Summary A free (GPL) Bomberman-like multiplayer game

Summary:	%{Summary}
Name:		clanbomber
Version:	2.1.1
Release:	3
License:	GPL
Group:		Games/Arcade
URL:		https://savannah.nongnu.org/projects/clanbomber/
Source0:	https://download.savannah.gnu.org/releases/clanbomber/%{name}-%{version}.tar.lzma
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch1:		gcc7-fixes.patch
Patch2:		clanbomber-2.1.1-mageia-boost-filesystem.patch
Patch3:		clang.patch
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(sdl) >= 1.2.0
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(SDL_ttf)
BuildRequires:	pkgconfig(SDL_gfx)
BuildRequires:	gettext-devel

%description
ClanBomber is a free (GPL) Bomberman-like multiplayer game that uses ClanLib, a
free multi platform C++ game SDK. First "ClanBomber" was only a working title
for a small game started in September 1998, that has only been started to learn
how to use ClanLib. But the ClanBomber project has grown into a real game. It
is fully playable and features Computer controlled bombers, however, it is
recommended to play ClanBomber with friends (3-8 players are really fun).

%prep

%autosetup -p1


# make autoreconf happy
sed -i -e 's,dist-lzma,subdir-objects,' -e 's,-Werror,,' configure.ac

%build
autoreconf -fi
# (gc) workaround g++ exception bug when -fomit-frame-pointer is set
export CFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer -Wno-c++11-narrowing"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer -Wno-c++11-narrowing"
%configure --bindir=%{_gamesbindir} --datadir=%{_gamesdatadir} --with-boost-libdir=%{_libdir}
%make_build

%install

%makeinstall_std

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png


# XDG menu
install -d %{buildroot}%{_datadir}/applications
mv %{buildroot}%{_gamesdatadir}/applications/*.desktop %{buildroot}%{_datadir}/applications/

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_gamesbindir}/*
%{_gamesdatadir}/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
