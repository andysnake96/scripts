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
#!/usr/bin/bash
#download concurrently files from link passed by argv  in a number of process configurable in CONCURRENCY_DOWNLOAD variable
#links will be parsed by xargs from passed file and download handled with wget setting fake headers 
FILE_LIST=$1
CONCURRENCY_DOWNLOAD=5
SET_FAKE_BROSWER_HEADER="--header=\"User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0\" --header=\"Accept: image/png,image/*;q=0.8,*/*;q=0.5\" --header=\"Accept-Language: en-US,en;q=0.5\""
echo $FAKE_BROSWER_HEADER
echo "WGETTING ALL FILE FROM LINES OF LINKS FROM FILE "$FILE_LIST
echo "R.B. NO SPACES 1 LINK PER LINE "
cat $FILE_LIST | xargs -d "\n" -L 1 -n 1 -P $CONCURRENCY_DOWNLOAD wget $(SET_FAKE_BROSWER_HEADER)
