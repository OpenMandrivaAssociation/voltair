%define oname VoltAir

Summary:	A casual single and local multiplayer game
Name:		  voltair
Version:	1.0
Release:	5
License:	Apache License
Group:		Games/Adventure
Url:		  http://google.github.io/VoltAir
# From git by tag https://github.com/google/VoltAir/archive/v%{version}.tar.gz
Source0:	%{oname}-%{version}.tar.gz
Source1:	%{name}.png
Patch0:		VoltAir-1.0-qmake.patch
Patch1:		VoltAir-1.0-controls.patch
BuildRequires:	imagemagick
BuildRequires:	qmake5
BuildRequires:	liquidfun-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Multimedia)
BuildRequires:	pkgconfig(Qt5Qml) >= 5.3
BuildRequires:	pkgconfig(Qt5Quick)

%description
A casual single and local multiplayer game.

The game features a spunky, speedy robot stranded on an alien planet.
Going as fast as his single wheel will carry him, he flies over ramps,
zips around meteors, and rides geysers in his search for the portal that
will take him home.

%files
%{_gamesbindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%dir %{_libdir}/%{oname}
%{_libdir}/%{oname}/*

#----------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}/%{oname}
%patch0 -p2
%patch1 -p2

%build
%qmake_qt5
%make

%install
make install INSTALL_ROOT=%{buildroot}%{_libdir} STRIP=true

# install wrapper
mkdir -p %{buildroot}%{_gamesbindir}
cat > %{buildroot}%{_gamesbindir}/%{name} << EOF
#!/bin/bash
cd %{_libdir}/%{oname}
./%{oname}
EOF
chmod +x %{buildroot}%{_gamesbindir}/%{name}

# install menu entry
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=%{oname}
Comment=A casual single and local multiplayer game
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;AdventureGame;
EOF

# install menu icons
for N in 16 32 48 64 128;
do
convert %{SOURCE1} -scale ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

