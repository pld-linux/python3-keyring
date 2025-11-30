#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# pytest tests

%define		module	keyring
Summary:	Python 3 library to access the system keyring service
Summary(pl.UTF-8):	Biblioteka Pythona 3 do dostępu do systemowego pęku kluczy
Name:		python3-%{module}
Version:	25.7.0
Release:	1
License:	MIT, PSF
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/keyring
Source0:	https://files.pythonhosted.org/packages/source/k/keyring/%{module}-%{version}.tar.gz
# Source0-md5:	57c23d340e4d08ac4896f142ee423eca
URL:		https://pypi.python.org/pypi/keyring
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-setuptools >= 1:77
BuildRequires:	python3-setuptools_scm >= 3.4.1
%if %{with tests}
#BuildRequires:	python3-black >= 0.3.7
#BuildRequires:	python3-checkdocs >= 2.4
#BuildRequires:	python3-cov
%if "%{_ver_lt %{py3_ver} 3.12}" == "1"
BuildRequires:	python3-importlib_metadata >= 4.11.4
%endif
BuildRequires:	python3-jaraco.classes
BuildRequires:	python3-jaraco.context
BuildRequires:	python3-jaraco.functools
BuildRequires:	python3-jeepney >= 0.4.2
BuildRequires:	python3-pyfakefs
#BuildRequires:	python3-pygobject-stubs
BuildRequires:	python3-pytest >= 6
# lint only
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-enabler >= 3.4
#BuildRequires:	python3-pytest-flake8
#BuildRequires:	python3-pytest-mypy >= 1.0.1
#BuildRequires:	python3-pytest-ruff >= 0.2.1
BuildRequires:	python3-secretstorage >= 3.2
#BuildRequires:	python3-shtab >= 1.1.0
#BuildRequires:	python3-types-pywin32
%endif
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9.3
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-rst.linker >= 1.9
#BuildRequires:	python3-sphinx-lint
BuildRequires:	sphinx-pdg-3 >= 3.5
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
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

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

# "keyring" name is too generic, add -py[version] suffix
%{__mv} $RPM_BUILD_ROOT%{_bindir}/keyring{,-py3}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst SECURITY.md
%attr(755,root,root) %{_bindir}/keyring-py3
%{py3_sitescriptdir}/keyring
%{py3_sitescriptdir}/keyring-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build-3/sphinx/html/{_static,*.html,*.js}
%endif
