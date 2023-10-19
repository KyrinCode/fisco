#!/bin/bash

# Launch multiple clients to send txs on a single chain with test_eth.py
# Parameter 1: host
# Parameter 2: group_id
# Parameter 3: round_id
# Parameter 4: tx_cnt

set -e

# python test_eth_stats0.py -i $1 -g $2

WAIT_LOCK="/tmp/wait$2.lock"
wait_it(){
	tmp_lock=$2
	if [[ -f $tmp_lock ]]; then rm $tmp_lock ; fi
	touch $tmp_lock
	# 数文件记录，只要记录数大于等于进程数，表明运行结束
	while [[ $(cat $tmp_lock | wc -l) -lt $1 ]]; do
		sleep 10
	done
}

x=$(($4/30))
y=$(($4%30))

for ((i=0; i<$y; i++)); do
	cnt_array[$i]=$(($x+1))
done
for ((i=$y; i<30; i++)); do
	cnt_array[$i]=$x
done

start_array[0]=0
for ((i=1; i<30; i++)); do
	start_array[$i]=$((${start_array[$(($i-1))]}+${cnt_array[$(($i-1))]}))
done

# echo ${cnt_array[*]}
# echo ${start_array[*]}

for j in {8545..8554}; do	
	(
		for k in {1..3}; do
			(
				# echo $1 $2 $j ${cnt_array[$((($j-8545)*3+($k-1)))]}
				idx=$((($j-8545)*3+($k-1)))
				python test_eth.py -i $1 -p $j -g $2 -r $3 -c ${cnt_array[$idx]} -s ${start_array[$idx]} && echo "1" >> $WAIT_LOCK
			)&
		done
	)&
done
wait_it 30 $WAIT_LOCK

# python test_eth_stats1.py -i $1 -g $2