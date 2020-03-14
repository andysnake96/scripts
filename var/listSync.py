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
#sync 2 list of file by using filename (last part of unix path /) as file unique key, so discarding duplicate in list (same file in other path)
#merge 1 list with another showing missing filename in list 1 and remote duplicates
import sys
def listLoadNoDuplicates(filename):
	#return created filename list --> paths and  duplicates path
	filelist=open(filename)
	paths=filelist.readlines()
	#paths.sort()
	outList=dict()					#output list of filename -> path
	duplicates=list()				#duplicate filenames
	for path in paths:
		filenameKey=(path.split("/")[-1])[:-1]
		if outList.get(filenameKey)!=None:
			duplicates.append(path[:-1])
			#continue
		else:
			outList[filenameKey]=path[:-1]
	return outList,duplicates

def mergeLists(dstList,srcList):
	#merge scrList in dstList
	#return missing files path and already knownd paths
	missingFiles=list()			#missing file path of files in dst list 
	alreadyOwnedFiles=list()
	for kv in list(srcList.items()):
		filename=kv[0]
		filePath=kv[1]
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
def printList(l):
	for i in l:
		print(i)

VERBOSE=False
if __name__=="__main__":
	fileListLocal=sys.argv[1]
	srcList,b=	listLoadNoDuplicates(fileListLocal)
        if VERBOSE:
	    print("\nlocal duplicates:")
	    printList(b)
	if len(sys.argv)>2:
		fileListRemote=sys.argv[2]
		remList,b=	listLoadNoDuplicates(fileListRemote)
                if VERBOSE
		    print("\nremote duplicates:")
		    printList(b)
		missing,dup=mergeLists(srcList,remList)
		print("\nMISSING IN LOCAL FROM REMOTE")
		printList(missing)
                if VERBOSE
		    print("\nALREADY OWNED IN LOCAL")
		    printList(dup)
