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
#!/bin/bash

#get videos tumbrl
CONCURRENCY_LEVEL=4
genTumbrls(){
	#args videosListFile,seekTime,tumbrlSize,[output format]
	#will save in videosBaseDir tumbrls
	
	videosListFile=$1 	#find output like 
	tumbrlTime=$2		#like 00:00:27.000
	tumbrlSize=$3		#like 500x500
	tmbrlFormat="jpg"	#DOTLESS
	if [[ -v $4 ]];then tmbrlFormat=$4;fi
	cat $videosListFile| xargs -d "\n" -n 1 -P $CONCURRENCY_LEVEL -I "%" ffmpeg -i %  -ss $tumbrlTime -vframes 1 -s $tumbrlSize -y %.$tmbrlFormat

}


VIDEO_INFO_EXTENSION="info"
#extract videos infos in separated files  -- ffprobe output --- into calling dir
getVideosInfos(){
	#args videosListFile
	for f in $(cat $1);do
		ffprobe $f 2>&1 | grep "Video :"  > $f.$VIDEO_INFO_EXTENSION ;
		2>&1 ffprobe -loglevel error -show_entries stream=time_base -select_streams v:0 -of csv=p=0 $f 2>&1>> $f.$VIDEO_INFO_EXTENSION;
	done
}
getVideosInfos1File(){
	cat $1  | xargs -n 1 -I "%" sh -c 'echo -ne "%\t\t"  && ffprobe % 2>&1 | grep "Video: " && echo -ne "\t\t" && ffprobe -loglevel error -show_entries stream=time_base -select_streams v:0 -of csv=p=0 % 2>&1'  > a

}
#SEEM SAME EFFECT FROM OUTPUTs DIFF
trimVideo(){
	#input input video,startTime,endTime,outFpath
	ffmpeg -i $1 -filter_complex "[0:v]trim=$2:$3,setpts=PTS-STARTPTS[v0];[0:a]atrim=$2:$3,asetpts=PTS-STARTPTS[a0]" -map "[v0]" -map "[a0]" $4
}
trimVideoSST(){
	#input input video,startTime,endTime,outFpath
	ffmpeg -i $1 -ss $2 -to $3 $4
}
