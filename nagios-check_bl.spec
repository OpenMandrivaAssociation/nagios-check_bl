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


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-9mdv2011.0
+ Revision: 620431
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 1.0-8mdv2010.0
+ Revision: 440197
- rebuild

* Mon Dec 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-7mdv2009.1
+ Revision: 314628
- now a noarch package
- use a herein document for configuration
- reply on filetrigger for reloading nagios

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-6mdv2009.0
+ Revision: 239083
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Apr 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-5mdv2008.0
+ Revision: 13789
- use the new /etc/nagios/plugins.d scandir


* Wed Nov 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-4mdv2007.0
+ Revision: 84571
- Import nagios-check_bl

* Thu Aug 10 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-4mdk
- disable debug packages

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0-3mdk
- this cannot be a noarch package

* Fri Jun 17 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0-2mdk
- nuke dot, fix noarch

* Fri Jun 17 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdk
- initial Mandriva package

