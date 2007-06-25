%define	snap	beta1
Summary:	ZFS Filesystem for FUSE/Linux
Name:		zfs-fuse
Version:	0.4.0
Release:	0.%{snap}.1
License:	CCDL 1.0
Group:		Applications/Emulators
Source0:	http://download.berlios.de/zfs-fuse/%{name}-%{version}_%{snap}.tar.bz2
# Source0-md5:	994329d660aa5dce7429eaee86426010
URL:		http://www.wizy.org/wiki/ZFS_on_FUSE
BuildRequires:	libfuse-devel
BuildRequires:	scons
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZFS has many features which can benefit all kinds of users - from the
simple end-user to the biggest enterprise systems. ZFS list of
features:
 - Provable integrity - it checksums all data (and meta-data), which
   makes it possible to detect hardware errors (hard disk corruption,
   flaky IDE cables..). Read how ZFS helped to detect a faulty power
   supply after only two hours of usage, which was previously silently
   corrupting data for almost a year!
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

%prep
%setup -q -n %{name}-%{version}_%{snap}

sed -i -e 's#-Werror##g' src/SConstruct

%build
cd src
%{__scons} \
	%{!?debug:dist=1} \
		CXXFLAGS="%{rpmcflags}"


%install
rm -rf $RPM_BUILD_ROOT

cd src
%{__scons} install \
	install_dir=$RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES HACKING INSTALL LICENSE README STATUS TESTING TODO
%attr(755,root,root) %{_bindir}/*
