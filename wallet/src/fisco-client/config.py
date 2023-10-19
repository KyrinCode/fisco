import os
import yaml
import json

from _utils import create_dir

this_file = os.path.abspath(__file__)
contracts_dir = os.path.dirname(os.path.dirname(this_file)) + "/contracts"
sdk_dir = os.path.dirname(os.path.dirname(this_file)) + "/python-sdk"
keystore_dir = sdk_dir + "/bin/accounts"
config_dir = os.path.expanduser('~') + '/.fisco-wallet'
message_dir = config_dir + "/twoWayExchange"
custom_dir = config_dir + "/oneWayTransfer"

class Config:
	"""
	对客户端配置的抽象封装
	"""
	def __init__(self):
		
		self.config_dir = config_dir
		# self.config_dir = os.path.dirname(config_file)
		self.config_file = '/config.yaml'
		self.config_path = self.config_dir + self.config_file

		self.initial_config = {
			'group_num' : 2,
			'contracts_info' : {}
		}

		# Variables from configuration file. They will be initialized after load
		self.group_num = 0

		"""
		The format of contracts_info:
		{
			'crc20' : {
				'geth_1' : '0xd24ea07c7c9742b95f53836d531510748d65e6c0'
				'geth_2' : '0xd24ea07c7c9742b95f53836d531510748d65e6c0'
			}

		}
		"""
		self.contracts_info = {}

	def isConfig(self):
		"""Check if exists configuration on default path"""
		if os.path.isfile(self.config_path):
			return True
		else:
			return False

	def createEmptyConfig(self):
		create_dir(self.config_dir)
		with open(self.config_path, 'w+') as f:
			yaml.dump(self.initial_config, f)

	def loadConfig(self):
		"""Load configuration from .yaml file"""
		if not self.isConfig():
			self.createEmptyConfig()
			self.loadConfig()
		else:
			with open(self.config_path, 'r') as yaml_file:
				file = yaml.safe_load(yaml_file)
			for key, value in file.items():
				setattr(self, key, value)
		return self

	# future work
	def dumpConfig(self):
		config = dict(
			group_num = self.group_num,
			contracts_info = self.contracts_info
		)
		with open(self.config_path, 'w+') as f:
			yaml.dump(config, f)

	# future work
	def addURL(self, chain_name, network_id, chain_id, url):
		if chain_name in self.chains_info:
			self.chains_info[chain_name]['service'].append(url)
		else:
			self.chains_info[chain_name] = dict(
				network_id = network_id,
				chain_id = chain_id,
				service = [url]
			)

		self.dumpConfig()
		print("Add URL successful!")

	# future work
	def deleteURL(self, chain_name, url):
		if chain_name in self.chains_info:
			for i in range(0, len(self.chains_info[chain_name]['service'])):
				if self.chains_info[chain_name]['service'][i] == url:
					del(self.chains_info[chain_name]['service'][i])
					self.dumpConfig()
					print("Delete URL successful!")
					break
				print("The url doesn't exist!")
		else:
			print("This chain doesn't exist!")

	def updateContractInfo(self, contract_name, group_id, contract_addr):
		if contract_name in self.contracts_info:
			self.contracts_info[contract_name][group_id] = contract_addr
		else:
			self.contracts_info[contract_name] = {group_id : contract_addr}
		self.dumpConfig()
		print("Contract updated!")

	def deleteContractInfo(self, contract_name, group_id):
		if contract_name in self.contracts_info:
			if group_id in self.contracts_info[contract_name]:
				del(self.contracts_info[contract_name][group_id])
				self.dumpConfig()
				print("Contract Deleted!")
			else:
				print("The record doesn't exist!")
		else:
			print("The record doesn't exist!")

	# future work
	def showConfig(self):
		self.loadConfig()
		config = dict(
			group_num = self.group_num,
			contracts_info = self.contracts_info
		)
		return json.dumps(config, indent=4)