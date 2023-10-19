import sys, getopt

from fisco_client import *
from _utils import print_error

def parce_argv(argv):
	ip = "127.0.0.1"
	port = 8545
	group_id = 1
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
	group_id = 1
	
	if argv:
		ip, port, group_id = parce_argv(argv)

	cli = Client(ip, port, False)

	if cli.get_contract_address(group_id, "testToken") == "":
		print_error("No testToken contract deployed.")

	if cli.get_contract_address(group_id, "testSpeed") == "":
		print_error("No testSpeed contract deployed.")

	to_addr = "0x0000000000000000000000000000000000000000"
	value = 1
	cnt = 10000
	
	for i in range(cnt):
		try:
			tx_hash = cli.testPeak(group_id, to_addr, value)
			# tx_hash = cli.testPeakCompress(group_id, to_addr, value, 10)
		except Exception as e:
			print(e)
		# print("group {} cnt {} tx_hash: {}".format(group_id, i+1, tx_hash))

if __name__ == "__main__":
	main(sys.argv[1:])