pragma solidity >=0.4.0 <0.7.0;

interface ERC20 {
	function transferFrom(address _from, address _to, uint256 _value) external returns(bool success);
	function transfer(address _to, uint256 _value) external returns(bool success);
}

/**
  * @title   多链单向转账
  * @author  wxdbt, Kyrin
  * @dev     v0.2
*/
contract oneWayTransfer {
	
	struct TxInfo {
		address to;
		uint value;
		uint expBlockNumber;
		address tokenAddr;
	}
	
	// 锁定时间为区块高度
	uint lockTime = 10;

	// 第一层key为from，第二层key为secretHash
	mapping(address => mapping(bytes32 => TxInfo)) public txPool;
	
	event Deposit(address from, address to, uint value, address tokenAddr);
	event Withdraw(address from, address to, uint value, address tokenAddr);
	event Refund(address from, address to, uint value, address tokenAddr);
	
	/**
	  * @notice  转账发起人将资金锁在合约中
	  * @param   tokenAddr   ERC20代币合约地址
	  * @param   to          转账接收人地址
	  * @param   value       转账金额
	  * @param   secretHash  哈希锁
	  * @return  资金锁定成功与否
	*/
	function deposit(address tokenAddr, address to, uint value, bytes32 secretHash) public returns(bool success) {
		require(txPool[msg.sender][secretHash].value == 0, "Transaction exists!");
		require(value != 0, "Zero value!");
		ERC20 token = ERC20(tokenAddr);
		require(token.transferFrom(msg.sender, address(this), value), "No token was approved!");
		txPool[msg.sender][secretHash] = TxInfo({
				to: to,
				value: value,
				expBlockNumber: block.number + lockTime,
				tokenAddr: tokenAddr
		});
		emit Deposit(msg.sender, to, value, tokenAddr);
		return true;
	}
	
	/**
	  * @notice  转账接收人在锁定时间之内将资金从合约中取出
	  * @param   from    转账发起人地址
	  * @param   secret  哈希锁明文
	  * @return  资金取出成功与否
	*/
	function withdraw(address from, string memory secret) public returns(bool success) {
		bytes32 secretHash = keccak256(abi.encodePacked(secret));
		TxInfo storage tx_tmp = txPool[from][secretHash];
		require(tx_tmp.value != 0, "Wrong secret!");
		require(tx_tmp.to == msg.sender, "No right to withdraw!");
		require(block.number <= tx_tmp.expBlockNumber, "LockTime passed, transaction end!");
		ERC20 token = ERC20(tx_tmp.tokenAddr);
		require(token.transfer(msg.sender, tx_tmp.value), "Transfer failed!");
		emit Withdraw(from, msg.sender, tx_tmp.value, tx_tmp.tokenAddr);
		delete txPool[from][secretHash];
		return true;
	}
	
	/**
	  * @notice  转账发起人在锁定时间之后将资金从合约中退回
	  * @param   secret  哈希锁明文
	  * @return  资金退回成功与否
	*/
	function refund(string secret) public returns(bool success) {
		bytes32 secretHash = keccak256(abi.encodePacked(secret));
		TxInfo storage tx_tmp = txPool[msg.sender][secretHash];
		require(tx_tmp.value != 0, "No fund locked!");
		require(block.number > tx_tmp.expBlockNumber, "Waiting lockTime!");
		ERC20 token = ERC20(tx_tmp.tokenAddr);
		require(token.transfer(msg.sender, tx_tmp.value), "Transfer failed!");
		emit Refund(msg.sender, tx_tmp.to, tx_tmp.value, tx_tmp.tokenAddr);
		delete txPool[msg.sender][secretHash];
		return true;
	}
}