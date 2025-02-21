%undefine _debugsource_packages

Name:		docker-compose
Version:	2.33.1
Release:	1
Summary:	Multi-container orchestration for Docker

License:	ASL 2.0
URL:		https://github.com/docker/compose
Source0:	https://github.com/docker/compose/archive/v%{version}.tar.gz
# go mod vendor ; tar cJf vendor.tar.xz vendor
Source1:	vendor.tar.xz

# docker-compose is compatible with fig and is a simple rename.
# Currently it only prints deprecation warnings for changed functionality.
Provides:	fig = %{version}-%{release}
# Last fig EVR was 1.0.1-2
Obsoletes:	fig <= 1.0.1-3

BuildRequires:  golang >= 1.21
BuildRequires:  make
Requires:       docker >= 24.0.1

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
%autosetup -p 1 -n compose-%{version} -a 1

%build
export GO111MODULE=on
# Thanks to OpenSUSE for sharing their build !
go build \
   -buildmode=pie \
   -trimpath \
   -ldflags="-linkmode=external -s -w -X github.com/docker/compose/v2/internal.Version=%{version}" \
   -o bin/build/docker-compose ./cmd/

%install
install -d -m 0755 %{buildroot}/%{_libexecdir}/docker/cli-plugins
install -p -m 0755 bin/build/%{name} %{buildroot}/%{_libexecdir}/docker/cli-plugins/


%files
%doc BUILDING.md CONTRIBUTING.md README.md MAINTAINERS NOTICE
%license LICENSE
%{_libexecdir}/docker/cli-plugins/%{name}
