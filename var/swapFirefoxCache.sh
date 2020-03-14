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

TMP_ZIP_FNAME="oldFirefoxCache.zip"
if [[ $2 ]];then TMP_ZIP_FNAME=$2;fi 
timeStamp="$(date --iso-8601=minutes | perl -pe 's/[^0-9]+//g')"
#eventually avoid overwrite previous write
if [[ -f $TMP_ZIP_FNAME ]];then TMP_ZIP_FNAME="oldFirefoxCache.new.zip"$timeStamp;fi
echo "using [to restore zipped firefox cache ] actual firefox will be saved in $TMP_ZIP_FNAME"
sleep 2
zip -r0 $TMP_ZIP_FNAME .cache/mozilla
zip -r0 $TMP_ZIP_FNAME .mozilla
echo "possible: rm -rf .mozilla .cache/mozilla "
if [[ $1 ]];then 
	rm -rf .mozilla .cache/mozilla
	unzip $1
	rm $1
fi
