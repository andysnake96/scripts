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
import json,base64

filename='www.instagram.com_Archive [19-12-20 17-11-09].har'
EXTENSION=".jpg" #extension in grepped and decoded base64 from firefox har
f=open(filename)
harParsed=json.load(f)
base64Grepped=list()
entries=harParsed['log']['entries']
for e in entries:
    respData=e['response']['content']
    if respData['mimeType']=="image/jpeg":
        base64Grepped.append(respData['text']) #TODO may be useful control in size ?

#serialize
for i in range(len(base64Grepped)):
    #f=open(str(i)+".base64","w")
    f=open(str(i)+EXTENSION,"wb")
    f.write(base64.b64decode(base64Grepped[i]))
    f.close()

    
