#!/bin/bash

. ~/.profile

ZK_LIBS="$(readlink -f $(which zkCli.sh ) |sed s/'bin\/zkCli.sh//')/lib/*"
ZK_JAR="$(readlink -f $(which zkCli.sh ) |sed s/'bin\/zkCli.sh//')/zookeeper-3.4.6.jar:"

exec {{ nix_bin }}/java \
	-cp "$ZK_JAR:$ZK_LIBS:{{ zookeeper_confdir }}" \
	-Djava.net.preferIPv4Stack=true \
	-Dzookeeper.datadir.autocreate=false \
	org.apache.zookeeper.server.quorum.QuorumPeerMain \
    {{ zookeeper_zoo_cfg }}

