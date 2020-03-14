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
#!/usr/bin/env python3
from re import findall
metadataLines=open("a").readlines()
time=""
metadata=""
size=""
i=0
grouppedDict=dict()
#TODO SWITCH 
for l in metadataLines:
	fields=l.split("\t\t")
	fname=fields[0]
	fmetadata=fields[1]
	ftime=fields[2]
	fsize=findall("[0-9]{3,4}x[0-9]+",fields[1])[0]


	if ftime!=time or fsize!=size:
	##if ftime!=time or fmetadata!=metadata:
	#if ftime!=time:
		i+=1
		if grouppedDict.get(i)==None:
			grouppedDict[i]=[]
			#print(i)
	if ftime!=time:
		time=ftime
	if fsize!=metadata:
		size=fsize
	if fmetadata!=metadata:
		metadata=fmetadata
	grouppedDict[i].append(fname)

names=""
for i,name in grouppedDict.items():
	for n in name:
		names+=" "+n
	print(names,i)
	names=""

