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
import sys
def genSpinnerLine(lineSize,simbol,numSimbolsPerLineMax,separator=" ",start="[",end="]"):
	#generate spinner frames with given linesize simbol to show, max num of simble to show 
	spinnerFrames=list()
	tmp=list()
	frame=str()
	for i in range(lineSize-1,-1,-1):
		if i>=lineSize-1-numSimbolsPerLineMax:#gen first frame by concat of semparator and simbols
			frame=separator*(i)+simbol*(lineSize-i-1)
			#print(frame)
		else:			  #like snake move append on lx new simbol and remove on right
			tmp=list(frame)
			tmp[i]=simbol
			tmp[i+numSimbolsPerLineMax]=separator
			frame="".join(tmp)
			#print(frame,i,i+numSimbolsPerLineMax-1)
		spinnerFrames.append("["+frame+"]")
	#get === fade out removing simbols on end of seq
	for i in range(numSimbolsPerLineMax,-1,-1):
		tmp=list(frame)
		tmp[i]=separator
		frame="".join(tmp)
		#print(frame)
		spinnerFrames.append("["+frame+"]")
	tmp=spinnerFrames[:]
	tmp.reverse()
	spinnerFrames.extend(tmp)
	return spinnerFrames

def basharrayFramePrint(spinnerFrames):
	#bash array print for paste into spinner.sh script
	out="("
	for frame in spinnerFrames:
		out+=' "'+frame+'"'
	out+=")"
	return out
		
if __name__=="__main__":
	lineSize=77
	if len(sys.argv)>1:
		lineSize=int(sys.argv[1])
	char="="
	if len(sys.argv)>2:
		char=sys.argv[2]
	charPerLineMax=5
	if len(sys.argv)>3:
		charPerLineMax=int(sys.argv[3])
	framesArray=genSpinnerLine(lineSize,char,charPerLineMax)
	bashArrayStr=basharrayFramePrint(framesArray)
	print("\n".join(framesArray))
	#print("a=",bashArrayStr)
