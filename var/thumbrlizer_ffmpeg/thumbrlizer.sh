#!/usr/bin/bash
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

regexScript="pythonRegex.py"
regexPattern='Duration: (.*), start'
randTimeScript="randTimeInDuration.py"
JOBS_PATHNAME="jobs.list"
CONCURRENCY_FACTOR=6
for f in $(ls *mp4);do
	#f_duration="$( ./$regexScript $regexPattern $(ffprobe f 2>&1 ))"
	ffprobeData="$(ffprobe $f 2>&1 ))"
	f_duration="$( ./$regexScript 'Duration: (.*), start' $ffprobeData) "
	f_fps="$( ./$regexScript ', (.*) fps,' $ffprobeData )"
	randTime_selected="$( ./$randTimeScript $f_duration $f_fps FRAME )"
	echo duration:  $f_duration randtime:  $randTime_selected
	#ffmpeg -i $f -ss $randTime_selected -vframes 1 -vf fps=1 $f.bmp &
	ffmpeg -i $f -vf "select=eq(n\,50)" -vframes 1 $f.bmp &
done

