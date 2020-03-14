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
def renamerDict(d,BASEPATH="."):
    #rename files in BASEPATH according to value associated to filename key in dict
    #absolute path used by python path module
    absPath=os.path.abspath(BASEPATH)
    for _filename,_newName in d.items():
        filename=os.path.join(absPath,_filename)
        newName=os.path.join(absPath,_newName)
        os.rename(filename,newName)
        
