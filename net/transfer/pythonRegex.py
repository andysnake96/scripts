#!/usr/bin/python3
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

from re import findall
from sys import argv
from os import environ 
#wrap python regex (substring matching directly) 
##########  USAGES: PATTERN [1) input filename || INPUT STRING SHELL SPLITTED]
#if next flag is true -> usage will be 1) so filename input taken from argv[2] and different output file will be written for each regex match (with a numeric index for filename )
#otherwise usage 2) will be used so input will be taken from argv[2:] and joined with python string lib --> regex matches written on stdout
QUIET=False
FILEIO=True 
SERIALIZE_RESULT_TO_FILES=False
PREFIX_OUTPUT=""
SUFFIX_OUTPUT=""
TRAIL_REMOVE_INDEX=0
HEAD_REMOVE_INDEX=0
######env override dflt config
""" exportable variables
    non trivial by name
    TRAIL_REMOVE_INDEX,HEAD_REMOVE_INDEX: outputdata will be cutted in [HEAD_REMOVE_INDEX:TRAIL_REMOVE_INDEX]
"""
if environ.get("SERIALIZE_RESULT_TO_FILES")!=None and "T" in environ["SERIALIZE_RESULT_TO_FILES"].upper(): SERIALIZE_RESULT_TO_FILES=True
if environ.get("FILEIO")!=None and "F" in environ["FILEIO"].upper(): FILEIO=False
if environ.get("PREFIX_OUTPUT")!=None and  len(environ["PREFIX_OUTPUT"])>0: PREFIX_OUTPUT=environ["PREFIX_OUTPUT"]
if environ.get("SUFFIX_OUTPUT")!=None and  len(environ["SUFFIX_OUTPUT"])>0: SUFFIX_OUTPUT=environ["SUFFIX_OUTPUT"]
if environ.get("HEAD_REMOVE_INDEX")!=None and  len(environ["HEAD_REMOVE_INDEX"])>0: HEAD_REMOVE_INDEX=int(environ["HEAD_REMOVE_INDEX"])
if environ.get("TRAIL_REMOVE_INDEX")!=None and  len(environ["TRAIL_REMOVE_INDEX"])>0: TRAIL_REMOVE_INDEX=int(environ["TRAIL_REMOVE_INDEX"])
if environ.get("QUIET")!=None and  "T" in environ["QUIET"].upper(): QUIET=True
if not QUIET:print("EXPORTABLE: SERIALIZE_RESULT_TO_FILES\t FILEIO\t PREFIX_OUTPUT\t SUFFIX_OUTPUT \t TRAIL_REMOVE_INDEX \t HEAD_REMOVE_INDEX")
def regex(pattern,string):
    #wrap python regex api, return a list of matches of pattern inside string
    return findall(pattern,string)
def joinRegex(pattern,stringTokenized):
    #join list of string (e.g. tokinzation of bash of redirected input" and apply pattern regex
    stringJoined=" ".join(stringTokenized)
    return regex(pattern,stringJoined)

if __name__=="__main__":
    if len(argv)<3: 
        print("usage PATTERN, [ STRING or input filenmae ]\ngiven: ",argv)
        exit(1)
    PATTERN=argv[1]
    STRING=""
    res=0
    if(FILEIO==True):
        f=open(argv[2])
        STRING=f.read()
        #f.close()
        res=regex(PATTERN,STRING)
        #res=regex(PATTERN,STRING)
    else:
        STRING_TOKENIZED=argv[2:]
        STRING=" ".join(argv[2:]) 
        res=joinRegex(PATTERN,STRING_TOKENIZED)
    
    if not QUIET:print(" searched for regex ",PATTERN)
    if len(res) ==0:
        print(" inside string of len ",len(STRING))
        print("no result founded")
        exit()

    ############## output founded data
    for r in range(len(res)):
        #if given, cut target data founded in the set
        trgtStr=res[r]
        if TRAIL_REMOVE_INDEX!=0: trgtStr=trgtStr[:TRAIL_REMOVE_INDEX]  
        if HEAD_REMOVE_INDEX!=0: trgtStr=trgtStr[HEAD_REMOVE_INDEX:]
        
        print(PREFIX_OUTPUT+trgtStr+SUFFIX_OUTPUT)
        if SERIALIZE_RESULT_TO_FILES:
            #print(r)
            newFileName=str(r)+".base64"
            f=open(newFileName,"w")
            f.write(PREFIX_OUTPUT+trgtStr+SUFFIX_OUTPUT)
            f.close()
