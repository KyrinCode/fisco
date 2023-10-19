#!/bin/bash

# hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.38 10.21.4.39)
hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.39)
len=${#hosts[@]}

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

# echo "============= Update .bash_profile ============="
# for i in ${hosts[@]}; do
# 	scp ~/Playground/fisco/remote/.bash_profile fisco@$i:~/
# done

echo "============= Show fisco-bcos processes ============="
for i in ${hosts[@]}; do
	echo $i
	ssh fisco@$i "pkill -9 bcos" && echo "1" >> $WAIT_LOCK
done

echo "============= Kill fisco-bcos processes ============="
for i in ${hosts[@]}; do
	(ssh fisco@$i "pkill -9 bcos" && echo "1" >> $WAIT_LOCK)&
done
wait_it $len $WAIT_LOCK

echo "============= Update fisco-bcos workspace ============="
for i in ${hosts[@]}; do
	ssh fisco@$i "rm -rf fisco && mkdir -p fisco/setup"
	scp ~/Playground/fisco/setup/* fisco@$i:~/fisco/setup/
	scp -r ~/Playground/fisco/wallet fisco@$i:~/fisco/
	scp ~/Playground/fisco/remote/requirements.txt fisco@$i:~/fisco/wallet/src/
done

echo "============= Launch fisco-bcos multichain ============="
for i in ${hosts[@]}; do
	(ssh fisco@$i "source ~/.bash_profile && setproxy && cd ~/fisco/setup && bash auto.sh $i" && echo "1" >> $WAIT_LOCK)&
done
wait_it $len $WAIT_LOCK

echo "============= Retrieve sdk_key ============="
for i in ${hosts[@]}; do
	mkdir -p sdk_key/$i && scp -r fisco@$i:~/fisco/setup/nodes/$i/sdk* sdk_key/$i
done

echo "============= Distributee sdk_key ============="
for i in ${hosts[@]}; do
	scp -r sdk_key fisco@$i:~/fisco/wallet/src/python-sdk/bin/
done
scp -r sdk_key fisco@10.21.4.37:~/vue/backend/python-sdk/bin/

# echo "============= (Re)Create python environment ============="
# for i in ${hosts[@]}; do
# 	(ssh fisco@$i "conda remove -y --name fisco --all && conda create -y --name fisco python=3.7 && conda activate fisco && pip install -r ~/fisco/wallet/src/requirements.txt && pip uninstall -y eth-utils eth-account eth-rlp" && echo "1" >> $WAIT_LOCK)&
# done
# wait_it $len $WAIT_LOCK

# echo "============= Test peak speed ============="
# for i in ${hosts[@]}; do
# 	(ssh fisco@$i "conda activate fisco && cd ~/fisco/wallet/src/fisco-client && bash test_peak.sh" && echo "1" >> $WAIT_LOCK)&
# done
# wait_it $len $WAIT_LOCK