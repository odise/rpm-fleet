 Copyright 2014, Jan Nabbefeld
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To Install:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# wget https://raw.github.com/odise/rpm-fleet/master/fleet.spec -O ~/rpmbuild/SPECS/fleet.spec
# wget https://github.com/coreos/etcd/releases/download/v0.8.3/fleet-v0.8.3-linux-amd64.tar.gz -O ~/rpmbuild/SOURCES/fleet-v0.8.3-linux-amd64.tar.gz
# rpmbuild -bb ~/rpmbuild/SPECS/fleet.spec

%define debug_package %{nil}
%define etcd_user  %{name}
%define etcd_group %{name}
%define etcd_data  %{_localstatedir}/lib/%{name}

Name:      fleet
Version:   0.8.3
Release:   1
Summary:   A Distributed init System.
License:   Apache 2.0
URL:       https://github.com/coreos/fleet
Group:     System Environment/Daemons
Source0:   https://github.com/coreos/%{name}/releases/download/v%{version}/%{name}-v%{version}-linux-amd64.tar.gz
#Source1:   %{name}.initd
#Source2:   %{name}.sysconfig
#Source3:   %{name}.nofiles.conf
#Source4:   %{name}.logrotate
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Packager:  Jan Nabbefeld <jan.nabbefeld@kreuzwerker.de>
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%description
Fleet ties together systemd and etcd into a distributed init system. 
Think of it as an extension of systemd that operates at the cluster level
instead of the machine level. This project is very low level and is 
designed as a foundation for higher order orchestration.

%prep
%setup -n %{name}-v%{version}-linux-amd64

%build
rm -rf %{buildroot}

echo  %{buildroot}

%install
install -d -m 755 %{buildroot}/%{_sbindir}
install    -m 755 %{_builddir}/%{name}-v%{version}-linux-amd64/fleetd    %{buildroot}/%{_sbindir}
install    -m 755 %{_builddir}/%{name}-v%{version}-linux-amd64/fleetctl %{buildroot}/%{_sbindir}

#install -d -m 755 %{buildroot}/usr/share/doc/%{name}-v%{version}
#install    -m 644 %{_builddir}/%{name}-v%{version}-linux-amd64/README-etcd.md    %{buildroot}/%{_defaultdocdir}/%{name}-v%{version}
#install    -m 644 %{_builddir}/%{name}-v%{version}-linux-amd64/README-etcdctl.md %{buildroot}/%{_defaultdocdir}/%{name}-v%{version}

#install -d -m 755 %{buildroot}/%{_localstatedir}/log/%{name}
#install -d -m 755 %{buildroot}/%{_localstatedir}/lib/%{name}

#install -d -m 755 %{buildroot}/%{_initrddir}
#install    -m 755 %_sourcedir/%{name}.initd        %{buildroot}/%{_initrddir}/%{name}

#install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
#install    -m 644 %_sourcedir/%{name}.sysconfig    %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

#install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
#install    -m 644 %_sourcedir/%{name}.logrotate    %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

#install -d -m 755 %{buildroot}/%{_sysconfdir}/security/limits.d/
#install    -m 644 %_sourcedir/%{name}.nofiles.conf %{buildroot}/%{_sysconfdir}/security/limits.d/%{name}.nofiles.conf

%clean
rm -rf %{buildroot}

%pre
getent group %{etcd_group} >/dev/null || groupadd -r %{etcd_group}
getent passwd %{etcd_user} >/dev/null || /usr/sbin/useradd --comment "etcd Daemon User" --shell /bin/bash -M -r -g %{etcd_group} --home %{etcd_data} %{etcd_user}

#%post
#chkconfig --add %{name}

#%preun
#if [ $1 = 0 ]; then
#  service %{name} stop > /dev/null 2>&1
#  chkconfig --del %{name}
#fi

%files
%defattr(-,root,root)
%{_sbindir}/fleet*
#%{_defaultdocdir}/%{name}-v%{version}/*.md
#%attr(0755,%{etcd_user},%{etcd_group}) %dir %{_localstatedir}/log/%{name}
#%attr(0755,%{etcd_user},%{etcd_group}) %dir %{_localstatedir}/lib/%{name}
#%{_initrddir}/etcd
#%{_sysconfdir}/logrotate.d/%{name}
#%{_sysconfdir}/security/limits.d/etcd.nofiles.conf
#%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Wed Oct 08 2014 Jan Nabbefeld <jan.nabbefeld@kreuzwerker.de> 0.1.0
- Initial spec.