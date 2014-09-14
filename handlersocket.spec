# NOTE: plugin itself is built within main mysql/percona-server package
%include	/usr/lib/rpm/macros.perl
Summary:	HandlerSocket plugin for MySQL
Summary(pl.UTF-8):	Wtyczka HandlerSocket dla MySQL-a
Name:		handlersocket
Version:	1.1.1
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://github.com/DeNA/HandlerSocket-Plugin-for-MySQL/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7c634126b93a38af23bc0052b60c2130
URL:		https://github.com/DeNA/HandlerSocket-Plugin-for-MySQL
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	perl-devel >= 1:5.10
BuildRequires:	rpm-perlprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HandlerSocket is a NoSQL plugin for MySQL. It works as a daemon inside
the mysqld process, accept TCP connections, and execute requests from
clients. HandlerSocket does not support SQL queries. Instead, it
supports simple CRUD operations on tables.

%description -l pl.UTF-8
HandlerSocket to wtyczka NoSQL dla MySQL-a. Działa jako demon wewnątrz
procesu mysqld, przyjmuje połączenia TCP i wykonuje żądania od
klientów. HandlerSocket nie obsługuje zapytań SQL, a jedynie proste
operacje CRUD na tabelach.

%package client
Summary:	HandlerSocket client program
Summary(pl.UTF-8):	Program kliencki HandlerSocket
Group:		Applications/Databases
Requires:	libhsclient = %{version}-%{release}

%description client
HandlerSocket is a NoSQL plugin for MySQL. It works as a daemon inside
the mysqld process, accept TCP connections, and execute requests from
clients. HandlerSocket does not support SQL queries. Instead, it
supports simple CRUD operations on tables.

This package contains command line client.

%description client -l pl.UTF-8
HandlerSocket to wtyczka NoSQL dla MySQL-a. Działa jako demon wewnątrz
procesu mysqld, przyjmuje połączenia TCP i wykonuje żądania od
klientów. HandlerSocket nie obsługuje zapytań SQL, a jedynie proste
operacje CRUD na tabelach.

Ten pakiet zawiera klienta działającego z linii poleceń.

%package -n libhsclient
Summary:	HandlerSocket client library
Summary(pl.UTF-8):	Biblioteka kliencka HandlerSocket
Group:		Libraries

%description -n libhsclient
HandlerSocket is a NoSQL plugin for MySQL. It works as a daemon inside
the mysqld process, accept TCP connections, and execute requests from
clients. HandlerSocket does not support SQL queries. Instead, it
supports simple CRUD operations on tables.

This package contains C++ client library.

%description -n libhsclient -l pl.UTF-8
HandlerSocket to wtyczka NoSQL dla MySQL-a. Działa jako demon wewnątrz
procesu mysqld, przyjmuje połączenia TCP i wykonuje żądania od
klientów. HandlerSocket nie obsługuje zapytań SQL, a jedynie proste
operacje CRUD na tabelach.

Ten pakiet zawiera bibliotekę kliencką C++.

%package -n libhsclient-devel
Summary:	Header files for HandlerSocket client library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki klienckiej HandlerSocket
Group:		Development/Libraries
Requires:	libhsclient = %{version}-%{release}
Requires:	libstdc++-devel

%description -n libhsclient-devel
Header files for HandlerSocket client library.

%description -n libhsclient-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki klienckiej HandlerSocket.

%package -n libhsclient-static
Summary:	Static HandlerSocket client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka HandlerSocket
Group:		Development/Libraries
Requires:	libhsclient-devel = %{version}-%{release}

%description -n libhsclient-static
Static HandlerSocket client library.

%description -n libhsclient-static -l pl.UTF-8
Statyczna biblioteka kliencka HandlerSocket.

%package -n perl-Net-HandlerSocket
Summary:	HandlerSocket client library for Perl
Summary(pl.UTF-8):	Biblioteka kliencka HandlerSocket dla Perla
Group:		Development/Languages/Perl
Requires:	libhsclient = %{version}-%{release}

%description -n perl-Net-HandlerSocket
HandlerSocket is a NoSQL plugin for MySQL. It works as a daemon inside
the mysqld process, accept TCP connections, and execute requests from
clients. HandlerSocket does not support SQL queries. Instead, it
supports simple CRUD operations on tables.

This package contains Perl client library.

%description -n perl-Net-HandlerSocket -l pl.UTF-8
HandlerSocket to wtyczka NoSQL dla MySQL-a. Działa jako demon wewnątrz
procesu mysqld, przyjmuje połączenia TCP i wykonuje żądania od
klientów. HandlerSocket nie obsługuje zapytań SQL, a jedynie proste
operacje CRUD na tabelach.

Ten pakiet zawiera bibliotekę kliencką dla Perla.

%prep
%setup -q -n HandlerSocket-Plugin-for-MySQL-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-handlersocket_server

%{__make} \
	libhsclient_la_LDFLAGS=

# not build when not building plugin
%{__make} -C client hsclient \
	hsclient_LDADD='$(top_builddir)/libhsclient/libhsclient.la' \
	hsclient_LDFLAGS=

cd perl-Net-HandlerSocket
%{__perl} Makefile.PL \
	CC="%{__cxx}" \
	OPTIMIZE="%{rpmcxxflags}" \
	INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D client/hsclient $RPM_BUILD_ROOT%{_bindir}/hsclient

%{__make} -C perl-Net-HandlerSocket pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libhsclient -p /sbin/ldconfig
%postun	-n libhsclient -p /sbin/ldconfig

%files client
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README docs-en
%lang(ja) %doc docs-ja
%attr(755,root,root) %{_bindir}/hsclient

%files -n libhsclient
%defattr(644,root,root,755)
%doc libhsclient/COPYRIGHT.txt
%attr(755,root,root) %{_libdir}/libhsclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhsclient.so.0

%files -n libhsclient-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhsclient.so
%{_libdir}/libhsclient.la
%{_includedir}/handlersocket

%files -n libhsclient-static
%defattr(644,root,root,755)
%{_libdir}/libhsclient.a

%files -n perl-Net-HandlerSocket
%defattr(644,root,root,755)
%doc perl-Net-HandlerSocket/{COPYRIGHT.txt,Changes,README}
%{perl_vendorarch}/Net/HandlerSocket.pm
%{perl_vendorarch}/Net/HandlerSocket
%dir %{perl_vendorarch}/auto/Net/HandlerSocket
%attr(755,root,root) %{perl_vendorarch}/auto/Net/HandlerSocket/HandlerSocket.so
%{_mandir}/man3/Net::HandlerSocket.3pm*
