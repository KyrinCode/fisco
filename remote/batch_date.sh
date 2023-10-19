#!/bin/bash

hosts=(10.21.4.32 10.21.4.33 10.21.4.34 10.21.4.35 10.21.4.36 10.21.4.38 10.21.4.39)
for i in ${hosts[@]}; do
	ssh fisco@$i "date +"%Y-%m-%d-%H-%M-%S""
done

