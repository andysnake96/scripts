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

import re,sys
#wrap python regex (substring matching directly) 
##########  USAGES: PATTERN [1) input filename || INPUT STRING SHELL SPLITTED]
#if next flag is true -> usage will be 1) so filename input taken from argv[2] and different output file will be written for each regex match (with a numeric index for filename )
#otherwise usage 2) will be used so input will be taken from argv[2:] and joined with python string lib --> regex matches written on stdout
FILEIO=True 
if len(sys.argv)<2:
    print("usage PATTERN, [ STRING or input filenmae ]")

def regex(pattern,string):
    #wrap python regex api, return a list of matches of pattern inside string
    return re.findall(pattern,string)
def joinRegex(pattern,stringTokenized):
    #join list of string (e.g. tokinzation of bash of redirected input" and apply pattern regex
    stringJoined=" ".join(stringTokenized)
    return regex(pattern,stringJoined)

if __name__=="__main__":
    PATTERN=sys.argv[1]
    STRING=""
    res=0
    if(FILEIO==True):
        f=open(sys.argv[2])
        STRING=[f.read()]
        #f.close()
        res=joinRegex(PATTERN,STRING)
        #res=regex(PATTERN,STRING)
    else:
        STRING_TOKENIZED=sys.argv[2:]
        STRING=" ".join(sys.argv[2:]) 
        res=joinRegex(PATTERN,STRING_TOKENIZED)
    if len(res) ==0:
        print(" searching regex ",PATTERN)
        print(" inside string of len ",len(STRING))
        print("no result founded")
        exit()
    
    for r in range(len(res)):
        #print(r)
        f=open(str(r),"w")
        f.write(res[r])
        f.close()
