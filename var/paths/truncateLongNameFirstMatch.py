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


#recursivelly find and rename all filenames containing a pattern before the end
#e.g. video with .mp4 not at the end of filename
import os,re,sys
def regex(pattern,string):                   
    return re.findall(pattern,string)        

def getFilenamesTree(rootPathStr,pattern=".*mp4"):
    #recursivelly find all filenames (abs path) containing pattern before end of pathname, returning it
    pathnamesTarget=list()
    for root, directories, filenames in os.walk(rootPathStr):
        #print(root,"\t",directories,"\t",filenames)
        for filename in filenames:
            if len(regex(pattern+".+",filename))>0: #regex pattern plus any char consecutive in filename to identify long filename to rename
                pathnamesTarget.append(os.path.join(os.path.abspath(root),filename))
                #pathnamesTarget.append(filename)       #WORK WITHOUT ABS PATH
    return pathnamesTarget

ASK_RENAME_CONFIRM=True
if __name__=="__main__":
    if len(sys.argv)<2:
        print("usage < PATTERN REGEX TO SET TRUNCATION OF FILENAMES RECURSIVELLY, e.g. .*mp4 will truncate recursivelly all filenames at .*mp4")
        exit(1)
    pattern=sys.argv[1]
    patternTruncateRegex="("+pattern+").+"
    for f in getFilenamesTree(".",pattern):
        truncatedFilename=regex(patternTruncateRegex,f)[0]
        if ASK_RENAME_CONFIRM:
            ask="renaming\t"+f+"\t"+truncatedFilename+"?y/n\t\t"
            answ=input(ask)
            if "N" in answ.upper():
                continue        #confirmation denied -> next
        os.rename(f,truncatedFilename)
