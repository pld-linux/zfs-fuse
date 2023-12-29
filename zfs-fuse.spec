# TODO: systemd units, scrub script
Summary:	ZFS Filesystem for FUSE/Linux
Summary(pl.UTF-8):	System plików ZFS dla Linuksa z FUSE
Name:		zfs-fuse
Version:	0.7.2.2
Release:	1
License:	CCDL v1.0
Group:		Applications/File
#Source0Download: https://github.com/gordan-bobic/zfs-fuse/releases
Source0:	https://github.com/gordan-bobic/zfs-fuse/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8590a93698ada698586cf3215f3be7e6
Source1:	%{name}.init
Patch0:		%{name}-ztest_path.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-python3.patch
Patch3:		%{name}-tirpc.patch
Patch4:		%{name}-format.patch
Patch5:		%{name}-common.patch
Patch6:		%{name}-xattr.patch
URL:		https://github.com/gordan-bobic/zfs-fuse
# also (but no tags)
#URL:		https://github.com/zfs-fuse/zfs-fuse
BuildRequires:	glibc-devel >= 6:2.3.4
BuildRequires:	libaio-devel
BuildRequires:	libfuse-devel >= 2.6.0
BuildRequires:	libtirpc-devel
BuildRequires:	rpmbuild(macros) >= 1.337
BuildRequires:	scons
BuildRequires:	zlib-devel
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
  new directory. You can efficiently have thousands of filesystems, each
  with it's own quotas and reservations, and different properties
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
- atomowe uaktualnienia - stan na dysku zawsze jest spójny, nie ma
  potrzeby wykonywania długiego sprawdzania systemu plików po
  wymuszonych rebootach czy utracie zasilania.
- natychmiastowe migawki i kopie - można mieć godzinne, dzienne i
  tygodniowe kopie zapasowe w sposób wydajny, a także eksperymentować z
  nowymi konfiguracjami systemu plików bez żadnego ryzyka.
- wbudowana (opcjonalna) kompresja
- duża skalowalność
- model przechowywania danych oparty na pulach - tworzenie systemu
  plików jest tak łatwe, jak utworzenie nowego katalogu. Można w sposób
  wydajny mieć tysiące systemów plików, każdy z nich z własnymi
  ograniczeniami (quotą) i rezerwacjami oraz różnymi właściwościami
  (algorytmem kompresji, algorytmem sum kontrolnych itp.).
- wbudowany RAID-0 (striping), RAID-1 (mirroring) i RAID-Z (podobny do
  programowego RAID-5, ale bardziej wydajny dzięki modelowi
  transakcyjnemu ZFS-a z kopiowaniem przy zapisie (copy-on-write)).
- wiele innych (różne rozmiary sektora, adaptacyjna kolejność bajtów w
  słowie...).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
cd src
CC="%{__cc}" \
CFLAGS="%{rpmcflags} -DNDEBUG" \
%scons \
	%{!?debug:dist=1}

%install
rm -rf $RPM_BUILD_ROOT

cd src
CC="%{__cc}" \
CFLAGS="%{rpmcflags} -DNDEBUG" \
%scons install \
	cfg_dir=$RPM_BUILD_ROOT%{_sysconfdir}/zfs-fuse \
	install_dir=$RPM_BUILD_ROOT%{_bindir} \
	man_dir=$RPM_BUILD_ROOT%{_mandir}/man8
cd ..

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/zfs-fuse

install -d $RPM_BUILD_ROOT%{systemdunitdir}
cp -p zfs-fuse*.service $RPM_BUILD_ROOT%{systemdunitdir}

# TODO: zfs-fuse.modules-load zfs-fuse.scrub zfs-fuse.sysconfig zfsrc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
%service -q %{name} stop
/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES LICENSE README README.NFS STATUS TESTING TODO
%attr(755,root,root) %{_bindir}/mount.zfs
%attr(755,root,root) %{_bindir}/zdb
%attr(755,root,root) %{_bindir}/zfs
%attr(755,root,root) %{_bindir}/zfs-fuse
%attr(755,root,root) %{_bindir}/zpool
%attr(755,root,root) %{_bindir}/zstreamdump
%attr(755,root,root) %{_bindir}/ztest
#%{systemdunitdir}/zfs-fuse.service
#%{systemdunitdir}/zfs-fuse-oom.service
#%{systemdunitdir}/zfs-fuse-pid.service
%attr(754,root,root) /etc/rc.d/init.d/zfs-fuse
%dir %{_sysconfdir}/zfs-fuse
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zfs-fuse/zfs_pool_alert
%{_mandir}/man8/zdb.8*
%{_mandir}/man8/zfs-fuse.8*
%{_mandir}/man8/zfs.8*
%{_mandir}/man8/zpool.8*
%{_mandir}/man8/zstreamdump.8*
