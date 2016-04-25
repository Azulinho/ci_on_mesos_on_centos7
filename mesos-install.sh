#!/bin/bash

zypper install -y java-1_7_0-openjdk


cd /tmp

test -e /usr/local/ssl/bin/openssl || {
	wget -c https://openssl.org/source/openssl-1.0.2g.tar.gz
	tar xzf openssl-1.0.2g.tar.gz
	cd openssl-1.0.2g
	./config
	make
	make install
	cd -
}



test -e /usr/local/apr/bin/apr-1-config ||  {
	wget -c http://archive.apache.org/dist/apr/apr-1.5.2.tar.bz2
	tar xjf apr-1.5.2.tar.bz2
	cd apr-1.5.2
	./configure
	make
	make install
	cd -
}

test -e /usr/local/apr/bin/apu-1-config || {
	wget -c http://archive.apache.org/dist/apr/apr-util-1.5.4.tar.bz2
	tar xjf apr-util-1.5.4.tar.bz2
	cd apr-util-1.5.4
	./configure --with-apr=/usr/local/apr
	make
	make install
	cd -
}


test -e /usr/local/bin/sqlite3 || {
	wget -c http://sqlite.org/2016/sqlite-autoconf-3120200.tar.gz
	tar xvzf sqlite-autoconf-3120200.tar.gz
	cd sqlite-autoconf-3120200
	./configure
	make
	make install
	cd -
}

test -e /usr/local/lib/pkgconfig/libffi.pc || {
	wget -c ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz
	tar xzf libffi-3.2.1.tar.gz
	cd libffi-3.2.1
	./configure
	make
	make install
	cd -
}

test -e /usr/local/bin/python || {
	wget -c https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz
	tar xf Python-2.7.11.tar.xz
	cd Python-2.7.11
	./configure
	make
	make install
	cd -
}

test -e /usr/local/bin/scons || {
	wget -c http://downloads.sourceforge.net/scons/scons-2.5.0.tar.gz
	tar xzf scons-2.5.0.tar.gz
	cd scons-2.5.0
	export PATH=/usr/local/bin:$PATH
	python setup.py install 
	cd -
}

test -e /usr/local/lib/libserf-1.so.1.3.0 || {
	wget -c http://serf.googlecode.com/svn/src_releases/serf-1.3.8.tar.bz2
	tar xjf serf-1.3.8.tar.bz2
	cd serf-1.3.8
	export PATH=/usr/local/bin:$PATH
	scons APR=/usr/local/apr/bin/apr-1-config APU=/usr/local/apr/bin/apu-1-config
	scons APR=/usr/local/apr/bin/apr-1-config APU=/usr/local/apr/bin/apu-1-config install
	cd -
}

test -e /usr/local/bin/svnversion || {
	wget -c http://www.apache.org/dist/subversion/subversion-1.9.3.tar.bz2
	tar xjf subversion-1.9.3.tar.bz2
 	cd subversion-1.9.3
	./configure --with-apr=/usr/local/apr/bin/apr-1-config --with-apr-util=/usr/local/apr/bin/apu-1-config
	make
	make install
	cd -
}


test -e /usr/local/apache-maven-3.3.9/bin/mvn || {
	wget -c http://www-eu.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
	tar -C /usr/local -xzf apache-maven-3.3.9-bin.tar.gz
}

test -e /usr/local/bin/curl || {
	wget -c https://curl.haxx.se/download/curl-7.48.0.tar.lzma
	tar xf curl-7.48.0.tar.lzma
	cd curl-7.48.0
	./configure
	make
	make install
	cd -
}

test -e /usr/local/lib/sasl2/ || {
	wget -c ftp://ftp.cyrusimap.org/cyrus-sasl/cyrus-sasl-2.1.26.tar.gz
	tar xzf cyrus-sasl-2.1.26.tar.gz
	cd cyrus-sasl-2.1.26
	./configure --enable-cram  
	make
	make install
	cd -
}

wget -c wget http://www.apache.org/dist/mesos/0.28.0/mesos-0.28.0.tar.gz
tar -xf mesos-0.28.0.tar.gz
cd mesos-0.28.0
mkdir build
cd build
export PATH=/usr/local/bin:$PATH
../configure --with-apr=/usr/local/apr/ --with-apr-util=/usr/local/apr/ --includedir=/usr/local/apr/include/apr-1/ --with-svn=/usr/local/  
make

