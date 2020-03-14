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
#GENERATE A TRAILER OF INPUTTED VIDEO AT $1

ffmpeg -i $1 \
       -vf select='lt(mod(t\,1000)\,4)',setpts=N/FRAME_RATE/TB \
       -af aselect='lt(mod(t\,1000)\,4)',asetpts=N/SR/TB \
       TRAILER_$1.mp4
