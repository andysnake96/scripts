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
from json import load,loads

#simple script to read (compressed) mono language english dictionry in json
#if compressed mode enabled dict will be decompressed by zip
#[COMPRESSED] DICTIONRY HAVE TO BE IN THE SAME PATH OF THIS SCRIPT 
#endless final loop to search words :)

MODE_COMPRESS=True 	#TOGGLE COMPRESSED MODE
DICTIONARYFILENAME="dictionary.json"
if MODE_COMPRESS:
	from zipfile import ZipFile
	DICTIONARYZIPFILENAME="dictionary.json.zip"
	archive = ZipFile(DICTIONARYZIPFILENAME, 'r')
	extractedData=archive.read(DICTIONARYFILENAME)
	archive.close()
	dictionary=loads(extractedData)
	del archive,extractedData
else:
	dictFile=open(DICTIONARYFILENAME)
	dictionary=load(dictFile)
	dictFile.close()
	del dictFile
d=dictionary
while 1:
	searchK=input()
	try: print(d[searchK])
	except: print("NOT FOUND")
	print("\n"+"#"*96+"\n")
