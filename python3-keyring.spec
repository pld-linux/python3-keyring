#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# py.test tests

%define 	module	keyring
Summary:	Python 3 library to access the system keyring service
Summary(pl.UTF-8):	Biblioteka Pythona 3 do dostępu do systemowego pęku kluczy
Name:		python3-%{module}
Version:	24.2.0
Release:	1
License:	MIT, PSF
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/keyring
Source0:	https://files.pythonhosted.org/packages/source/k/keyring/%{module}-%{version}.tar.gz
# Source0-md5:	ed5df85d33c36bb268a79d4472a13312
URL:		https://pypi.python.org/pypi/keyring
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.15.0
%if %{with tests}
#BuildRequires:	python3-black >= 0.3.7
#BuildRequires:	python3-checkdocs >= 2.4
#BuildRequires:	python3-cov
%if "%{py3_ver}" != "3.12"
BuildRequires:	python3-importlib_metadata >= 4.11.4
%endif
%if "%{py3_ver}" == "3.8"
BuildRequires:	python3-importlib_resources
%endif
BuildRequires:	python3-jaraco.classes
BuildRequires:	python3-jeepney >= 0.4.2
#BuildRequires:	python3-mypy >= 0.9.1
BuildRequires:	python3-pytest >= 6
#BuildRequires:	python3-pytest-enabler >= 1.3
BuildRequires:	python3-pytest-flake8
#BuildRequires:	python3-ruff
BuildRequires:	python3-secretstorage >= 3.2
%endif
%if %{with doc}
BuildRequires:	python3-Sphinx >= 3.5
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-rst.linker >= 1.9
#BuildRequires:	python3-sphinx-lint
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.8
# kwalletd5 through dbus
Suggests:	python3-dbus
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python keyring library provides a easy way to access the system
keyring service from Python. It can be used in any application that
needs safe password storage.

%description -l pl.UTF-8
Biblioteka Pythona keyring udostępnia prosty sposób dostępu do usługi
systemowego pęku kluczy z poziomu Pythona. Może być używana w dowolnej
aplikacji wymagającej bezpiecznego przechowywania haseł.

%package apidocs
Summary:	API documentation for Python keyring library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Pythona keyring
Group:		Documentation

%description apidocs
API documentation for Python keyring library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Pythona keyring.

%prep
%setup -q -n %{module}-%{version}

cat >setup.py <<EOF
from setuptools import setup
setup()
EOF

%build
%py3_build %{?with_doc:build_sphinx}

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_flake8" \
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

# "keyring" name is too generic, add -py[version] suffix
%{__mv} $RPM_BUILD_ROOT%{_bindir}/keyring{,-py3}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst
%attr(755,root,root) %{_bindir}/keyring-py3
%{py3_sitescriptdir}/keyring
%{py3_sitescriptdir}/keyring-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build-3/sphinx/html/{_static,*.html,*.js}
%endif
