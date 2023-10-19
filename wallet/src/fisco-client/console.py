import sys, getopt, pprint

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from fisco_client import *
from _utils import pic, _h, print_error

CmdCompleter = WordCompleter(
	[
		'showConfig',
		'getAccount',
		'switchAccount',
		'multi-deploy',
		'deploy',
		'add',
		'multi-delete',
		'delete',
		'call',
		'send',
		'getClientVersion',
		'getBlockNumber',
		'getPbftView',
		'getSealerList',
		'getObserverList',
		'getConsensusStatus',
		'getSyncStatus',
		'getPeers',
		'getGroupPeers',
		'getNodeIDList',
		'getGroupList',
		'getBlockByHash',
		'getBlockByNumber',
		'getBlockHashByNumber',
		'getTransactionByHash',
		'getTransactionReceipt',
		'getPendingTransactions',
		'getPendingTxSize',
		'getPendingInfo',
		'getGaspriceInfo',
		'getCode',
		'getTotalTransactionCount',
		'getBlockLimit',
		'getBalanceInfo',
		'getBalance',
		'transfer',
		'approve',
		'multi-approve',
		'allowed',
		'getAllowedInfo',
		'txPool',
		'txPools',
		'oneWayTransfer deposit',
		'oneWayTransfer withdraw',
		'oneWayTransfer refund',
		'createCus',
		'viewTransfer',
		'twoWayExchange deposit',
		'twoWayExchange withdraw',
		'twoWayExchange refund',
		'createMsg',
		'viewExchange',
		'checkTxs',
		'createConfirmMsg',
		'firstConfirmMsgSign',
		'secondConfirmMsgSign',
		'depositApprove'
	],
	ignore_case = True,
	sentence = True
)

def parce_argv(argv):
	ip = "127.0.0.1"
	port = 8545
	try:
		opts, args = getopt.getopt(argv, "hi:p:", ["help", "ip=", "port="])
	except getopt.GetoptError:
		print("console.py -h")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print(_h)
			sys.exit()
		if opt in ("-i", "--ip"):
			ip = arg
		if opt in ("-p", "--port"):
			port = int(arg)
	return ip, port

