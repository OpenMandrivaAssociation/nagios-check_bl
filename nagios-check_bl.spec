%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	A Nagios plugin to check against RBL
Name:		nagios-check_bl
Version:	1.0
Release:	%mkrel 9
License:	GPL
Group:		Networking/Other
URL:		http://www.bashton.com/content/nagiosplugins
Source0:	http://www.bashton.com/downloads/%{name}-%{version}.tar.bz2
Requires:	nagios
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
A Nagios plugin to check whether a server is in any known anti-spam blocklists.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/nagios/plugins
install -m  755 check_bl %{buildroot}%{_datadir}/nagios/plugins/

perl -pi -e 's|/usr/lib/nagios|%{_datadir}/nagios|' \
    %{buildroot}%{_datadir}/nagios/plugins/check_bl

install -d -m 755 %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_bl.cfg <<'EOF'
define command {
	command_name    check_bl
	command_line    %{_datadir}/nagios/plugins/check_bl -H $HOSTADDRESS$ -B sbl-xbl.spamhaus.org,bl.spamcop.net
}
EOF

%if %mdkversion < 200900
%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_bl.cfg
%{_datadir}/nagios/plugins/check_bl
