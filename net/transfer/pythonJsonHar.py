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
from json import load
from base64 import b64decode
from sys import argv
""" python module for decoding images and vids in har caputre given in argv
    will be created in current dir 1.jpg,2.jpg ... 1.mp4,2.mp4 .... for any img/vid in given har file
"""
"""
    MAIN INSTR FOR INSTAGRAM CAPTURE:
    CAPTURE
"""

if len(argv)<2: 
    print("Usage: har for decoding imgs/vids")
    exit(1)
filename=argv[1]
EXTENSION_IMG=".jpg" 
EXTENSION_VIDS=".mp4" 
f=open(filename)
harParsed=load(f)
base64GreppedImgs=list()
base64GreppedVids=list()
entries=harParsed['log']['entries']
for e in entries:
    respData=e['response']['content']
    if "image" in respData['mimeType']:
        base64GreppedImgs.append(respData['text']) 
    elif "video" in respData['mimeType']:
        base64GreppedVids.append(respData['text']) 
    #TODO POSSIBLE CHECK IN SIZE BY LEN OF BASE64

#de serialize imgs
for i in range(len(base64GreppedImgs)):
    f=open(str(i)+EXTENSION_IMG,"wb")
    f.write(b64decode(base64GreppedImgs[i]))
    f.close()

#de serialize vids 
for i in range(len(base64GreppedVids)):
    f=open(str(i)+EXTENSION_VIDS,"wb")
    f.write(b64decode(base64GreppedVids[i]))
    f.close()
