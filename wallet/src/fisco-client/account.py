import json
import sys
import getpass
import secrets
import os
from ecdsa import SigningKey
from binascii import hexlify, unhexlify
from Cryptodome.Hash import keccak
from mnemonic import Mnemonic

from _utils import create_dir
from config import sdk_dir, keystore_dir
sys.path.append(sdk_dir)

from eth_utils import to_checksum_address
from eth_account.account import Account as EthAccount
from eth_account.messages import encode_defunct
from client_config import client_config

class Account:
	"""
	一个私钥对应着一个Account，
	对消息、交易签名
	"""
	def __init__(self, keystore=None):
		if keystore is None:
			self.encrypted = None
			self.address = None
		else:
			self.load(keystore)

	def load(self, keystore):
		"""
		加载私钥文件
		"""
		try:
			with open(keystore, 'r') as f:
				self.encrypted = json.load(f)
				self.address = self.encrypted['address']
		except:
			self.encrypted = None
			self.address = None
			print("Failed to initiate the account!")

	@staticmethod
	def create(restore_password=None, restore_sentence=None):
		"""
		静态方法: 用于创建一个新的私钥并返回对应的account
		@param restore_password 助记密码
		@param restore_sentence 助记词
		@Return: Account
		"""
		if restore_password is None: # 随机生成账户
			randbits_256 = secrets.randbits(256)
			randbits_hex = hex(randbits_256)
			private_key = randbits_hex[2:]
		else: # 根据助记词生成新的私钥
			mnemonic = Mnemonic("english")
			seed = mnemonic.to_seed(restore_sentence, restore_password)
			private_key = seed[32:]

		password = client_config.account_password

		# password = getpass.getpass("Password: ")
		# password_check = getpass.getpass("Repeat password: ")

		# while password != password_check:
		# 	print("Try again")
		# 	password = getpass.getpass("Password: ")
		# 	password_check = getpass.getpass("Repeat password: ")

		encrypted = EthAccount.encrypt(private_key, password)
		address = "0x" + encrypted['address']

		create_dir(keystore_dir)
		account_keyfile = address + ".keystore"
		keystore_path = os.path.join(keystore_dir, account_keyfile)
		with open(keystore_path, 'w+') as f:
			json.dump(encrypted, f)

		print("New account has been generated, the address is : ", str(address))
		print("The key has been saved to ", keystore_path)

		return Account(keystore_path)

	@staticmethod
	def restore(restore_password, restore_sentence):
		"""
		根据助记词及助记密码，恢复账户
		"""
		return Account.create(restore_password, restore_sentence)

	def signMessage(self, message, password):
		"""
		对信息进行签名
		"""
		message_hash = encode_defunct(text=message)
		private_key = EthAccount.decrypt(self.encrypted, password)
		signed = EthAccount.sign_message(message_hash, private_key)
		return signed

	# future work
	def signTransaction(self, transaction_dict, password):
		"""
		对交易进行签名，返回签名后的数据结构
		"""
		private_key = EthAccount.decrypt(self.encrypted, password)
		signed = EthAccount.sign_transaction(transaction_dict, private_key)
		return signed

	# future work
	def sendTransaction(self, w3, transaction_dict, password):
		"""
		利用该账户发送一笔交易
		@param transaction_dict:
		tx = {
			# Note that the address must be in checksum format or native bytes:
			'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
			'value': 1000000000,
			'gas': 2000000,
			'gasPrice': 234567897654321,
			'nonce': 0,
			'chainId': 1,
			'authority':''
		}
		@param password:

		@Return bytes: 该笔交易的哈希  
		"""
		signed = self.signTransaction(transaction_dict, password)
		raw_transaction = signed.rawTransaction
		return w3.eth.sendRawTransaction(raw_transaction)

	# future work
	def sendMoney(self, w3, chain_id, to_addr, value, password):
		"""
		利用该账户发送一笔交易给to_addr账户
		"""
		to_addr = Web3.toChecksumAddress(to_addr)
		sender_addr = Web3.toChecksumAddress(self.address)
		tx = dict(
			to=to_addr,
			nonce=w3.eth.getTransactionCount(sender_addr),
			gasPrice=w3.eth.gasPrice,
			gas=2000000,
			value=hex(int(value)),
			chainId=chain_id,
			authority=''
		)
		return self.sendTransaction(w3, tx, password)

if __name__ == "__main__":
	# a = Account.create()
	# print(a.signMessage("fool", "123"))
	# b = Account.create("123", "fool")
	# a = Account(keystore_dir + "/e1bf9d9e1d803041d9d4607af2efab79605a0cce")
	# print(a.signMessage("fool", "123"))
	a = Account("/Users/kyrin/Playground/Fisco_Bcos_Multichain/src/python-sdk/bin/accounts/pyaccount.keystore")
	print(a.address)