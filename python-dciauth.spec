%global modulename dciauth
%global sum DCI authentication module used by dci-control-server and python-dciclient

Name:           python-%{modulename}
Version:        1.0.0
Release:        1%{?dist}
Summary:        %{sum}

License:        ASL 2.0
URL:            https://github.com/redhat-cip/python-%{modulename}
Source0:        %{modulename}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python%{python3_pkgversion}-devel

%description
An python module which provides a convenient example.

%package -n python2-%{modulename}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{modulename}}

%description -n python2-%{modulename}
%{sum}

%package -n python%{python3_pkgversion}-%{modulename}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modulename}}

%description -n python%{python3_pkgversion}-%{modulename}
%{sum}

%prep
%autosetup -n %{modulename}-%{version}

%build
%py2_build
%py3_build

%install
%py3_install
%py2_install

%files -n python2-%{modulename}
%license LICENSE
%doc README.md
%{python2_sitelib}/*

%files -n python%{python3_pkgversion}-%{modulename}
%license LICENSE
%doc README.md
%{python%{python3_pkgversion}_sitelib}/*
%{_bindir}/%{modulename}

%changelog
* Mon Nov 6 2017 Guillaume Vincent <gvincent@redhat.com> 1.0.0
- Initial commit
