%global debug_package %{nil}

Name:           docker-compose
Version:	1.29.2
Release:	2
Summary:        Multi-container orchestration for Docker

License:        ASL 2.0
URL:            https://github.com/docker/compose
Source0:        https://files.pythonhosted.org/packages/source/d/%{name}/%{name}-%{version}.tar.gz

# docker-compose is compatible with fig and is a simple rename.
# Currently it only prints deprecation warnings for changed functionality.
Provides:       fig = %{version}-%{release}
# Last fig EVR was 1.0.1-2
Obsoletes:      fig <= 1.0.1-3

BuildRequires:  python-devel
BuildRequires:  python-setuptools

Requires:       python-cached-property >= 1.3.0
Requires:       python-docker >= 3.4.1
Requires:       python-docker-pycreds >= 0.3.0
Requires:       python-dockerpty >= 0.4.1
Requires:       python-docopt >= 0.6.2
Requires:       python-idna >= 2.5
Requires:       python-jsonschema >= 2.6.0
Requires:       python-pysocks >= 1.6.7
Requires:       python-requests >= 2.18.4
Requires:       python-setuptools
Requires:       python-six >= 1.10.0
Requires:       python-texttable >= 0.9.1
Requires:       python-websocket-client >= 0.32.0
Requires:       python-yaml >= 3.12
Requires:	python-paramiko >= 2.7.1
BuildArch:      noarch

%description
Compose is a tool for defining and running multi-container Docker
applications. With Compose, you use a Compose file to configure your
application's services. Then, using a single command, you create and
start all the services from your configuration.

Compose is great for development, testing, and staging environments,
as well as CI workflows.

Using Compose is basically a three-step process.

1. Define your app's environment with a Dockerfile so it can be
   reproduced anywhere.
2. Define the services that make up your app in docker-compose.yml so
   they can be run together in an isolated environment:
3. Lastly, run docker-compose up and Compose will start and run your
   entire app.

%prep
%autosetup -p 1

# Remove dependency version constraints not relevant in Fedora/EPEL
sed -e 's/, < [0-9.]\+//' -i setup.py

# https://github.com/docker/compose/issues/4884
sed -e '/requests >= / s/2\.6\.1/2.6.0/' -i setup.py

# Upstream uses an underscore here
rm -r docker_compose.egg-info

%build
%py3_build

%install
%py3_install
install -D -p -m 644 contrib/completion/bash/docker-compose %{buildroot}%{_datadir}/bash-completion/completions/docker-compose
install -D -p -m 644 contrib/completion/zsh/_docker-compose %{buildroot}%{_datadir}/zsh/site-functions/_docker-compose
install -D -p -m 644 contrib/completion/fish/docker-compose.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/docker-compose.fish

%files
%doc CHANGELOG.md
%license LICENSE
%{_bindir}/%{name}
%{python3_sitelib}/*
%{_datadir}/bash-completion
%{_datadir}/zsh
%{_datadir}/fish
