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
	# print(ip, port)
	cli = Client(ip, port)
	
	cli.deployNoArgContract(group_id, "testToken")
	cli.deployNoArgContract(group_id, "testSpeed")

	with open("test_eth.json", "r") as f:
		info = json.load(f)
	
	block_start = cli.getBlockNumber(group_id) + 1
	tx_cnt_start = int(cli.getTotalTransactionCount(group_id)['txSum'], 16)
	print_color("host {} group {} start block: {} start tx count: {}".format(ip, group_id, block_start, tx_cnt_start))
	info[group_id-1]["block_start"] = block_start
	info[group_id-1]["tx_cnt_start"] = tx_cnt_start

	with open("test_eth.json", "w") as f:
		json.dump(info, f)

if __name__ == "__main__":
	main(sys.argv[1:])