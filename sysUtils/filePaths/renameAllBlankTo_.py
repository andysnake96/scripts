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
#!/usr/bin/python3
#recurisvelly replace spaces with _ in files from calling dir
import os
toUnderscorizeChar=[" ","-","$","'",'"']
def getFilenamesTree(rootPathStr):
#recursivelly find all filenames (abs path) containing spaces and return them
    filenamesWithSpaces=list()
    for root, directories, filenames in os.walk(rootPathStr):
        #print(root,"\t",directories,"\t",filenames)
        for filename in filenames:
            for toRenameChar in toUnderscorizeChar:
                if(filename.find(toRenameChar) != -1):
                    print(filename)
                    filenamesWithSpaces.append(os.path.join(os.path.abspath(root),filename))
                    break

                #filenamesWithSpaces.append(filename)       #WORK WITHOUT ABS PATH
    return filenamesWithSpaces

if __name__=="__main__":
    newFn=""
    for f in getFilenamesTree("."):
        newFn=f
        for c in toUnderscorizeChar:
            if(f.find(c) != -1):
                newFn=newFn.replace(c,"_")
        print(f,"->",newFn)
        os.rename(f,newFn)
        #print(f)
