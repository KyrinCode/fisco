import sys, getopt

from fisco_client import *
from _utils import print_error, print_color

def parce_argv(argv):
	ip = "127.0.0.1"
	port = 8545
	try:
		opts, args = getopt.getopt(argv, "i:p:", ["ip=", "port="])
	except getopt.GetoptError:
		print_error("Something bad occurred.")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--ip"):
			ip = arg
		if opt in ("-p", "--port"):
			port = int(arg)
	return ip, port

def main(argv):
	ip = "127.0.0.1"
	port = 8545
	group_num = 2

	if argv:
		ip, port = parce_argv(argv)
	# print(ip, port)
	cli = Client(ip, port, False)
	
	cli.deployNoArgContracts("testToken")
	cli.deployNoArgContracts("testSpeed")

	with open("test_peak.json", "r") as f:
		info = json.load(f)
	
	print("\n")
	for group_id in range(1, group_num+1):
		block_start = cli.getBlockNumber(group_id) + 1
		tx_cnt_start = int(cli.getTotalTransactionCount(group_id)['txSum'], 16)
		print_color("group {} start block: {} start tx count: {}".format(group_id, block_start, tx_cnt_start))
		info[group_id-1]["block_start"] = block_start
		info[group_id-1]["tx_cnt_start"] = tx_cnt_start
	print("\n")
	
	with open("test_peak.json", "w") as f:
		json.dump(info, f)

if __name__ == "__main__":
	main(sys.argv[1:])