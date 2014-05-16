%define		php_name	php%{?php_suffix}
%define		modname		uploadprogress
%define		status		stable
Summary:	%{modname} - An extension to track progress of a file upload
Summary(pl.UTF-8):	%{modname} - rozszerzenie do śledzenia postępu przesyłania pliku
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.3.1
Release:	7
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	13fdc39d68e131f37c4e18c3f75aeeda
URL:		http://pecl.php.net/package/uploadprogress/
BuildRequires:	%{php_name}-devel >= 4:5.2.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-uploadprogress < 1.0.3.1-6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extension to track progress of a file upload.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie do śledzenia postępu przesyłania pliku na serwer.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc examples
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
