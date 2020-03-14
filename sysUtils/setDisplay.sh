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
sudo mount  /dev/sda1 DATAMOUNTED
sudo mount /dev/sda6 DATA2
sudo mount /dev/sda5 CENTOS/

#sudo ifconfig enp2s0 up
sudo ifup enp2s0
xrandr --newmode "2560x1080_60.00"  230.00  2560 2720 2992 3424  1080 1083 1093 1120 -hsync +vsync
xrandr --addmode DVI-D-1 "2560x1080_60.00"
xrandr --size "2560x1080_60.00"
#create N add new mode resolution for the screen
#arandr
