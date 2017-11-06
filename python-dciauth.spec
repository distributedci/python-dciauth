%global library dciauth
%global sum DCI authentication module used by dci-control-server and python-dciclient

Name:           python-%{library}
Version:        1.0.0
Release:        1%{?dist}
Summary:        %{sum}

License:        ASL 2.0
URL:            https://github.com/redhat-cip/python-%{library}
Source0:        %{library}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
%if 0%{?rhel}
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
%else
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif

%description
An python module which provides a convenient example.

%package -n python2-%{library}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{library}}

%description -n python2-%{library}
%{sum}

%package -n python%{python3_pkgversion}-%{library}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{library}}

%description -n python%{python3_pkgversion}-%{library}
%{sum}

%prep
%autosetup -n %{library}-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%files -n python2-%{library}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{library}/*

%files -n python%{python3_pkgversion}-%{library}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{library}/*

%changelog
* Mon Nov 6 2017 Guillaume Vincent <gvincent@redhat.com> 1.0.0
- Initial commit
