%define		mod_name	suid
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: execution of scripts under their own uids
Summary(pl):	Modu³ do apache: wykonywanie skryptów pod wskazanym uidem
Name:		apache1-mod_%{mod_name}
Version:	1.1
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.jdimedia.nl/igmar/mod_%{mod_name}/files/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	1e47d40d8f0404d9faa3040655df44a2
URL:		http://www.jdimedia.nl/igmar/mod_suid/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_suid <= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache module: execution of scripts under their own uids per-vhost.

%description -l pl
Modu³ do apache: wykonywanie skryptów pod wskazanym uidem per-vhost.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1.1-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc CHANGES.txt README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
