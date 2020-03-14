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
#!/bin/bash
##SEND A LIST OF FILE USING NETCAT

echo "usage LIST_FILE;DEST_IP;DEST_PORT"
#FIRST MESSAGE -> LIST OF FILES THAT WILL BE SENT
LIST_FILE_PATH=$1
DEST_IP=$2
DEST_PORT=$3
SENDER_WAITING_TIME=2
nc $DEST_IP $DEST_PORT -w 1 < $LIST_FILE_PATH

## SEND FILES IN LIST TO DEST

for file in $(cat $LIST_FILE_PATH); do 
	echo sending $file
	sleep $SENDER_WAITING_TIME
	nc $DEST_IP $DEST_PORT -w 1 < $file
done
