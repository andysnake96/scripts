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
_tmuxStartTemplate() {
    tmux new-session -d -s sess >/dev/null
    tmux rename-window -t sess:0 'main'
    tmux splitw -v -p 10 -t sess:0.0
    tmux splitw -h -p 80 -t sess:0.1
    #required; otherwise pane numbering is bs
    tmux select-pane -t sess:0.0
    tmux send-keys -t sess:0.0 'sudo htop' Enter
    tmux send-keys -t sess:0.1 'tmux clock -t sess:0.1' Enter
    tmux select-pane -t sess:0.0
    tmux new-window -t sess
    tmux rename-window -t sess:1 'second'
    tmux splitw -v -p 10 -t sess:1.0
    tmux splitw -h -p 80 -t sess:1.1
    tmux select-pane -t sess:1.0
    tmux splitw -h -p 5 -t sess:1.0
    tmux clock -t sess:1.1
    tmux new-window -t sess
    tmux rename-window -t sess:2 'scratch'
    tmux splitw -v -p 10 -t sess:2.0
    tmux select-pane -t sess:2.0
    tmux splitw -h -p 5 -t sess:2.0
    tmux clock -t sess:2.1
    tmux select-window -t sess:0.0
    tmux a -t sess
}
controlSpawn(){
	SESSION="control"
	if [[ $1 ]];then $SESSION=$1;fi
	tmux new-session -d -s $SESSION>/dev/null
    	tmux rename-window -t sess:0 $1
	tmux splitw -v  -t $SESSION:0.0
	#tmux splitw -h -t $SESSION:0.1
	#required; otherwise pane numbering is bs
	tmux select-pane -t $SESSION:0.0
	tmux send-keys -t $SESSION:0.0 'htop' Enter
	tmux send-keys -t $SESSION:0.1 'watch -n 0.5 nvidia-smi' Enter
	tmux a -t $SESSION
}

if [[ $1 ]];then controlSpawn $1;fi
