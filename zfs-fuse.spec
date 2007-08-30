%define	snap	beta1
Summary:	ZFS Filesystem for FUSE/Linux
Summary(pl.UTF-8):	System plików ZFS dla Linuksa z FUSE
Name:		zfs-fuse
Version:	0.4.0
Release:	0.%{snap}.1
License:	CCDL 1.0
Group:		Applications/Emulators
Source0:	http://download.berlios.de/zfs-fuse/%{name}-%{version}_%{snap}.tar.bz2
# Source0-md5:	994329d660aa5dce7429eaee86426010
URL:		http://www.wizy.org/wiki/ZFS_on_FUSE
BuildRequires:	libfuse-devel
BuildRequires:	rpmbuild(macros) >= 1.337
BuildRequires:	scons
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZFS has many features which can benefit all kinds of users - from the
simple end-user to the biggest enterprise systems. ZFS list of
features:
- Provable integrity - it checksums all data (and meta-data), which
  makes it possible to detect hardware errors (hard disk corruption,
  flaky IDE cables...).
- Atomic updates - means that the on-disk state is consistent at all
  times, there's no need to perform a lengthy filesystem check after
  forced reboots/power failures.
- Instantaneous snapshots and clones - it makes it possible to have
  hourly, daily and weekly backups efficiently, as well as experiment
  with new system configurations without any risks.
- Built-in (optional) compression
- Highly scalable
- Pooled storage model - creating filesystems is as easy as creating a
  new directory. You can efficiently have thousands of filesystems,
  each with it's own quotas and reservations, and different properties
  (compression algorithm, checksum algorithm, etc..).
- Built-in stripes (RAID-0), mirrors (RAID-1) and RAID-Z (it's like
  software RAID-5, but more efficient due to ZFS's copy-on-write
  transactional model).
- Among others (variable sector sizes, adaptive endianness, ...)

%description -l pl.UTF-8
ZFS ma wiele możliwości, które mogą zadowolić wielu użytkowników - od
zwykłych użytkowników końcowych do największych systemów
korporacyjnych. Oto lista możliwości:
- kontrolowana integralność - wszystkie dane (i metadane) mają
  obliczane sumy kontrole, które umożliwiają wykrywanie błędów
  sprzętowych (uszkodzeń twardych dysków, niesprawnych kabli IDE).
- atomowe uaktualnienia - stan na dysku zawsze jest spójny, nie
  ma potrzeby wykonywania długiego sprawdzania systemu plików po
  wymuszonych rebootach czy utracie zasilania.
- natychmiastowe migawki i kopie - można mieć godzinne, dzienne i
  tygodniowe kopie zapasowe w sposób wydajny, a także eksperymentować
  z nowymi konfiguracjami systemu plików bez żadnego ryzyka.
- wbudowana (opcjonalna) kompresja
- duża skalowalność
- model przechowywania danych oparty na pulach - tworzenie systemu
  plików jest tak łatwe, jak utworzenie nowego katalogu. Można w
  sposób wydajny mieć tysiące systemów plików, każdy z nich z własnymi
  ograniczeniami (quotą) i rezerwacjami oraz różnymi właściwościami
  (algorytmem kompresji, algorytmem sum kontrolnych itp.).
- wbudowany RAID-0 (striping), RAID-1 (mirroring) i RAID-Z (podobny do
  programowego RAID-5, ale bardziej wydajny dzięki modelowi
  transakcyjnemu ZFS-a z kopiowaniem przy zapisie (copy-on-write)).
- wiele innych (różne rozmiary sektora, adaptacyjna kolejność bajtów w
  słowie...).

%prep
%setup -q -n %{name}-%{version}_%{snap}

sed -i -e 's#-Werror##g' src/SConstruct

%build
cd src
%scons \
	%{!?debug:dist=1} \
	CCFLAGS="%{rpmcflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

cd src
%scons install \
	install_dir=$RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES HACKING INSTALL LICENSE README STATUS TESTING TODO
%attr(755,root,root) %{_bindir}/*
