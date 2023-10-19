import sys, getopt

from fisco_client import *
from _utils import print_error

def parce_argv(argv):
	ip = "127.0.0.1"
	port = 8545
	group_id = 1
	round_id = 0
	cnt = 100
	start = 0
	
	try:
		opts, args = getopt.getopt(argv, "i:p:g:r:c:s:", ["ip=", "port=", "group=", "round=", "cnt=", "start="])
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
		if opt in ("-r", "--round"):
			round_id = int(arg)
		if opt in ("-c", "--cnt"):
			cnt = int(arg)
		if opt in ("-s", "--start"):
			start = int(arg)
	return ip, port, group_id, round_id, cnt, start

def main(argv):
	if argv:
		ip, port, group_id, round_id, cnt, start = parce_argv(argv)

	with open("./test_eth_data/group"+str(group_id)+"/logic_ids_round"+str(round_id)+".json", "r") as f:
		logic_ids = json.load(f)

	cli = Client(ip, port)

	if cli.get_contract_address(group_id, "testToken") == "":
		print_error("No testToken contract deployed.")

	if cli.get_contract_address(group_id, "testSpeed") == "":
		print_error("No testSpeed contract deployed.")

	to_addr = "0x0000000000000000000000000000000000000000"
	value = 1
	
	for i in range(cnt):
		try:
			tx_hash = cli.testETH(group_id, to_addr, value, logic_ids[start+i])
		except Exception as e:
			print(e)
		# print("group {} cnt {} tx_hash: {}".format(group_id, i+1, tx_hash))

if __name__ == "__main__":
	main(sys.argv[1:])