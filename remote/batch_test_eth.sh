#!/bin/bash

hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.37 10.21.4.38 10.21.4.39)
# hosts=(10.21.4.37 10.21.4.38 10.21.4.39)
len=${#hosts[@]}
workspace="~/fisco/wallet/src/fisco-client"

WAIT_LOCK="/tmp/wait0.lock"
wait_it(){
	tmp_lock=$2
	if [[ -f $tmp_lock ]]; then rm $tmp_lock ; fi
	touch $tmp_lock
	# 数文件记录，只要记录数大于等于进程数，表明运行结束
	while [[ $(cat $tmp_lock | wc -l) -lt $1 ]]; do
		sleep 10
	done
}

echo "============= Batch test eth stats0 ============="
for i in ${hosts[@]}; do
	(
		for g in {1..2}; do
			(
				ssh fisco@$i "conda activate fisco && cd $workspace && python test_eth_stats0.py -i $i -g $g" && echo "1" >> $WAIT_LOCK
			)&
		done
	)&
done
wait_it 16 $WAIT_LOCK

echo "============= Batch test eth ============="
python batch_test_eth.py

sleep 10
echo "============= Batch test eth stats1 ============="
for i in ${hosts[@]}; do
	(
		for g in {1..2}; do
			(
				ssh fisco@$i "conda activate fisco && cd $workspace && python test_eth_stats1.py -i $i -g $g" && echo "1" >> $WAIT_LOCK
			)&
		done
	)&
done
wait_it 16 $WAIT_LOCK