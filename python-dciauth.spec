%global modulename python-dciauth
%global sum DCI authentication module used by dci-control-server and python-dciclient

Name:           python-%{modulename}
Version:        1.0.0
Release:        1%{?dist}
Summary:        %{sum}

License:        ASL 2.0
URL:            https://github.com/redhat-cip/python-dciauth
Source0:        dciauth-%{version}.tar.gz

BuildArch:      noarch

%description
An python module which provides a convenient example.

%package -n python2-%{modulename}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{modulename}}

%description -n python2-%{modulename}
%{sum}

%package -n python3-%{modulename}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{modulename}}

%description -n python3-%{modulename}
%{sum}

%prep
%autosetup -n %{modulename}-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%files -n python2-%{modulename}
%license LICENSE
%doc README.md
%{python2_sitelib}/*

%files -n python3-%{modulename}
%license LICENSE
%doc README.md
%{python3_sitelib}/*
%{_bindir}/dciauth

%changelog
* Mon Nov 3 2017 Guillaume Vincent <gvincent@redhat.com> 0.1.0-1
- Initial commit
