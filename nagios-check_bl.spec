%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	A Nagios plugin to check against RBL
Name:		nagios-check_bl
Version:	1.0
Release:	%mkrel 4
License:	GPL
Group:		Networking/Other
URL:		http://www.bashton.com/content/nagiosplugins
Source0:	http://www.bashton.com/downloads/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
A Nagios plugin to check whether a server is in any known
anti-spam blocklists.

%prep

%setup -q

# lib64 fix
perl -pi -e "s|/usr/lib|%{_libdir}|g" check_bl

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/nagios/plugins

install -m0755 check_bl %{buildroot}%{_libdir}/nagios/plugins/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0755,root,root) %{_libdir}/nagios/plugins/check_bl