def main(argv):
	ip = "127.0.0.1"
	port = 8545
	if argv:
		ip, port = parce_argv(argv)
	print(pic)
	cli = Client(ip, port)

	while 1:
		# command = input("\n>>> ")
		user_input = prompt(
			'>>> ',
			history = FileHistory('history.txt'),
			auto_suggest = AutoSuggestFromHistory(),
			completer = CmdCompleter,
		)

		cmd = user_input.split()
		if user_input in ("q", "exit"):
			break
		
		elif cmd[0] == "showConfig":
			cli.showConfig()
		
		elif cmd[0] == "getAccount":
			print("0x" + cli.getAccount())

		elif cmd[0] == "switchAccount":
			if len(cmd) == 2:
				cli.switchAccount(cmd[1])
			elif len(cmd) == 1:
				cli.switchAccount()
			else: print("Wrong parameter number!")
		
		elif cmd[0] == "getClientVersion":
			if len(cmd) == 2:
				print(cli.getClientVersion(int(cmd[1])))
			else: print("Wrong parameter number!")

		elif cmd[0] == "getBlockNumber":
			if len(cmd) == 2:
				print(cli.getBlockNumber(int(cmd[1])))
			else: print_error("Wrong parameter number!")
		
		elif cmd[0] == "getPbftView":
			if len(cmd) == 2:
				print(cli.getPbftView(int(cmd[1])))
			else: print_error("Wrong parameter number!")
				
		elif cmd[0] == "getSealerList":
			if len(cmd) == 2:
				print(cli.getSealerList(int(cmd[1])))
			else: print_error("Wrong parameter number!")	

		elif cmd[0] == "getObserverList":
			if len(cmd) == 2:
				print(cli.getObserverList(int(cmd[1])))
			else: print_error("Wrong parameter number!")
				
		elif cmd[0] == "getConsensusStatus":
			if len(cmd) == 2:
				print(cli.getConsensusStatus(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getSyncStatus":
			if len(cmd) == 2:
				print(cli.getSyncStatus(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getPeers":
			if len(cmd) == 2:
				print(cli.getPeers(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getGroupPeers":
			if len(cmd) == 2:
				print(cli.getGroupPeers(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getNodeIDList":
			if len(cmd) == 2:
				print(cli.getNodeIDList(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getGroupList":
			if len(cmd) == 2:
				print(cli.getGroupList(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getBlockByHash":
			if len(cmd) == 3:
				pprint.pprint(cli.getBlockByHash(int(cmd[1]), cmd[2]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getBlockByNumber":
			if len(cmd) == 3:
				pprint.pprint(cli.getBlockByNumber(int(cmd[1]), int(cmd[2])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getBlockHashByNumber":
			if len(cmd) == 3:
				print(cli.getBlockHashByNumber(int(cmd[1]), int(cmd[2])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getTransactionByHash":
			if len(cmd) == 3:
				print(cli.getTransactionByHash(int(cmd[1]), cmd[2]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getTransactionReceipt":
			if len(cmd) == 3:
				print(cli.getTransactionReceipt(int(cmd[1]), cmd[2]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getPendingTransactions":
			if len(cmd) == 2:
				print(cli.getPendingTransactions(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getPendingTxSize":
			if len(cmd) == 2:
				print(cli.getPendingTxSize(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getPendingInfo":
			if len(cmd) == 1:
				print(cli.getPendingInfo())
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getGaspriceInfo":
			if len(cmd) == 1:
				print(cli.getGaspriceInfo())
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getCode":
			if len(cmd) == 3:
				print(cli.getCode(int(cmd[1]), cmd[2]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getTotalTransactionCount":
			if len(cmd) == 2:
				print(cli.getTotalTransactionCount(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getBlockLimit":
			if len(cmd) == 2:
				print(cli.getBlockLimit(int(cmd[1])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "multi-deploy":
			if len(cmd) == 2:
				cli.deployNoArgContracts(cmd[1])
			else: print_error("Wrong parameter number!")
		
		elif cmd[0] == "deploy":
			if len(cmd) == 3:
				cli.deployNoArgContract(int(cmd[1]), cmd[2])
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "add":
			if len(cmd) == 4:
				cli.addContractAddress(int(cmd[1]), cmd[2], cmd[3])
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "multi-delete":
			if len(cmd) == 2:
				cli.deleteContractAddresses(cmd[1])
			else: print_error("Wrong parameter number!")
		
		elif cmd[0] == "delete":
			if len(cmd) == 3:
				cli.deleteContractAddress(int(cmd[1]), cmd[2])
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "call":
			if len(cmd) >= 4:
				args = cmd[4:]
				print(cli.call(int(cmd[1]), cmd[2], cmd[3], args))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "send":
			if len(cmd) >= 4:
				args = cmd[4:]
				print(cli.sendRawTransactionGetReceipt(int(cmd[1]), cmd[2], cmd[3], args))
			else: print_error("Wrong parameter number!")
				
		elif cmd[0] == "getBalanceInfo":
			if len(cmd) == 2:
				amount, balanceInfo = cli.getBalanceInfo(cmd[1])
				print("Amount: %s BalanceInfo: %s" % (amount, balanceInfo))
			elif len(cmd) == 3:
				amount, balanceInfo = cli.getBalanceInfo(cmd[1], cmd[2])
				print("Amount: %s BalanceInfo: %s" % (amount, balanceInfo))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getBalance":				
			if len(cmd) == 3:
				print(cli.getBalance(int(cmd[1]), cmd[2]))
			elif len(cmd) == 4:
				print(cli.getBalance(int(cmd[1]), cmd[2], cmd[3]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "transfer":
			if len(cmd) == 5:
				print(cli.transfer(int(cmd[1]), cmd[2], cmd[3], int(cmd[4])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "approve":
			if len(cmd) == 5:
				print(cli.approve(int(cmd[1]), cmd[2], cmd[3], int(cmd[4])))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "multi-approve":
			if len(cmd) == 3:
				if cli.approveAll(cmd[1], cmd[2]):
					print("Success!")
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "allowed":
			if len(cmd) == 4:
				print(cli.allowed(int(cmd[1]), cmd[2], cmd[3]))
			elif len(cmd) == 5:
				print(cli.allowed(int(cmd[1]), cmd[2], cmd[3], cmd[4]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "getAllowedInfo":
			if len(cmd) == 3:
				print(cli.getAllowedInfo(cmd[1], cmd[2]))
			elif len(cmd) == 4:
				print(cli.getAllowedInfo(cmd[1], cmd[2], cmd[3]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "txPool":
			if len(cmd) == 5:
				print(cli.txPool(int(cmd[1]), cmd[2], cmd[3], cmd[4]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "txPools":
			if len(cmd) == 4:
				print(cli.txPools(cmd[1], cmd[2], cmd[3]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "oneWayTransfer":
			if cmd[1] == "deposit":
				if len(cmd) == 4:
					cli.oneWayTransferDeposit(int(cmd[2]), cmd[3])
				elif len(cmd) == 6:
					cli.oneWayTransferDeposit(int(cmd[2]), cmd[3], cmd[4], cmd[5])
				else: print_error("Wrong parameter number!")
			elif cmd[1] == "withdraw":
				if len(cmd) == 5:
					cli.oneWayTransferWithdraw(int(cmd[2]), cmd[3], cmd[4])
				else: print_error("Wrong parameter number!")
			elif cmd[1] == "refund":
				if len(cmd) == 4:
					cli.oneWayTransferRefund(int(cmd[2]), cmd[3])
				else: print_error("Wrong parameter number!")
			else:
				print_error("Wrong function!")

		elif cmd[0] == "createCus":
			if len(cmd) == 3:
				cli.createCus(cmd[1], cmd[2])
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "viewTransfer":
			if len(cmd) == 2:
				cli.viewTransfer(cmd[1])
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "twoWayExchange":
			if cmd[1] == "deposit":
				if len(cmd) == 3:
					cli.twoWayExchangeDeposit(cmd[2])
				else: print_error("Wrong parameter number!")
			elif cmd[1] == "withdraw":
				if len(cmd) == 5:
					cli.twoWayExchangeWithdraw(int(cmd[2]), cmd[3], cmd[4])
				elif len(cmd) == 8:
					cli.twoWayExchangeWithdraw(int(cmd[2]), cmd[3], cmd[4], cmd[5], cmd[6], cmd[7])
				else: print_error("Wrong parameter number!")
			elif cmd[1] == "refund":
				if len(cmd) == 4:
					cli.twoWayExchangeRefund(int(cmd[2]), cmd[3])
				else: print_error("Wrong parameter number!")
			else:
				print_error("Wrong function!")

		elif cmd[0] == "createMsg":
			if len(cmd) == 2:
				cli.createMsg(cmd[1])
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "viewExchange":
			if len(cmd) == 2:
				cli.viewExchange(cmd[1])
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "checkTxs":
			if len(cmd) == 4:
				print(cli.checkTxs(cmd[1], cmd[2], cmd[3]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "createConfirmMsg":
			if len(cmd) == 4:
				print(cli.createConfirmMsg(cmd[1], cmd[2], cmd[3]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "firstConfirmMsgSign":
			if len(cmd) == 2:
				print(cli.firstConfirmMsgSign(cmd[1]))
			elif len(cmd) == 3:
				print(cli.firstConfirmMsgSign(cmd[1], cmd[2]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "secondConfirmMsgSign":
			if len(cmd) == 2:
				print(cli.secondConfirmMsgSign(cmd[1]))
			elif len(cmd) == 4:
				print(cli.secondConfirmMsgSign(cmd[1], cmd[2], cmd[3]))
			else: print_error("Wrong parameter number!")

		elif cmd[0] == "depositApprove":
			if len(cmd) == 4:
				print(cli.depositApprove(int(cmd[1]), cmd[2], int(cmd[3])))
			else: print_error("Wrong parameter number!")

	for i in range(len(cli.FBclients)):
		cli.FBclients[i].finish()
		
if __name__ == "__main__":
	main(sys.argv[1:])
	