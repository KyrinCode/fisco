#!/bin/bash

hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.38 10.21.4.39)
# hosts=(10.21.4.38)

echo "============= Batch start all nodes ============="
for i in ${hosts[@]}; do
	workspace="~/fisco/setup/nodes/$i"
	ssh fisco@$i "cd $workspace && bash start_all.sh"
done