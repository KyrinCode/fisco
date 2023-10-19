import os
import sys

from config import sdk_dir, contracts_dir
sys.path.append(sdk_dir)

from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client_config import client_config

# 从文件加载abi定义
def compileContracts():
	contract_files = os.listdir(contracts_dir)
	contract_files.sort()
	if contract_files != None:
		for contract_file in contract_files:
			compileContract(contract_file)

def compileContract(contract_file):
	if os.path.isfile(client_config.solc_path) or os.path.isfile(client_config.solcjs_path):
		Compiler.compile_file(os.path.join(contracts_dir, contract_file), contracts_dir)

if __name__ == '__main__':
	compileContract("TokenA.sol")
	compileContract("TokenB.sol")
	compileContract("testApprove.sol")
	compileContract("oneWayTransfer.sol")
	compileContract("twoWayExchange.sol")
	compileContract("testToken.sol")
	compileContract("testSpeed.sol")