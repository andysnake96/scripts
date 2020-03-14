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
#sync 2 list of file by using filename (last part of unix path /) as file unique key, so discarding duplicate in list (same file in other path)
#merge 1 list with another showing missing filename in list 1 and remote duplicates
from sys import argv
from os import environ 

#ENVIRON VAR SET TO GET LISTs CMP IN DIFFERENT MODES:
#ovverride path interrpreting modee by these environ variables
MODE_FULL_PATH="MODE_FULL_PATH" #as key for a file is taken all the filename alone (no dir path to it)
MODE_NO_EXTENSIONS="MODE_NO_EXTENSIONS" #as key for a file is taken the the filename alone less the extension part
MODE_NO_EXTENSION_LAST="MODE_NO_EXTENSION_LAST" #as key for a file is taken the the filename alone less the Last extension part

Mode=MODE_FULL_PATH
if environ.get(MODE_FULL_PATH)!=None and "T" in environ.get(MODE_FULL_PATH).upper(): Mode=MODE_FULL_PATH
if environ.get(MODE_NO_EXTENSION_LAST)!=None and "T" in environ.get(MODE_NO_EXTENSION_LAST).upper(): Mode=MODE_NO_EXTENSION_LAST
if environ.get(MODE_NO_EXTENSIONS)  !=None and "T" in environ.get(MODE_NO_EXTENSIONS).upper(): Mode=MODE_NO_EXTENSIONS
##helpers
getFileFullNameKeyFromPath=lambda path: (path.split("/")[-1])
def getFileNoExtensionNameKeyFromPath(path):
    fName=path.split("/")[-1]
    firstDotPos=fName.find(".")
    return fName[:firstDotPos]

def getFileNoExtensionLastNameKeyFromPath(path):
    #return filename excluding last extension
    fileName=path.split("/")[-1]
    for x in range(len(fileName)-1,-1,-1):
        if fileName[x]==".":
            return fileName[:x]
    return fileName
###############

def listLoadNoDuplicates(filename):
    #filename is a .list file or simply a list of filenames path
    #return created filename list --> paths and  duplicates path
    filelist=open(filename)
    paths=filelist.readlines()
    filelist.close()
    
    outList=dict()                  #output list of filename -> path
    duplicates=list()               #duplicate filenames
    for path in paths:
        if Mode==MODE_FULL_PATH: getK=getFileFullNameKeyFromPath
        elif Mode==MODE_NO_EXTENSION_LAST: getK=getFileNoExtensionLastNameKeyFromPath
        elif Mode==MODE_NO_EXTENSIONS: getK=getFileNoExtensionNameKeyFromPath
        filenameKey=getK(path)
        print(filenameKey)
        if outList.get(filenameKey)!=None:
            duplicates.append(path)
        else:
            outList[filenameKey]=path
    return outList,duplicates

def mergeLists(dstList,srcList):
    #merge scrList in dstList
    #return missing files path and already knownd paths ( in destList)
    missingFiles=list()         #missing file path of files in dst list 
    alreadyOwnedFiles=list()
    for filename,filePath in srcList.items():
        if dstList.get(filename)==None:
            dstList[filename]=filePath
            missingFiles.append(filePath)
        else:
            alreadyOwnedFiles.append(filePath)
    return missingFiles,alreadyOwnedFiles

def printDict(d):
    i=list(d.items())
    for kv in i:
        print(kv[0],"-->",kv[1])
def printList(l,header=""):
    for i in l:
        print(header,i)
def cmpLists(listFileName1,listFileName2=""):
    fileListLocal=listFileName1
    srcList,srcDuplicates=listLoadNoDuplicates(fileListLocal)
    remList=""
    if(environ.get("SUPPRESS_LOCAL")==None):
        print("local fileList:")
        printDict(srcList)
        print("local duplicates:")
        printList(srcDuplicates)

    if listFileName2!="":
        fileListRemote=listFileName2
        remList,remDuplicates=  listLoadNoDuplicates(fileListRemote)
       # print("remote fileList:")
       # printDict(remList)
       # print("remote duplicates:")
       # printList(remDuplicates)

        #### COMPARING LISTS BY SETTED MODE
        missing,dup=mergeLists(srcList,remList)
        print("MISSING IN LOCAL FROM REMOTE")
        printList(missing,"MISS")
        print("ALREADY OWNED IN LOCAL")
        printList(dup)
    return {"SRC":srcList,"DST":remList}
    
if __name__=="__main__":
    print("see top Doc for env ovverride: MODE_NO_EXTENSIONS, MODE_NO_EXTENSION_LAST, MODE_FULL_PATH(dflt)\nand OutputMode SUPPRESS_LOCAL ")
    print("ActualMode: ",Mode)
    print("usage: list1FilePath,[list2FilePath]\n if only1 will be filtered duplicates in list1\nif both given searched common and missing items in list1")
    
    if len(argv) > 2: cmpLists(argv[1],argv[2])
    elif len(argv) == 2: cmpLists(argv[1])
    else: raise Exception("Invalid argument given")

