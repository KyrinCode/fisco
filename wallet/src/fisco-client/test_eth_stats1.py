import sys, getopt

from fisco_client import *
from _utils import print_error, print_color

def parce_argv(argv):
	ip = "127.0.0.1"
	port = 8545
	try:
		opts, args = getopt.getopt(argv, "i:p:g:", ["ip=", "port=", "group="])
	except getopt.GetoptError:
		print_error("Something bad occurred.")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--ip"):
			ip = arg
		if opt in ("-p", "--port"):
			port = int(arg)
		if opt in ("-g", "--group"):
			group_id = int(arg)
	return ip, port, group_id

def main(argv):
	ip = "127.0.0.1"
	port = 8545
	# group_num = 2

	if argv:
		ip, port, group_id = parce_argv(argv)
	cli = Client(ip, port)

	with open("test_eth.json", "r") as f:
		info = json.load(f)

	block_end = cli.getBlockNumber(group_id)
	tx_cnt_end = int(cli.getTotalTransactionCount(group_id)['txSum'], 16)
	print_color("host {} group {} end block: {} end tx count: {}".format(ip, group_id, block_end, tx_cnt_end))
	info[group_id-1]["block_end"] = block_end
	info[group_id-1]["tx_cnt_end"] = tx_cnt_end
	
	timestamp_start = int(cli.getBlockByNumber(group_id, info[group_id-1]["block_start"])['timestamp'], 16)
	timestamp_end = int(cli.getBlockByNumber(group_id, block_end)['timestamp'], 16)
	info[group_id-1]["timestamp_start"] = timestamp_start
	info[group_id-1]["timestamp_end"] = timestamp_end
	
	elapse_time = (timestamp_end - timestamp_start) / 1000.0
	print_color("host {} group {} elapse time: {} s".format(ip, group_id, elapse_time))

	tx_cnt = tx_cnt_end - info[group_id-1]["tx_cnt_start"]
	tps = tx_cnt / elapse_time
	print_color("host {} group {}: {} s, {} txs, {} tps".format(ip, group_id, elapse_time, tx_cnt, tps))

	with open("test_eth.json", "w") as f:
		json.dump(info, f)

if __name__ == "__main__":
	main(sys.argv[1:])