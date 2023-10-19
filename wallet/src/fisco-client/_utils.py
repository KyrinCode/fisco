import os
import errno
import json

def is_path(path):
    """
    Check if path is directory
    """
    if os.path.exists(path):
        return True
    return False


def create_dir(dirname):
    """
    Create directory if doesn't aleady exists
    """
    if not is_path(dirname):
        try:
            os.makedirs(dirname)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

def print_color(s):
    print("\033[1;36m" + s + "\033[0m")

def print_error(s):
    print("\033[1;41m" + "Error: " + s + "\033[0m")

pic = \
"""
***************************************************************************************
  __  __       _ _   _      _           _          _____                      _      
 |  \/  |     | | | (_)    | |         (_)        / ____|                    | |     
 | \  / |_   _| | |_ _  ___| |__   __ _ _ _ __   | |     ___  _ __  ___  ___ | | ___ 
 | |\/| | | | | | __| |/ __| '_ \ / _` | | '_ \  | |    / _ \| '_ \/ __|/ _ \| |/ _ \ 
 | |  | | |_| | | |_| | (__| | | | (_| | | | | | | |___| (_) | | | \__ \ (_) | |  __/
 |_|  |_|\__,_|_|\__|_|\___|_| |_|\__,_|_|_| |_|  \_____\___/|_| |_|___/\___/|_|\___|
                                                                                     
************************Welcome to FISCOBCOS Multichain Wallet*************************
"""

_h = pic + \
"""
>>> showConfig
>>> q / exit

>>> getAccount
>>> switchAccount (<addr>)
>>> getClientVersion <group_id>
>>> getBlockNumber <group_id>
>>> getPbftView <group_id>
>>> getSealerList <group_id>
>>> getObserverList <group_id>
>>> getConsensusStatus <group_id>
>>> getSyncStatus <group_id>
>>> getPeers <group_id>
>>> getGroupPeers <group_id>
>>> getNodeIDList <group_id>
>>> getGroupList <group_id>
>>> getBlockByHash <group_id> <hash>
>>> getBlockByNumber <group_id> <num>
>>> getBlockHashByNumber <group_id> <num>
>>> getTransactionByHash <group_id> <hash>
>>> getTransactionReceipt <group_id> <hash>
>>> getPendingTransactions <group_id>
>>> getPendingTxSize <group_id>
>>> getPendingInfo
>>> getGaspriceInfo
>>> getCode <group_id> <addr>
>>> getTotalTransactionCount <group_id>
>>> getBlockLimit <group_id>

>>> multi-deploy <contract_name>
>>> deploy <group_id> <contract_name>
>>> add <group_id> <contract_name> <contract_addr>
>>> multi-delete <contract_name>
>>> delete <group_id> <contract_name>
>>> call <group_id> <contract_name> <fn_name> (<args>)
>>> send <group_id> <contract_name> <fn_name> (<args>)

>>> getBalanceInfo <token_name> (<addr>)
>>> getBalance <group_id> <contract_name> (<addr>)
>>> transfer <group_id> <token_name> <to_addr> <value>
>>> approve <group_id> <token_name> <contract_name> <value>
>>> multi-approve <token_name> <contract_name>
>>> allowed <group_id> <token_name> <contract_name> (<addr>)
>>> getAllowedInfo <token_name> <contract_name> (<addr>)
>>> txPool <group_id> <contract_name> <from_addr> <secret>
>>> txPools <contract_name> <from_addr> <secret>

>>> oneWayTransfer deposit <value> <secret> (<token_name>) (<to_addr>)
>>> oneWayTransfer withdraw <group_id> <from_addr> <secret>
>>> oneWayTransfer refund <group_id> <secret>
>>> createCus <to_addr> <secret>
>>> viewTransfer <secret>

>>> twoWayExchange deposit <secret>
>>> twoWayExchange withdraw <group_id> <from_addr> <secret> (<confirm_msg>) (<pre_sig>) (<post_sig>)
>>> twoWayExchange refund <group_id> <secret>
>>> createMsg <secret>
>>> viewExchange <secret>
>>> checkTxs <secret> <from_addr> <to_addr>
>>> createConfirmMsg <secret> <addr1> <addr2>
>>> firstConfirmMsgSign <secret> (<confirmMsg>)
>>> secondConfirmMsgSign <secret> (<confirmMsg>) (<preSigStr>)

***************************************************************************************
"""