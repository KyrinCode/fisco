#!/bin/bash

set -e

# hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.38 10.21.4.39)
hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.38 10.21.4.39)
len=${#hosts[@]}
ports={8545..8554}
workspace="~/fisco/wallet/src/fisco-client"

WAIT_LOCK="/tmp/wait.lock"
wait_it(){
	tmp_lock=$2
	if [[ -f $tmp_lock ]]; then rm $tmp_lock ; fi
	touch $tmp_lock
	# 数文件记录，只要记录数大于等于进程数，表明运行结束
	while [[ $(cat $tmp_lock | wc -l) -lt $1 ]]; do
		sleep 10
	done
}

for i in ${hosts[@]}; do
	(ssh fisco@$i "conda activate fisco && cd $workspace && bash test_peak.sh 127.0.0.1 8545" && echo "1" >> $WAIT_LOCK)&
done
wait_it $len $WAIT_LOCK