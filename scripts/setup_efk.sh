#!/bin/bash

#VARIABLES
kibana_version="kibana-4.3.0-linux-x64"
public_ip="52.23.250.243"

if [[ "$EUID" -ne "0" ]]; then
echo 'Run as root!'
exit 51
fi

cd /root/

#Add elasticsearch repo
cat >/etc/yum.repos.d/elasticsearch1.repo <<'EOF';
[elasticsearch-2.x]
name=Elasticsearch repository for 2.x packages
baseurl=http://packages.elastic.co/elasticsearch/2.x/centos
gpgcheck=1
gpgkey=http://packages.elastic.co/GPG-KEY-elasticsearch
enabled=1
EOF

#Import GPG keys for elasticsearch
rpm --import https://packages.elastic.co/GPG-KEY-elasticsearch || { echo -e '\nError importing elasticsearch GPG keys\n'; exit 52; }
echo -e '\nGPG keys imported elasticsearch repo\n'

#Install elasticsearch, java, rubygems, byobu, htop, git, tree, make, glibc-devel, gcc
yum install elasticsearch java-1.7.0-openjdk rubygems ruby-devel make glibc-devel gcc byobu htop git tree -y --enablerepo=epel || { echo -e '\nError installing packages with yum\n'; exit 53; }
echo -e '\nPackages installed\n'

#Install head plugin for elasticsearch
/usr/share/elasticsearch/bin/plugin install mobz/elasticsearch-head  || { echo -e '\nError installing head plugin for elasticsearch\n'; exit 54; }
echo -e '\nHead plugin installed\n'

#Install fluentd & its plugins
curl -L https://toolbelt.treasuredata.com/sh/install-redhat-td-agent2.sh | sh
td-agent-gem install fluent-plugin-elasticsearch || { echo -e '\nError installing elasticsearch plugin for fluentd\n'; exit 55; }
echo -e '\nElasticsearch plugin installed for fluentd\n'

#Download & extract kibana
wget https://download.elastic.co/kibana/kibana/${kibana_version}.tar.gz
tar xvzf ~/${kibana_version}.tar.gz || { echo -e '\nError installing kibana\n'; exit 56; }
echo -e '\nKibana downloaded\n'


#Configure td-agent
cat >/etc/td-agent/td-agent.conf <<'EOF';
<source>
        type tail
        path /dump/test.log
        pos_file /dump/test.log.pos
        format json
        tag frontlayer.qreceiver
</source>

<match *.*>
        @type copy
        <store>
                @type stdout
        </store>
        <store>
                @type elasticsearch
                host localhost
                port 9200
                index_name fluentd
                type_name fluentd
                logstash_format true
                flush_interval 1
        </store>
</match>
EOF


#Configure elasticsearch
sed -i '/network.host\:/c\network.host\: 0.0.0.0' /etc/elasticsearch/elasticsearch.yml || { echo -e '\nError configuring elasticsearch\n'; exit 57; }
echo -e '\nElasticsearch configured\n'

#Configure kibana
sed -i '/elasticsearch.url\:/c\elasticsearch.url\: \"http\:\/\/'"${public_ip}"'\:9200\"' /root/${kibana_version}/config/kibana.yml || { echo -e '\nError configuring kibana\n'; exit 58; }
echo -e '\nKibana configured\n'

echo '
#
## Script completed successfully, now run 
##      service td-agent restart
##      service elasticsearch restart
##      /root/${kibana_version}/bin/kibana
#
'