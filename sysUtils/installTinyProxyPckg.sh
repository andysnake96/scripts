#!/usr/bin/bash
#Copyright Andrea Di Iorio
#This file is part of scripts
#scripts is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#scripts is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with scripts.  If not, see <http://www.gnu.org/licenses/>.
#!bin/bash
STR0="INSTALLING PACKAGES NEEDED FOR THE PROXY"
echo $STR0

yum install -y epel-release
yum update
yum -y install tinyproxy

STR1="INSTALL FINISHED CONFIGURING PROXY"
CONFIG_FILE_PATH="/etc/tinyproxy/tinyproxy.conf"

echo "goto " $CONFIG_FILE_PATH change default port and add Allow ...ip addr
PROXYPORT=9696
IPPAGE="ipecho.net/plain"
MYIP=curl -s $IPPAGE

echo "Allow "$IPPAGE >>$CONFIG_FILE_PATH

echo "NOW SET UP ON YOUR SAFE BROWSER PROXY WITH" $MYIP:$PROXYPORT
