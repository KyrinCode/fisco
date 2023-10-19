import os
import sys
import traceback
import yaml
import json
from binascii import hexlify

from account import Account
from _utils import is_path, create_dir, print_color, print_error
from message import Msg, Tx, Cus
from config import Config, sdk_dir, contracts_dir, keystore_dir, message_dir, custom_dir

from client.bcosclient import BcosClient
from eth_utils import to_checksum_address, keccak
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client.bcoserror import BcosException, BcosError
from client_config import client_config

class Client:
	"""
	客户端的封装，类似geth的console
	"""
	def __init__(self, ip="127.0.0.1", port=8545, console=True): # port为多链客户端连接的节点起始port，如1个group10个节点，则rpc连接了8545和8545+10，channel连接了20200和20200+10
		if console:
			print("Loading config...", end=" ")
		self.config = Config().loadConfig()
		if console:
			print("√√√")
		create_dir(keystore_dir)
		keystore_path = os.path.join(keystore_dir, client_config.account_keyfile)
		if is_path(keystore_path):
			self.account = Account(keystore_path)
		else: self.account = Account().create()
		if console:
			print("Current account: 0x" + self.account.address)
		self.FBclients = []
		for i in range(1, self.config.group_num+1):
			port_real = port+(i-1)*4 # 4取决于一个group设置了几个节点
			if console:
				print("connecting to " + ip + ":" + str(port_real) + " group " + str(i))
			self.FBclients.append(BcosClient(i, ip, port_real, client_config.account_keyfile)) # 每个机构出10个节点维护一个群组
		if console:
			print("Client started.")

	def showConfig(self):
		"""
		显示客户端的配置信息
		"""
		# Version
		print_color("Version:")
		print("v1.0.0 by Kyrin 2021.03")
		# Clients
		print_color("Clients:")
		for i in range(self.config.group_num):
			print(self.FBclients[i].getinfo().replace(",", ", ").replace(" :", ": "))
		# Multichain
		print_color("Multichain:")
		print(self.config.showConfig())

	def getAccount(self):
		"""
		显示当前账户地址
		"""
		return self.account.address

	def switchAccount(self, address=""):
		account_keyfile = address + ".keystore"
		keystore_path = os.path.join(keystore_dir, account_keyfile)
		if is_path(keystore_path):
			self.account = Account(keystore_path)
		else: self.account = Account().create()
		for i in range(0, self.config.group_num):
			self.FBclients[i].load_default_account("0x"+self.account.address+".keystore")
		print_color("0x" + self.account.address + " switched")

	def check_group(self, group_id):
		if group_id > self.config.group_num:
			print_error("Group number exceeded!")
			return False
		return True

	def getClientVersion(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getNodeVersion()
		return res

	def getBlockNumber(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getBlockNumber()
		return res

	def getPbftView(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getPbftView()
		return res

	def getSealerList(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getSealerList()
		return res

	def getObserverList(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getObserverList()
		return res

	def getConsensusStatus(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getConsensusStatus()
		return res

	def getSyncStatus(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getSyncStatus()
		return res

	def getPeers(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getPeers()
		return res

	def getGroupPeers(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getGroupPeers()
		return res

	def getNodeIDList(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getNodeIDList()
		return res

	def getGroupList(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getGroupList()
		return res

	def getBlockByHash(self, group_id, block_hash):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getBlockByHash(block_hash)
		return res

	def getBlockByNumber(self, group_id, num):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getBlockByNumber(num)
		return res

	def getBlockHashByNumber(self, group_id, num):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getBlockHashByNumber(num)
		return res

	def getTransactionByHash(self, group_id, hash):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getTransactionByHash(hash)
		return res

	def getTransactionReceipt(self, group_id, hash):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getTransactionReceipt(hash)
		return res

	def getPendingTransactions(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getPendingTransactions()
		return res

	def getPendingTxSize(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getPendingTxSize()
		return res

	def getPendingInfo(self):
		pending_info = {}
		for group_id in range(1, self.config.group_num+1):
			pending = self.getPendingTxSize(group_id)
			pending_info["group"+str(group_id)] = pending
		return pending_info

	def getGaspriceInfo(self):
		gasprice_info = {}
		for group_id in range(1, self.config.group_num+1):
			gasprice = 0
			gasprice_info["group"+str(group_id)] = gasprice
		return gasprice_info

	def getCode(self, group_id, address):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getCode(address)
		return res

	def getTotalTransactionCount(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getTotalTransactionCount()
		return res

	def getBlockLimit(self, group_id):
		if not self.check_group(group_id): return
		res = self.FBclients[group_id-1].getBlockLimit()
		return res

	def get_contract_address(self, group_id, contract_name):
		"""
		返回对应群组下合约地址
		"""
		if not self.check_group(group_id): return
		return self.config.contracts_info[contract_name][group_id]

	def get_abi(self, contract_name):
		"""
		返回合约abi文件
		"""
		abi_file = os.path.join(contracts_dir, contract_name + ".abi")
		data_parser = DatatypeParser()
		data_parser.load_abi_file(abi_file)
		contract_abi = data_parser.contract_abi
		return contract_abi

	def get_bin(self, contract_name):
		"""
		返回合约bin文件
		"""
		bin_file = os.path.join(contracts_dir, contract_name + ".bin")
		with open(bin_file, 'r') as f:
			contract_bin = f.read()
		return contract_bin

	def deployNoArgContracts(self, contract_name):
		"""
		在多群组部署合约
		"""
		for group_id in range(1, self.config.group_num+1):
			self.deployNoArgContract(group_id, contract_name)

	def deployNoArgContract(self, group_id, contract_name):
		"""
		在对应群组部署合约
		"""
		if not self.check_group(group_id): return

		contract_bin = self.get_bin(contract_name)
		result = self.FBclients[group_id-1].deploy(contract_bin)
		print("\ngroup_id: ", group_id)
		print("blockHash: ", result["blockHash"])
		print("blockNumber: ", result["blockNumber"])
		print("from: ", result["from"])
		print("contractAddress: ", result["contractAddress"])
		print("transactionHash: ", result["transactionHash"])
		# 把部署结果存入文件备查
		self.addContractAddress(group_id, contract_name, result["contractAddress"])

	def addContractAddress(self, group_id, contract_name, contract_addr):
		"""
		在对应群组添加（覆盖）合约地址信息
		"""
		self.config.updateContractInfo(contract_name, group_id, contract_addr)


	def deleteContractAddresses(self, contract_name):
		"""
		在多群组删除合约地址信息
		"""
		for group_id in range(1, self.config.group_num+1):
			self.deleteContractAddress(group_id, contract_name)

	def deleteContractAddress(self, group_id, contract_name):
		"""
		在对应群组删除合约地址信息
		"""
		self.config.deleteContractInfo(contract_name, group_id)

	def call(self, group_id, contract_name, fn_name, args=None):
		"""
		在对应群组获取合约状态
		"""
		if not self.check_group(group_id): return

		contract_abi = self.get_abi(contract_name)
		contract_addr = self.get_contract_address(group_id, contract_name)
		res = self.FBclients[group_id-1].call(contract_addr, contract_abi, fn_name, args)
		return res

	def sendRawTransaction(self, group_id, contract_name, fn_name, args=None):
		"""
		在对应群组发送合约交易，不等回执
		"""
		if not self.check_group(group_id): return

		contract_abi = self.get_abi(contract_name)
		contract_addr = self.get_contract_address(group_id, contract_name)
		result = self.FBclients[group_id-1].sendRawTransaction(contract_addr, contract_abi, fn_name, args)
		# print("result: ", result)
		return result

	def sendRawTransactionGetReceipt(self, group_id, contract_name, fn_name, args=None):
		"""
		在对应群组发送合约交易
		"""
		if not self.check_group(group_id): return

		contract_abi = self.get_abi(contract_name)
		contract_addr = self.get_contract_address(group_id, contract_name)
		receipt = self.FBclients[group_id-1].sendRawTransactionGetReceipt(contract_addr, contract_abi, fn_name, args)
		# print("receipt: ", receipt)
		return receipt

	# 代币合约

	def getBalanceInfo(self, token_name, addr=None):
		if addr == None:
			addr = self.getAccount()
		balanceInfo = {}
		amount = 0
		for group_id in range(1, self.config.group_num+1):
			balance = self.getBalance(group_id, token_name, addr)
			balanceInfo["group"+str(group_id)] = balance
			amount += balance 
		return amount, balanceInfo

	def getBalance(self, group_id, token_name, addr=None):
		if addr == None:
			addr = self.getAccount()
		addr = to_checksum_address(addr)

		balance = self.call(group_id, token_name, "balanceOf", [addr])[0]
		return balance

	def transfer(self, group_id, token_name, to_addr, value):
		to_addr = to_checksum_address(to_addr)
		args = [to_addr, value]
		receipt = self.sendRawTransactionGetReceipt(group_id, token_name, "transfer", args)
		return receipt

	def approve(self, group_id, token_name, contract_name, value):
		contract_addr = self.get_contract_address(group_id, contract_name)
		contract_addr = to_checksum_address(contract_addr)

		args = [contract_addr, value]
		receipt = self.sendRawTransactionGetReceipt(group_id, token_name, "approve", args)
		return receipt

	def approveAll(self, token_name, contract_name):
		status = True
		for group_id in range(1, self.config.group_num+1):
			balance = self.getBalance(group_id, token_name)
			receipt = self.approve(group_id, token_name, contract_name, balance)
			if receipt['status'] != "0x0":
				status = False
				print_error("Failed in group " + str(group_id))
		return status

	def allowed(self, group_id, token_name, contract_name, addr=None):
		if addr == None:
			addr = self.getAccount()
		addr = to_checksum_address(addr)

		contract_addr = self.get_contract_address(group_id, contract_name)
		contract_addr = to_checksum_address(contract_addr)

		args = [addr, contract_addr]
		allowance = self.call(group_id, token_name, "allowed", args)[0]
		return allowance

	def getAllowedInfo(self, token_name, contract_name, addr=None):
		if addr == None:
			addr = self.getAccount()
		allowed_info = {}
		for group_id in range(1, self.config.group_num+1):
			allowed = self.allowed(group_id, token_name, contract_name, addr)
			balance = self.getBalance(group_id, token_name, addr)
			allowed_info["group"+str(group_id)] = min(allowed, balance)
		return allowed_info

	def txPool(self, group_id, contract_name, from_addr, secret):
		from_addr = to_checksum_address(from_addr)
		secret_hash = keccak(str(secret).encode()).hex()
		args = [from_addr, secret_hash]
		tx_info = self.call(group_id, contract_name, "txPool", args)
		return tx_info

	def txPools(self, contract_name, from_addr, secret):
		txpools_info = {}
		for group_id in range(1, self.config.group_num+1):
			tx_info = self.txPool(group_id, contract_name, from_addr, secret)
			if tx_info[1] != 0:
				txpools_info["group"+str(group_id)] = tx_info
		return txpools_info

	# 单向多链转账合约

	def oneWayTransferLowerDeposit(self, group_id, token_name, to_addr, value, secret):
		"""
		调用oneWayTransfer合约的deposit
		secret在本地转换为secret_hash
		"""
		token_addr = self.get_contract_address(group_id, token_name)
		token_addr = to_checksum_address(token_addr)
		to_addr = to_checksum_address(to_addr)
		secret_hash = keccak(str(secret).encode()).hex()
		
		args = [token_addr, to_addr, value, secret_hash]
		receipt = self.sendRawTransactionGetReceipt(group_id, "oneWayTransfer", "deposit", args)
		# print(receipt)
		if receipt['status'] == "0x0":
			status = True
		else: status = False
		tx_hash = receipt['transactionHash']
		return tx_hash, status
		# tx_response = self.getTransactionByHash(group_id, tx_hash)
		# data_parser = DatatypeParser()
		# input_result = data_parser.parse_transaction_input(tx_response['input'])
		# print("transaction input parse:", input_result)
		# return receipt, tx_response

	def oneWayTransferDeposit(self, value, secret, token_name=None, to_addr=None):
		"""
		若存在<secret>/cus.yaml 根据cus.yaml在各群组调用oneWayTransferLowerDeposit()
		若不存在 根据负载均衡生成转账方案 必须有token_name和to_addr参数
		获得tx_hash写进<secret>/addr.json
		"""
		if is_path(custom_dir+"/"+secret+"/cus.yaml"):
			cus = self.load_cus(secret)
			if cus.value != value:
				print_error("Value not matched!")
				return
			if not self.check_cus(secret): return
			token_name = cus.token_name
			to_addr = cus.to_addr
			txs = cus.transactions
		else:
			if token_name == None or to_addr == None:
				print_error("Missing parameters!")
				return
			allowed_info = self.getAllowedInfo(token_name, "oneWayTransfer")
			pending_info = self.getPendingInfo()
			gasprice_info = self.getGaspriceInfo()
			txs = self.logical2Actual(self.config.group_num, value, allowed_info, pending_info, gasprice_info)

		secret_addr = {}
		secret_addr['secret'] = secret
		secret_addr['token_name'] = token_name
		secret_addr['transactions'] = []
		for tx in txs:
			tx_hash, status = self.oneWayTransferLowerDeposit(tx.group_id, token_name, to_addr, tx.value, secret)
			if status == True:
				tmp = {}
				tmp['group_id'] = tx.group_id
				tmp['tx_hash'] = tx_hash
				tmp['value'] = tx.value
				secret_addr['transactions'].append(tmp)
			else: print_error("Tx status error in group " + str(tx.group_id))
		create_dir(custom_dir+"/"+secret)
		with open(custom_dir+"/"+secret+"/0x"+self.getAccount()+".json", "w") as json_file:
			json_file.write(json.dumps(secret_addr, indent=4))
		print("Finish!")

	def oneWayTransferWithdraw(self, group_id, from_addr, secret):
		"""
		调用oneWayTransfer合约的withdraw
		"""
		from_addr = to_checksum_address(from_addr)
		args = [from_addr, secret]
		receipt = self.sendRawTransactionGetReceipt(group_id, "oneWayTransfer", "withdraw", args)
		if receipt['status'] == "0x0":
			print("Success!")
		else: print_error("Failed!")

	def oneWayTransferRefund(self, group_id, secret):
		"""
		调用oneWayTransfer合约的refund
		"""		
		args = [secret]
		receipt = self.sendRawTransactionGetReceipt(group_id, "oneWayTransfer", "refund", args)
		if receipt['status'] == "0x0":
			print("Success!")
		else: print_error("Failed!")

	def createCus(self, to_addr, secret):
		"""
		创建<secret>/cus.yaml模板
		"""
		create_dir(custom_dir+"/"+secret)
		msg = dict(
			secret = secret,
			from_addr = "0x"+self.getAccount(),
			to_addr = to_addr,
			token_name = '<token_name>',
			value = '<value>',
			transactions = {
				'tx1': {
					'group_id': '<group_id>',
					'value': '<value>'
				},
				'tx2': {
					'group_id': '<group_id>',
					'value': '<value>'
				}
			}
		)
		with open(custom_dir+"/"+secret+"/cus.yaml", 'w') as yaml_file:
			yaml.dump(msg, yaml_file, sort_keys=False)
		print("Success!")

	def load_cus(self, secret):
		"""
		解析<secret>/cus.yaml
		"""
		cus = Cus()
		if not is_path(custom_dir+"/"+secret):
			return cus
		with open(custom_dir+"/"+secret+"/cus.yaml", 'r') as yaml_file:
			f = yaml.safe_load(yaml_file)
		
		setattr(cus, 'secret', f['secret'])
		setattr(cus, 'from_addr', f['from_addr'])
		setattr(cus, 'to_addr', f['to_addr'])
		setattr(cus, 'token_name', f['token_name'])
		setattr(cus, 'value', f['value'])
		for k, v in f['transactions'].items():
			tx = Tx()
			setattr(tx, 'group_id', v['group_id'])
			setattr(tx, 'value', v['value'])
			cus.transactions.append(tx)
		return cus

	def check_cus(self, secret):
		"""
		检查<secret>/cus.yaml
		1. secret是否匹配
		2. from_addr是否为该账户
		3. allowed余额是否充足
		4. value是否与交易value的和相等
		5. 还没有检查group_id是否有重复
		"""
		cus = self.load_cus(secret)
		if secret != cus.secret:
			print_error("Secret not matched!")
			return False
		from_addr = cus.from_addr
		if from_addr != "0x"+self.getAccount():
			print_error("False account!")
			return False
		token_name = cus.token_name
		value_sum = 0
		for tx in cus.transactions:
			value_sum += tx.value
			if not self.allowed(tx.group_id, token_name, "oneWayTransfer") >= tx.value:
				print_error("Allowed balance not sufficient!")
				return False
		if value_sum != cus.value:
			print_error("Value not matched!")
			return False
		return True

	def viewTransfer(self, secret):
		"""
		查看<secret>/cus.yaml
		"""
		cus = self.load_cus(secret)
		cus.show()

	def logical2Actual(self, group_num, value, balance_info, pending_info, gasprice_info):
		"""
		负载均衡 逻辑交易向实际交易映射
		"""
		txs = []

		balance_weight = 0.4286
		pending_weight = 0.4286
		gasprice_weight = 0.1429

		# 去掉账户余额为0的子网链
		for group_id in range(1, group_num+1):
			if balance_info["group"+str(group_id)] == 0:
				del(balance_info["group"+str(group_id)])
				del(pending_info["group"+str(group_id)])
				del(gasprice_info["group"+str(group_id)])

		# 将变量同质化
		# 将链上账户余额同质化
		homo_balance = {}
		max_balance = max(v for v in balance_info.values())
		min_balance = min(v for v in balance_info.values())
		for k, v in balance_info.items():
			if (max_balance - min_balance) != 0:
				homo_balance[k] = (v - min_balance) / (max_balance - min_balance)
			else:
				homo_balance[k] = 1

		# 将交易池中交易数同质化
		homo_pending = {}
		max_pending = max(v for v in pending_info.values())
		min_pending = min(v for v in pending_info.values())
		for k, v in pending_info.items():
			if (max_pending - min_pending) != 0:
				homo_pending[k] = (max_pending - v) / (max_pending - min_pending)
			else:
				homo_pending[k] = 1

		# 将交易费同质化
		homo_gasprice = {}
		max_gasprice = max(v for v in gasprice_info.values())
		min_gasprice = min(v for v in gasprice_info.values())
		for k, v in gasprice_info.items():
			if (max_gasprice - min_gasprice) != 0:
				homo_gasprice[k] = (max_gasprice - v) / (max_gasprice - min_gasprice)
			else:
				homo_gasprice[k] = 1

		group_priority = {}
		for k in homo_balance.keys():
			group_priority[k] = balance_weight * homo_balance[k] + pending_weight * homo_pending[k] + gasprice_weight * homo_gasprice[k]
		group_priority = sorted(group_priority.items(), key = lambda x : x[1], reverse=True)
		# 根据排序结果进行输出返回
		for i in range(len(group_priority)):
			group_id = group_priority[i][0]
			if value > 0:
				if (value - balance_info[group_id]) >= 0:
					balance_num = balance_info[group_id]
				else:
					balance_num = value
				value -= balance_num
				tx = Tx()
				setattr(tx, 'group_id', int(group_id[5:]))
				setattr(tx, 'value', balance_num)
				txs.append(tx)
			else:
				break
		for tx in txs:
			print(tx.show())
		return txs

	# 双向资产交换合约

	def twoWayExchangeLowerDeposit(self, group_id, token_name, to_addr, value, secret, tx_cnt):
		"""
		调用twoWayExchange合约的deposit
		secret在本地转换为secret_hash
		"""
		token_addr = self.get_contract_address(group_id, token_name)
		token_addr = to_checksum_address(token_addr)
		to_addr = to_checksum_address(to_addr)
		secret_hash = keccak(str(secret).encode()).hex()

		args = [token_addr, to_addr, value, secret_hash, tx_cnt]
		receipt = self.sendRawTransactionGetReceipt(group_id, "twoWayExchange", "deposit", args)
		print(receipt)
		if receipt['status'] == "0x0":
			status = True
		else: status = False
		tx_hash = receipt['transactionHash']
		return tx_hash, status

	def twoWayExchangeDeposit(self, secret):
		"""
		根据msg.yaml在各群组调用twoWayExchangeLowerDeposit()
		获得tx_hash写进<secret>/addr.json
		"""
		msg = self.load_msg(secret)
		# 检查allowed余额 future work
		tx_cnt = len(msg.A2B_transactions) + len(msg.B2A_transactions)
		secret_addr = {}
		secret_addr['secret'] = secret
		secret_addr['token_name'] = msg.token_name
		secret_addr['transactions'] = []
		if "0x"+self.getAccount() == msg.A_addr:
			txs = msg.A2B_transactions
			to_addr = msg.B_addr
		elif "0x"+self.getAccount() == msg.B_addr:
			txs = msg.B2A_transactions
			to_addr = msg.A_addr
		else:
			print_error("Wrong account!")
			return
		for tx in txs:
			tx_hash, status = self.twoWayExchangeLowerDeposit(tx.group_id, msg.token_name, to_addr, tx.value, secret, tx_cnt)
			if status == True:
				tmp = {}
				tmp['group_id'] = tx.group_id
				tmp['tx_hash'] = tx_hash
				tmp['value'] = tx.value
				secret_addr['transactions'].append(tmp)
			else: print_error("Tx status error in group " + str(tx.group_id))
		with open(message_dir+"/"+secret+"/0x"+self.getAccount()+".json", "w") as json_file:
			json_file.write(json.dumps(secret_addr, indent=4))
		print("Finish!")

	def twoWayExchangeWithdraw(self, group_id, from_addr, secret, confirm_msg=None, pre_sig=None, post_sig=None):
		"""
		调用twoWayExchange合约的withdraw
		"""
		if confirm_msg == None and pre_sig == None and post_sig == None and is_path(message_dir+"/"+secret+"/confirm_msg.json"):
			with open(message_dir+"/"+secret+"/confirm_msg.json", "r") as json_file:
				f = json.load(json_file)
			confirm_msg = f['confirm_msg']
			pre_sig = f['pre_sig']
			post_sig = f['post_sig']
		from_addr = to_checksum_address(from_addr)
		args = [from_addr, secret, confirm_msg, pre_sig, post_sig]
		receipt = self.sendRawTransactionGetReceipt(group_id, "twoWayExchange", "withdraw", args)
		if receipt['status'] == "0x0":
			print("Success!")
		else: print_error("Failed!")

	def twoWayExchangeRefund(self, group_id, secret):
		"""
		调用twoWayExchange合约的refund
		"""		
		args = [secret]
		receipt = self.sendRawTransactionGetReceipt(group_id, "twoWayExchange", "refund", args)
		if receipt['status'] == "0x0":
			print("Success!")
		else: print_error("Failed!")

	def createMsg(self, secret):
		"""
		创建<secret>/msg.yaml模板
		"""
		create_dir(message_dir+"/"+secret)
		msg = dict(
			secret = secret,
			A_addr = '<A_addr>',
			B_addr = '<B_addr>',
			token_name = '<token_name>',
			value = '<value>',
			A2B_transactions = {
				'tx1': {
					'group_id': '<group_id>',
					'value': '<value>'
				},
				'tx2': {
					'group_id': '<group_id>',
					'value': '<value>'
				}
			},
			B2A_transactions = {
				'tx1': {
					'group_id': '<group_id>',
					'value': '<value>'
				},
				'tx2': {
					'group_id': '<group_id>',
					'value': '<value>'
				}
			}
		)
		with open(message_dir+"/"+secret+"/msg.yaml", 'w') as yaml_file:
			yaml.dump(msg, yaml_file, sort_keys=False)
		print("Success!")

	def load_msg(self, secret):
		"""
		解析secret/msg.yaml
		"""
		msg = Msg()
		if not is_path(message_dir+"/"+secret):
			return msg
		with open(message_dir+"/"+secret+"/msg.yaml", 'r') as yaml_file:
			f = yaml.safe_load(yaml_file)
		
		setattr(msg, 'secret', f['secret'])
		setattr(msg, 'A_addr', f['A_addr'])
		setattr(msg, 'B_addr', f['B_addr'])
		setattr(msg, 'token_name', f['token_name'])
		setattr(msg, 'value', f['value'])
		for k, v in f['A2B_transactions'].items():
			tx = Tx()
			setattr(tx, 'group_id', v['group_id'])
			setattr(tx, 'value', v['value'])
			msg.A2B_transactions.append(tx)
		for k, v in f['B2A_transactions'].items():
			tx = Tx()
			setattr(tx, 'group_id', v['group_id'])
			setattr(tx, 'value', v['value'])
			msg.B2A_transactions.append(tx)
		return msg

	def viewExchange(self, secret):
		"""
		查看<secret>/msg.yaml
		"""
		msg = self.load_msg(secret)
		msg.show()

	def load_txs(self, secret, addr):
		"""
		读取<secret>/addr.json
		"""
		with open(message_dir+"/"+secret+"/"+addr+".json", "r") as json_file:
			f = json.load(json_file)
		return f
		
	def checkTxs(self, secret, from_addr, to_addr):
		"""
		判断<secret>/from_addr.json内容是否属实
		调用txPool检查
		1. to是否是to_addr
		2. 是否锁定了value
		3. 是否是对应的token
		"""
		f = self.load_txs(secret, from_addr)
		if secret != f['secret']:
			print_error("Wrong secret!")
			return False
		for i, v in enumerate(f['transactions'], 1):
			# 此处并未用到tx_hash
			# tx_response = self.getTransactionByHash(v['group_id'], v['tx_hash'])
			# data_parser = DatatypeParser()
			# print(tx_response['input'])
			# input_result = data_parser.parse_transaction_input(tx_response['input'])
			# print(input_result)
			# if input_result['value'] != v['value']:
			# 	return False
			tx_info = self.txPool(v['group_id'], "twoWayExchange", from_addr, secret)
			if tx_info[0] != to_addr or tx_info[1] != v['value'] or tx_info[5] != self.get_contract_address(v['group_id'], f['token_name']):
				print_error("Wrong info!")
				return False
		return True

	def createConfirmMsg(self, secret, addr1, addr2):
		"""
		生成唯一 confirmMsg（当加入多种代币时，可按照外层 group_id、内层 token_name 字典序排序）
		将<secret>/addr1.json和<secret>/addr2.json读出进行重组
		格式为<group_id+tx_hash+...>按照group_id排序
		返回confirmMsg
		"""
		print("Checking txs...", end=" ")
		if self.checkTxs(secret, addr1, addr2) and self.checkTxs(secret, addr2, addr1):
			print("√√√")
		else: print_error("\nWrong transactions!")

		f1 = self.load_txs(secret, addr1)
		f2 = self.load_txs(secret, addr2)
		tx_list = f1['transactions']
		tx_list += f2['transactions']
		tx_list.sort(key=lambda tx: tx['group_id'])

		s = ""
		for i in tx_list:
			s += str(i['group_id'])
			s += ":"
			s += i['tx_hash']
			s += "+"

		s = s[:-1]

		f = {}
		f['confirm_msg'] = s
		f['pre_sig'] = ""
		f['post_sig'] = ""
		with open(message_dir+"/"+secret+"/confirm_msg.json", "w") as json_file:
			json_file.write(json.dumps(f, indent=4))

		return s

	def firstConfirmMsgSign(self, secret, confirmMsg=None):
		"""
		先签名方签名
		"""
		with open(message_dir+"/"+secret+"/confirm_msg.json", "r") as json_file:
			f = json.load(json_file)
		if confirmMsg == None:
			confirmMsg = f['confirm_msg']
		# print(self.account.signMessage(confirmMsg, client_config.account_password)['signature'].hex()[2:])
		pre_sig = self.account.signMessage(confirmMsg, client_config.account_password)['signature'].hex()[2:] # 对confirmMsg的hash签名，去掉0x前缀
		if f['pre_sig'] == "":
			f['pre_sig'] = pre_sig
			with open(message_dir+"/"+secret+"/confirm_msg.json", "w") as json_file:
				json_file.write(json.dumps(f, indent=4))
			return pre_sig
		elif f['pre_sig'] != pre_sig:
			print_error("You may not be the first signer!")
		else: print_error("Signed before!")

	def secondConfirmMsgSign(self, secret, confirmMsg=None, preSigStr=None):
		"""
		后签名方签名
		"""
		with open(message_dir+"/"+secret+"/confirm_msg.json", "r") as json_file:
			f = json.load(json_file)
		if confirmMsg == None:
			confirmMsg = f['confirm_msg']
		if preSigStr == None:
			preSigStr = f['pre_sig']
		# print(self.account.signMessage(confirmMsg+preSigStr, client_config.account_password)['signature'].hex()[2:])
		post_sig = self.account.signMessage(confirmMsg+preSigStr, client_config.account_password)['signature'].hex()[2:] # 对confirmMsg连接preSigStr的hash签名，去掉0x前缀
		if f['pre_sig'] == "":
			return "Error: You may not be the second signer!"
		elif f['post_sig'] == "":
			f['post_sig'] = post_sig
			with open(message_dir+"/"+secret+"/confirm_msg.json", "w") as json_file:
				json_file.write(json.dumps(f, indent=4))
			return post_sig
		elif f['post_sig'] != post_sig:
			print_error("You may not be the second signer!")
		else: print_error("Signed before!")

	# 性能测试

	def testPeak(self, group_id, to_addr, value):
		contract_name = "testSpeed"
		token_name = "testToken"
		token_addr = to_checksum_address(self.get_contract_address(group_id, token_name))
		to_addr = to_checksum_address(to_addr)
		args = [token_addr, to_addr, value]
		tx_hash = self.sendRawTransaction(group_id, contract_name, "testPeak", args)
		return tx_hash

	def testPeakCompress(self, group_id, to_addr, value, cnt):
		contract_name = "testSpeed"
		token_name = "testToken"
		token_addr = to_checksum_address(self.get_contract_address(group_id, token_name))
		to_addr = to_checksum_address(to_addr)
		args = [token_addr, to_addr, value, cnt]
		tx_hash = self.sendRawTransaction(group_id, contract_name, "testPeakCompress", args)
		return tx_hash

	def testETH(self, group_id, to_addr, value, logic_id):
		print_color("Tx logic_id: {}".format(logic_id))
		contract_name = "testSpeed"
		token_name = "testToken"
		token_addr = to_checksum_address(self.get_contract_address(group_id, token_name))
		to_addr = to_checksum_address(to_addr)
		args = [token_addr, to_addr, value, logic_id]
		tx_hash = self.sendRawTransaction(group_id, contract_name, "testETH", args)
		return tx_hash
		
	# 代币授权测试

	def depositApprove(self, group_id, token_name, value):
		contract_name = "testApprove"
		token_addr = to_checksum_address(self.get_contract_address(group_id, token_name))
		args = [token_addr, value]
		receipt = self.sendRawTransactionGetReceipt(group_id, contract_name, "depositApprove", args)
		return receipt