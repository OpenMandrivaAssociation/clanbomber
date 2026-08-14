%define Summary A free (GPL) Bomberman-like multiplayer game

Summary:	%{Summary}
Name:		clanbomber
Version:	2.1.1
Release:	4
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
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	python
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
# Boost.Asio 1.87+ removed io_service, address::from_string, resolver::query
sed -i \
	-e 's/boost::asio::io_service/boost::asio::io_context/g' \
	-e 's/address::from_string/make_address/g' \
	src/Server.h src/Client.h src/Server.cpp src/Client.cpp
python3 - <<'PY'
from pathlib import Path
import re
for name in ("src/Client.cpp", "src/Server.cpp"):
    p = Path(name)
    t = p.read_text()
    t = re.sub(
        r'tcp::resolver::query query\(([^;]+)\);\s*tcp::endpoint endpoint = \*resolver\.resolve\(query\);',
        r'tcp::endpoint endpoint = *resolver.resolve(\1);',
        t, flags=re.S)
    # udp::resolver::query query(host, port);  x = *resolver.resolve(query);
    t = re.sub(
        r'(udp::resolver::)query query\(([^;]+)\);',
        r'// \1query(\2);',
        t)
    t = t.replace('*resolver.resolve(query)', '*resolver.resolve(server_name, net_server_udp_port.str())')
    # leftover tcp resolve(query) if the first regex missed protocol-first form
    t = t.replace(
        'tcp::resolver::query query(tcp::v4(), server_name, net_server_tcp_port.str());',
        '')
    t = t.replace(
        '*resolver.resolve(query)',
        '*resolver.resolve(server_name, net_server_tcp_port.str()).begin()')
    t = t.replace(
        '*resolver.resolve(tcp::v4(), server_name, net_server_tcp_port.str())',
        '*resolver.resolve(server_name, net_server_tcp_port.str()).begin()')
    t = t.replace(
        '*resolver.resolve(server_name, net_server_udp_port.str())',
        '*resolver.resolve(server_name, net_server_udp_port.str()).begin()')
    t = t.replace('address.from_string(client_ip)',
                  'address = boost::asio::ip::make_address(client_ip)')
    p.write_text(t)
PY

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
