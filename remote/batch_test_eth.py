import os, time, json

with open("./test_eth_data/block_info_lengths.json", "r") as f:
	info_lengths = json.load(f)

interval = 1
rounds = len(info_lengths["0"])

for r in range(100):
	print("round {}".format(r))
	txs = []
	for shard in range(16):
		txs.append(str(info_lengths[str(shard)][r]))
	# batch send txs to every chains each round with test_eth.sh
	# print(' '.join(txs))
	os.putenv("TX_CNT_ARRAY", ' '.join(txs))
	os.system('./batch_test_eth2.sh ' + str(r) + ' "$TX_CNT_ARRAY"')
	# time.sleep(interval)