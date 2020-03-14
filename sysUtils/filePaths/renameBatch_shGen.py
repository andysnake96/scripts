#!/usr/bin/python3
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
#!/usr/bin/env python3
#simple script to generate a batch rename sh file
#based on the clip name file CLIPID/name
#will be gen mv CLIPID.mp4 name.mp4\n lines

from sys import argv
idNamesLines=open(argv[1]).readlines()
SUFFIX_RENAME=".mp4"
FILTER_ENTRIES_NAME_CONTAINS=["wm"]
for l in idNamesLines:
	id,name=l.split("/")
	for filter in FILTER_ENTRIES_NAME_CONTAINS:
		if filter.upper() not in name.upper():
			print("mv %s %s\n" % ("prev_"+id+SUFFIX_RENAME,name[:-1]+SUFFIX_RENAME))
