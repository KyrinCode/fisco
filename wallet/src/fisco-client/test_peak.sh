#!/bin/bash

set -e

python test_peak_stats0.py -i $1 -p $2

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
for i in {1..2}; do
	(
		# for j in {8545..8554}; do
		for j in {8545..8548}; do
			(
				for k in {1..10}; do
					(
						python test_peak.py -i $1 -g $i -p $j && echo "1" >> $WAIT_LOCK
					)&
				done
				echo "10 clients started..."
			)&
		done
	)&
done
# wait_it 60 $WAIT_LOCK
wait_it 80 $WAIT_LOCK

python test_peak_stats1.py -i $1 -p $2