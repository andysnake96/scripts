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
#!/usr/bin/env bash
#set -e
#CALL THIS SCRIPT IN THE DIRECTORY WITH VIDEO FILES WITH SAME SIZE AND ENCODING
#NO REECODING WILL BE DONE, VERY QUICK ;)

SUPPLMNT_OPT="-an"
CONCAT_LIST="concat.list"
OUT_FN="out.mp4"
ffmpegBuild="~/ffmpeg/bin/ffmpeg"
#SPEED_MOD_SETPTS="0.25*PTS"
echo "usage (ovverride dflt) CONCAT_LIST OUT_FILENAME AUDIO_PATH, exported FFMPEG_TRGT_BUILD=ffmpeg build target path"
echo "dflt usage: $CONCAT_LIST $OUT_FN [$AUDIO]  $ffmpegBuild..... 2 sec to STOP AND KILL "
sleep 2
if [[ $1 ]];then CONCAT_LIST=$1;fi
if [[ $2 ]];then OUT_FN=$2;fi
if [[ $3 ]];then AUDIO=$3;fi
if [[ $FFMPEG_TRGT_BUILD ]];then ffmpeg=$FFMPEG_TRGT_BUILD;fi

genConcatList(){
#gen concat list from current folder 
find . -iname "*mp4" -printf "file '%P'\n" > toConcat.list
}

#concat with given audio in compatible format coping video stream TODO AUDIO ONE ?
if [[ $AUDIO ]];then
	if [[ $SPEED_MOD_SETPTS ]];then 
		echo "SUGGESTED NVIDIA BUILD "
		eval $ffmpegBuild -f concat -safe 0 -i $CONCAT_LIST -i $AUDIO  -filter:v "setpts="$SPEED_MOD_SETPTS -c:v h264_nvenc -c:a copy -map 0:v:0 -map 1:a:0 -shortest $OUT_FN.mkv;
		exit 0;
	fi
	eval ${ffmpegBuild} -f concat -safe 0 -i $CONCAT_LIST -i $AUDIO  -c:v copy -map 0:v:0 -map 1:a:0 -shortest $OUT_FN;
	#echo "${ffmpegBuild} -f concat -safe 0 -i $CONCAT_LIST -i $AUDIO  -c:video copy -map 0:v:0 -map 1:a:0 -shortest $OUT_FN"
	exit 0;
else
	echo "audio not given... concat simply input file list"
	eval ${ffmpegBuild}  -f concat -safe 0 -i $CONCAT_LIST -c:v copy $SUPPLMNT_OPT  $OUT_FN	#RE ENCODE VIDEO IN CONCATENATION
fi
#concat using concatenation of videos and audios of the given list
#ffmpeg -f concat -safe 0 -i $CONCAT_LIST  -c:video copy  $OUT_FN
#ffmpeg -f concat -safe 0 -i $CONCAT_LIST  $OUT_FN				#RE ENCODE VIDEO IN CONCATENATION

#concat with re encoding and 4x time faster and given audio 


