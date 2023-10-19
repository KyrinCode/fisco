#!/bin/bash

# Connent to every single chain and launch clients with test_eth2.sh
# Parameter 1: round_id
# Parameter 2: tx_cnt_array

set -e

hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.37 10.21.4.38 10.21.4.39)
len=${#hosts[@]}
# ports={8545..8554}
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

txs=()
for x in $2; do
	# echo ${#txs[@]}
	# echo $x
	txs[${#txs[@]}]=$x
done
# echo ${txs[*]}
for ((i=0; i<len; i++)); do
	(
		for g in {1..2}; do
			(
				echo $i "bash test_eth.sh ${hosts[$i]} $g $1 ${txs[$(($i*2+g-1))]}"
				ssh fisco@${hosts[$i]} "conda activate fisco && cd $workspace && bash test_eth.sh ${hosts[$i]} $g $1 ${txs[$(($i*2+g-1))]}" && echo "1" >> $WAIT_LOCK
			)&
		done
	)&
done
wait_it $(($len*2)) $WAIT_LOCK