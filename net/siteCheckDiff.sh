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
#! /bin/bash

#script that redownload index file from a site,and check if something has changed from old copy of index previously download ( or 1st time init file..)

#CONFIGS
INDEX_URL="http://www.ce.uniroma2.it/courses/sdcc1819/"
OLDINDEX_FILENAME="index_old.html"
NEWINDEX_FILENAME="index.html"
RINGTONE_FILENAME="jeffs_models.mp3" #music used as ringtone on founded differences in site..
#CHECK IF OLD INDEX DOES EXIST..
if [ ! -f "$OLDINDEX_FILENAME" ]
then
    echo "not founded old index... init..."
    echo EMPTY > $OLDINDEX_FILENAME
fi

#re download index
curl $INDEX_URL > $NEWINDEX_FILENAME
curl_resoult=$?
if [ $curl_resoult != 0 ]
then
	echo "curl has failed :(((("
	exit
fi

#checking differences
diff $NEWINDEX_FILENAME $OLDINDEX_FILENAME 
diff_resoult=$?
echo $diff_resoult
#UPDATE OLDINDEX_FILENAME
cat $NEWINDEX_FILENAME > $OLDINDEX_FILENAME 

if [ $diff_resoult != 0 ]
then
	echo "SHOUD RE MIRROR SITE... ?"
	cvlc $RINGTONE_FILENAME --audio --play-and-exit
fi

