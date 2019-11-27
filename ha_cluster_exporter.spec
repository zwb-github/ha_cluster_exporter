Name:           prometheus-ha_cluster_exporter
# Version will be processed by the set_version source service
Version:        %%VERSION%%
Release:        0
License:        Apache-2.0
Summary:        Prometheus exporter for Pacemaker HA clusters metrics
Group:          System/Monitoring
Url:            https://github.com/ClusterLabs/ha_cluster_exporter
Source:         %{name}-%{version}.tar.gz
ExclusiveArch:  aarch64 x86_64 ppc64le s390x
Provides:       ha_cluster_exporter = %{version}-%{release}
Provides:       prometheus(ha_cluster_exporter) = %{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# Make sure that the binary is not getting stripped.
%undefine _build_create_debug
%define __arch_install_post export NO_BRP_STRIP_DEBUG=true

%description
Prometheus exporter for Pacemaker HA clusters metrics

%prep
%setup -q -c # unpack project sources

%define shortname ha_cluster_exporter

%install

# Install the binary.
install -D -m 0755 %{shortname}-%{version}-%{_arch} "%{buildroot}%{_bindir}/%{shortname}"

# Install the systemd unit
install -D -m 0644 %{shortname}.service %{buildroot}%{_unitdir}/%{name}.service

# Install compat wrapper for legacy init systems
install -Dd -m 0755 %{buildroot}%{_sbindir}
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rc%{name}

%pre
%service_add_pre %{name}.service

%post
%service_add_post %{name}.service

%preun
%service_del_preun %{name}.service

%postun
%service_del_postun %{name}.service

%files
%defattr(-,root,root)
%doc *.md
%doc doc/*
%if 0%{?suse_version} >= 1500
%license LICENSE
%else
%doc LICENSE
%endif
%{_bindir}/%{shortname}
%{_unitdir}/%{name}.service
%{_sbindir}/rc%{name}

%changelog
