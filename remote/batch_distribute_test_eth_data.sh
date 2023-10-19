#!/bin/bash

hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.37 10.21.4.38 10.21.4.39)
# hosts=(10.21.4.32)
len=${#hosts[@]}
workspace="~/fisco/wallet/src/fisco-client"

echo "============= Distribute test_eth_data ============="
for ((i=0; i<len; i++)); do
	echo ${hosts[$i]}
	ssh fisco@${hosts[$i]} "cd $workspace && rm -rf test_eth_data && mkdir test_eth_data && cd test_eth_data && mkdir group1 group2"
	scp ~/Playground/fisco/remote/test_eth_data/shard$(($i*2+1))/* fisco@${hosts[$i]}:$workspace/test_eth_data/group1/
	scp ~/Playground/fisco/remote/test_eth_data/shard$(($i*2+2))/* fisco@${hosts[$i]}:$workspace/test_eth_data/group2/
done