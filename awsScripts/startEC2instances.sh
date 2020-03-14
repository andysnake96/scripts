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
PK_PATH="/home/andysnake/aws/SSNAKE96.pem"
PID_REG_CMD="echo $$ >> newPids.list"
SSH_CMD="ssh -o \"StrictHostKeyChecking no \" -i $PK_PATH ec2-user@"
INIT_WAIT_TIME=300
RESTART_PORT=4444
INSTANCES_HN_FILENAME="instances.list"
BOTO3_WRAP_PYTHON_FILENAME="EC2instances.py"
spawn_terminals_ssh_to_ec2_instances(){
    echo "waiting for initialization of instances"
    sleep $1
    for hostname in $(cat ${INSTANCES_HN_FILENAME} );do
        xfce4-terminal --hold -e "$SSH_CMD$hostname" -T ${hostname}
    done

}

echo -e "usage possibilties:\n\t N -> number of ec2 instances to start from default launch template saving instance public host names in $ INSTANCES_HN_FILENAME"
echo -e "\tspawn -> spawn ssh terminal connected to ec2 instances configured in file $ INSTANCES_HN_FILENAME "
echo -e "\tterminate -> kill all running ec2 instances"


if [[ $1 == "spawn" ]]; then
    spawn_terminals_ssh_to_ec2_instances $2
elif [[ $1 == "terminate" ]]; then
    python3 $BOTO3_WRAP_PYTHON_FILENAME "terminate"
elif [[ $1 == "restart" ]]; then
     for hostname in $(cat ${INSTANCES_HN_FILENAME} );do
        nc ${hostname} ${RESTART_PORT} -q 0 < $INSTANCES_HN_FILENAME
    done
elif [[ $1 == "clean-logs" ]]; then
    aws s3 rm s3://mapreducechunks/ --recursive --exclude "*" --include "log*"
else
	python3 $BOTO3_WRAP_PYTHON_FILENAME $1 > ${INSTANCES_HN_FILENAME}
fi

