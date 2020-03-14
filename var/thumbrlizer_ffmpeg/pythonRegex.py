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
#!/usr/bin/env python3
import re,sys

#wrap python regex for easy use just passing in argv PATTERN, STRING(also splitted by shell, re joined with spaces)
if len(sys.argv)<2:
    print("usage PATTERN, STRING")

#join bash tokenization, newline that has separated tokens now are converted inspaces
def regex(pattern,string):
    return re.findall(pattern,string)
def joinRegex(pattern,stringTokenized):
    #join list of string (e.g. tokinzation of bash of redirected input" and apply pattern regex
    stringJoined=" ".join(stringTokenized)
    return regex(pattern,stringJoined)

if __name__=="__main__":
    PATTERN=sys.argv[1]
    STRING_TOKENIZED=sys.argv[2:]
    STRING=" ".join(sys.argv[2:]) 
    res=joinRegex(PATTERN,STRING_TOKENIZED)
    if len(res) ==0:
        print(" searching regex ",PATTERN)
        print(" inside string of len ",len(STRING))
        print("no result founded")
        exit()
    
    for r in res:
        print(r)
