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
def getFilenamesTree(rootPathStr):
#recursivelly find all filenames (abs path) containing spaces and return them
    filenamesWithSpaces=list()
    for root, directories, filenames in os.walk(rootPathStr):
        #print(root,"\t",directories,"\t",filenames)
        for filename in filenames:
            if(filename.find(" ") != -1):
                filenamesWithSpaces.append(os.path.join(os.path.abspath(root),filename))
                #filenamesWithSpaces.append(filename)       #WORK WITHOUT ABS PATH
    return filenamesWithSpaces

if __name__=="__main__":
    for f in getFilenamesTree("."):
        os.rename(f,f.replace(" ","_"))	#rename files with space with _ instead of space
        #print(f)
