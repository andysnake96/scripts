#!/usr/bin/bash
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
#take lines from FILENAME, then parse last part of path contained in that file in bash array
export FILENAME="n"
lines=( $(python3 -c $'from os import environ as env\nlines=open(env["FILENAME"]).readlines()\nfor l in lines: print(l.split("/")[-1])') )
#print bash array
for l in ${lines[@]};do echo $l;done

