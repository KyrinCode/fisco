#!/bin/bash

# hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.38 10.21.4.39)
hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.38 10.21.4.39)
# hosts=(10.21.4.32)


# echo "============= Update .bash_profile ============="
# for i in ${hosts[@]}; do
# 	scp ~/Playground/fisco/remote/.bash_profile fisco@$i:~/
# done

echo "============= Kill fisco-bcos processes ============="
for i in ${hosts[@]}; do
	ssh fisco@$i "pkill -9 bcos"
done

echo "============= Update fisco-bcos workspace ============="
for i in ${hosts[@]}; do
	ssh fisco@$i "rm -rf fisco && mkdir -p fisco/setup"
	scp ~/Playground/fisco/setup/* fisco@$i:~/fisco/setup/
	scp -r ~/Playground/fisco/wallet fisco@$i:~/fisco/
	scp ~/Playground/fisco/remote/requirements.txt fisco@$i:~/fisco/wallet/src/
done

echo "============= Launch fisco-bcos multichain ============="
for i in ${hosts[@]}; do
	ssh fisco@$i "source ~/.bash_profile && setproxy && cd ~/fisco/setup && bash auto.sh $i 4"
done

echo "============= Retrieve sdk_key ============="
for i in ${hosts[@]}; do
	mkdir -p sdk_key/$i && scp -r fisco@$i:~/fisco/setup/nodes/$i/sdk* sdk_key/$i
done

echo "============= Distributee sdk_key ============="
for i in ${hosts[@]}; do
	scp -r sdk_key fisco@$i:~/fisco/wallet/src/python-sdk/bin/
done
scp -r sdk_key fisco@10.21.4.32:~/vue/backend/python-sdk/bin/
# scp -r sdk_key fisco@10.21.4.37:~/vue/backend/python-sdk/bin/

# echo "============= (Re)Create python environment ============="
# for i in ${hosts[@]}; do
# 	ssh fisco@$i "conda remove -y --name fisco --all && conda create -y --name fisco python=3.7 && conda activate fisco && pip install -r ~/fisco/wallet/src/requirements.txt && pip uninstall -y eth-utils eth-account eth-rlp"
# done

# echo "============= Test peak speed ============="
# for i in ${hosts[@]}; do
# 	ssh fisco@$i "conda activate fisco && cd ~/fisco/wallet/src/fisco-client && bash test_peak.sh"
# done