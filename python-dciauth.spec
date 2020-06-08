%global summary DCI authentication module used by dci-control-server and python-dciclient
%if 0%{?fedora}
%{!?python3_pkgversion: %global python3_pkgversion 3}
%else
%{!?python3_pkgversion: %global python3_pkgversion 34}
%endif

Name:           python-dciauth
Version:        2.1.4
Release:        2%{?dist}
Summary:        DCI authentication module used by dci-control-server and python-dciclient

License:        ASL 2.0
URL:            https://github.com/redhat-cip/python-dciauth
Source0:        dciauth-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
%{summary}

%package -n python2-dciauth
Summary: %{summary}
%{?python_provide:%python_provide python2-dciauth}

%description -n python2-dciauth
%{summary}

%package -n python%{python3_pkgversion}-dciauth
Summary: %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-dciauth}

%description -n python%{python3_pkgversion}-dciauth
%{summary}

%prep
%autosetup -n dciauth-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%files -n python2-dciauth
%license LICENSE
%doc README.md
%{python2_sitelib}/*.egg-info
%dir %{python2_sitelib}/dciauth
%{python2_sitelib}/dciauth/*

%files -n python%{python3_pkgversion}-dciauth
%license LICENSE
%doc README.md
%{python3_sitelib}/*.egg-info
%dir %{python3_sitelib}/dciauth
%{python3_sitelib}/dciauth/*

%changelog
* Mon Jun 08 2020 Bill Peck <bpeck@redhat.com> 2.1.4-2
- Rebuild for RHEL-8

* Wed Apr 8 2020 Guillaume Vincent <gvincent@redhat.com> 2.1.4-1
- Fix payload to string transformation

* Mon Oct 21 2019 Guillaume Vincent <gvincent@redhat.com> 2.1.3-1
- Fix signature calculation for POST request

* Tue Oct 15 2019 Guillaume Vincent <gvincent@redhat.com> 2.1.2-1
- Fix missing v2 module in dist

* Mon Oct 14 2019 Guillaume Vincent <gvincent@redhat.com> 2.1.1-1
- Fix setup.py for pypi upload

* Tue Oct 8 2019 Guillaume Vincent <gvincent@redhat.com> 2.1.0-1
- Add DCI2-HMAC-SHA256 algorithm
- Support AWS4-HMAC-SHA256 algorithm

* Fri Jan 12 2018 Guillaume Vincent <gvincent@redhat.com> 2.0.2-1
- Fix error in signature validation due to time used
- Lower case header request

* Mon Jan 8 2018 Guillaume Vincent <gvincent@redhat.com> 2.0.1-1
- Fix error in signature validation due to uppercase headers

* Mon Dec 18 2017 Guillaume Vincent <gvincent@redhat.com> 2.0.0-1
- Revamp signature mechanism and copy AWS HMAC version 4 mechanism

* Mon Nov 16 2017 Guillaume Vincent <gvincent@redhat.com> 1.0.1-1
- Fix error in payload order

* Mon Nov 15 2017 Guillaume Vincent <gvincent@redhat.com> 1.0.0-1
- change calculate_signature API using params instead of query string

* Mon Nov 13 2017 Guillaume Vincent <gvincent@redhat.com> 0.1.2-1
- dummy patch

* Mon Nov 9 2017 Guillaume Vincent <gvincent@redhat.com> 0.1.1-1
- Fix signatures comparison on python 2

* Mon Nov 6 2017 Guillaume Vincent <gvincent@redhat.com> 0.1.0-1
- Initial commit
