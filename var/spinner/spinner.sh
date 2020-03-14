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
#developped by andysnake96
spinner_base() {
    local i sp n
    sp='/-\|'
    n=${#sp}
    printf ' '
    while sleep 0.1; do
        printf "%s\b" "${sp:i++%n:1}"
    done
}
spinner_echo() {
    local i sp n
    sp=("⢀⠀"  "⡀⠀"  "⠄⠀"  "⢂⠀"  "⡂⠀"  "⠅⠀"  "⢃⠀"  "⡃⠀"  "⠍⠀"  "⢋⠀"  "⡋⠀"  "⠍⠁"  "⢋⠁"  "⡋⠁"  "⠍⠉"  "⠋⠉"  "⠋⠉"  "⠉⠙"  "⠉⠙"  "⠉⠩"  "⠈⢙"  "⠈⡙"  "⢈⠩"  "⡀⢙"  "⠄⡙"  "⢂⠩"  "⡂⢘"  "⠅⡘"  "⢃⠨"  "⡃⢐"  "⠍⡐"  "⢋⠠"  "⡋⢀"  "⠍⡁"  "⢋⠁"  "⡋⠁"  "⠍⠉"  "⠋⠉"  "⠋⠉"  "⠉⠙"  "⠉⠙"  "⠉⠩"  "⠈⢙"  "⠈⡙"  "⠈⠩"  "⠀⢙"  "⠀⡙"  "⠀⠩"  "⠀⢘"  "⠀⡘"  "⠀⠨"  "⠀⢐"  "⠀⡐"  "⠀⠠"  "⠀⢀"  "⠀⡀")
    n=${#sp[@]}
    i=0
    SPINNERS_IN_LINE=33
    echo $n $i ${sp[@]}
    while sleep 0.01; do
    	i=$(((i+1)%n))
    	echo -en "\r"
	for j in $(seq 1 $SPINNERS_IN_LINE);do
		echo -en "${sp[i]} "
	done
    done
}

sp1=("[    ]" "[   =]" "[  ==]" "[ ===]" "[====]" "[=== ]" "[==  ]" "[=   ]")
sp2=("( ●    )" "(  ●   )" "(   ●  )" "(    ● )" "(     ●)" "(    ● )" "(   ●  )" "(  ●   )" "( ●    )" "(●     )")
sp3=("⢀⠀"  "⡀⠀"  "⠄⠀"  "⢂⠀"  "⡂⠀"  "⠅⠀"  "⢃⠀"  "⡃⠀"  "⠍⠀"  "⢋⠀"  "⡋⠀"  "⠍⠁"  "⢋⠁"  "⡋⠁"  "⠍⠉"  "⠋⠉"  "⠋⠉"  "⠉⠙"  "⠉⠙"  "⠉⠩"  "⠈⢙"  "⠈⡙"  "⢈⠩"  "⡀⢙"  "⠄⡙"  "⢂⠩"  "⡂⢘"  "⠅⡘"  "⢃⠨"  "⡃⢐"  "⠍⡐"  "⢋⠠"  "⡋⢀"  "⠍⡁"  "⢋⠁"  "⡋⠁"  "⠍⠉"  "⠋⠉"  "⠋⠉"  "⠉⠙"  "⠉⠙"  "⠉⠩"  "⠈⢙"  "⠈⡙"  "⠈⠩"  "⠀⢙"  "⠀⡙"  "⠀⠩"  "⠀⢘"  "⠀⡘"  "⠀⠨"  "⠀⢐"  "⠀⡐"  "⠀⠠"  "⠀⢀"  "⠀⡀")
spinner() {
    local i n sp
    sp=("${sp3[@]}")
    n=${#sp[@]}
    i=0
    SPINNERS_IN_LINE=3
    #echo $n $i ${sp[@]}
    while sleep 0.1; do
    	i=$(((i+1)%n))
	for j in $(seq 1 $SPINNERS_IN_LINE);do
		printf "%s" "${sp[i]} "
	done
	printf "\r"
    done
}
pythonJsonDecodeSpinnerjson() {
JSON_FILEPATH="spinners.json"
python_scpt_emdd="
import json,sys
a=open(\"$JSON_FILEPATH\")
j=json.load(a)
ks=list(j.keys())
for k in ks:
 print(j[k][\"frames\"])
"
python3 -c "$python_scpt_emdd"
}

_example_spinners_call(){
spinner &
sleep 4  # sleeping for 10 seconds is important work
kill "$!" # kill the spinner
printf '\n'
}

