#!/usr/bin/bash
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
PORT=9669
SENDER_WAITING_TIME=2
LIST_FILE_PATH="toReceive.list"
LIST_FILE_PATH_PARSED="toReceive_parsed.list"
nc -l -p $PORT -q 1 > $LIST_FILE_PATH
python3 takeFilenameRelative.py  $LIST_FILE_PATH > $LIST_FILE_PATH_PARSED
## SEND FILES IN LIST TO DEST
mkdir "RECEIVED"
cd "RECEIVED"
for file in $(cat ../$LIST_FILE_PATH_PARSED); do 
	echo expecting to receive $file
	nc -l -p $PORT -q 1  > $file
done
