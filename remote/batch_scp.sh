#!/bin/bash

hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.38 10.21.4.39)
# hosts=(10.21.4.37)
for i in ${hosts[@]}; do
	# scp requirements.txt fisco@$i:~/fisco/wallet/src/
	# scp .bash_profile fisco@$i:~/
	# scp -r ../wallet fisco@$i:~/fisco/
	scp -r ../wallet/src/fisco-client fisco@$i:~/fisco/wallet/src/
	# scp -r ../wallet/src/contracts fisco@$i:~/fisco/wallet/src/
	# scp -r ../wallet/src/fisco-client/fisco_client.py fisco@$i:~/fisco/wallet/src/fisco-client/
	# scp -r ../wallet/src/python-sdk fisco@$i:~/fisco/wallet/src/
	# scp -r ../wallet/src/python-sdk/client_config.py fisco@$i:~/fisco/wallet/src/python-sdk/
	# scp -r ../setup/*.sh fisco@$i:~/fisco/setup/
	# mkdir -p sdk_key/$i && scp -r fisco@$i:~/fisco/setup/nodes/127.0.0.1/sdk* sdk_key/$i
done