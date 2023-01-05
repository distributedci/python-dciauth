%global srcname dciauth
%global summary DCI authentication module used by dci-control-server and python-dciclient

Name:           python-%{srcname}
Version:        3.0.0
Release:        1%{?dist}
Summary:        %{summary}

License:        ASL 2.0
URL:            https://github.com/redhat-cip/python-%{srcname}
Source0:        %{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description
%{summary}

%package -n python3-%{srcname}
Summary: %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

# This will tell dnf/yum to install python3-dciauth when user searches for python-dciauth
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}

%{summary}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*.egg-info
%dir %{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}/*

%changelog
* Fri Jan 06 2023 Guillaume Vincent <gvincent@redhat.com> 3.0.0-1
- Build dciauth for python3 only

* Thu Aug 25 2022 Frederic Lepied <flepied@redhat.com> 2.1.7-3
- Rebuild for RHEL 9 (2nd try)

* Wed Aug 24 2022 Frederic Lepied <flepied@redhat.com> - 2.1.7-2
- Rebuild for RHEL 9

* Mon Feb 08 2021 Guillaume Vincent <gvincent@redhat.com> - 2.1.7-1
- Use the same timestamp to generate the signature

* Mon Feb 08 2021 Guillaume Vincent <gvincent@redhat.com> - 2.1.6-1
- Add logging

* Fri Dec 04 2020 Yassine Lamgarchal <ylamgarc@redhat.com > - 2.1.5-1
- Transform data in is_valid method into binary string

* Tue Jun 16 2020 Haïkel Guémar <hguemar@fedoraproject.org> - 2.1.4-3
- Make it a single-stack package on EL7/EL8

* Mon Jun 08 2020 Bill Peck <bpeck@redhat.com> 2.1.4-2
- Rebuild for RHEL-8
- Rebase to python36 on EL8

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
