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
echo "select WindoW for endless page scroll"
trap "echo -e '\n\nclosing endless loop';exit 1" SIGINT
sleep 2
KEY_PRESS_CLICK="click 1"
KEY_PRESS_RX="Right"
KEY_PRESS_LX="Left"
KEY_PRESS_SCROLL="End" #scroll
#instagram scroll series of a page

#MODE ENDLESS SCROLL
#MODE="SCROLL"
MODE="INSTAGRAM_SCROLL_CLICK_RX"
while true;do
	if [ $MODE == "SCROLL" ]; then
		xdotool key $KEY_PRESS_SCROLL
		sleep 1
	else 
		xdotool key $KEY_PRESS_CLICK 
		sleep 3
		xdotool key $KEY_PRESS_LX
		sleep 1
	fi
done;
