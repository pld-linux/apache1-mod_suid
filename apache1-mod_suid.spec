%define		mod_name	suid
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: execution of scripts under their own uids
Summary(pl):	Modu³ do apache: wykonywanie skryptów pod wskazanym uidem
Name:		apache1-mod_%{mod_name}
Version:	1.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.jdimedia.nl/igmar/mod_%{mod_name}/files/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	1e47d40d8f0404d9faa3040655df44a2
URL:		http://www.jdimedia.nl/igmar/mod_suid/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel
BuildRequires:	zlib-devel
Requires(post,preun):	%{apxs}
Requires:	apache1
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

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
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES.txt README
%attr(755,root,root) %{_pkglibdir}/*
