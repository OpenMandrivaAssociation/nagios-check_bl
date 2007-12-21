%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	A Nagios plugin to check against RBL
Name:		nagios-check_bl
Version:	1.0
Release:	%mkrel 5
License:	GPL
Group:		Networking/Other
URL:		http://www.bashton.com/content/nagiosplugins
Source0:	http://www.bashton.com/downloads/%{name}-%{version}.tar.bz2
Source1:	check_bl.cfg
Requires:	nagios
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
A Nagios plugin to check whether a server is in any known anti-spam blocklists.

%prep

%setup -q

cp %{SOURCE1} check_bl.cfg

# lib64 fix
perl -pi -e "s|/usr/lib|%{_libdir}|g" check_bl
perl -pi -e "s|_LIBDIR_|%{_libdir}|g" *.cfg

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/nagios/plugins
install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d

install -m0755 check_bl %{buildroot}%{_libdir}/nagios/plugins/
install -m0644 *.cfg %{buildroot}%{_sysconfdir}/nagios/plugins.d/

%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_bl.cfg
%attr(0755,root,root) %{_libdir}/nagios/plugins/check_bl
