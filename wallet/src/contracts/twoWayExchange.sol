pragma solidity >=0.4.25;

import "./strings.sol";

interface ERC20 {
	function transferFrom(address _from, address _to, uint256 _value) external returns(bool);
	function transfer(address _to, uint256 _value) external returns(bool);
}

/**
  * @title   资金的聚合与分散
  * @author  Haiki, Kyrin
  * @dev     v0.2
*/
contract twoWayExchange {
	using strings for *; // 为所有的类型都能使用这个库

	struct TxInfo {
		address to;
		uint value;
		uint secBlockNumber; // 安全时间，后签名方的取款截止点
		uint expBlockNumber; // 过期时间，先签名方的取款截止点，也是双方对自己锁定资金可以进行赎回的点，如果锁定都执行成功，取款阶段一方没有在取款截止点前及时完成取款，则原锁定方可以将资金赎回。
		uint txCnt; // 记录多链上实际交易的总个数(包括发送方和接收方的)，用来和confirmMsg中的hash个数做比较
		address tokenAddr;
	}

	// 安全时间过期时间的区块高度
	uint secTime = 20;
	uint expTime = 30;

	// 第一层key为from，第二层key为secretHash
	mapping(address => mapping(bytes32 => TxInfo)) public txPool;

	event Deposit(address from, address to, uint value, address tokenAddr);
	event Refund(address from, address to, uint value, address tokenAddr);
	event Withdraw(address from, address to, uint value, address tokenAddr);

	/**
	  * @notice  一方将资金锁在合约中
	  * @param   tokenAddr  ERC20代币合约地址
	  * @param   to         转账接收人地址
	  * @param   value      转账金额
	  * @param   secretHash 哈希锁
	  * @param   txCnt      多链上实际交易总数
	  * @return  资金锁定成功与否
	*/
	function deposit(address tokenAddr, address to, uint value, bytes32 secretHash, uint txCnt) public returns(bool success) {
		require(txPool[msg.sender][secretHash].value == 0, "Transaction exists!");
		require(value != 0, "Zero value!");
		ERC20 token = ERC20(tokenAddr);
		require(token.transferFrom(msg.sender, address(this), value), "No token was approved!");
		txPool[msg.sender][secretHash] = TxInfo({
			to: to,
			value: value,
			secBlockNumber: block.number + secTime,
			expBlockNumber: block.number + expTime,
			txCnt: txCnt,
			tokenAddr: tokenAddr
		});
		emit Deposit(msg.sender, to, value, tokenAddr);
		return true;
	}

	/**
	  * @notice  一方在过期时间之后将资金从合约中退回
	  * @param   secret 哈希锁原文
	  * @return  资金退回成功与否
	*/
	function refund(string memory secret) public returns(bool success) {
		bytes32 secretHash = keccak256(abi.encodePacked(secret));
		TxInfo storage tx_tmp = txPool[msg.sender][secretHash];
		require(tx_tmp.value != 0, "No fund locked!");
		require(block.number > tx_tmp.expBlockNumber, "Waiting expTime!");
		ERC20 token = ERC20(tx_tmp.tokenAddr);
		require(token.transfer(msg.sender, tx_tmp.value), "Transfer failed!");
		emit Refund(msg.sender, tx_tmp.to, tx_tmp.value, tx_tmp.tokenAddr);
		delete txPool[msg.sender][secretHash];
		return true;
	}

	/**
	  * @notice  判断转账接收人是先签名方还是后签名方，在对应的锁定时间内取款
	  * @param   from        转账发起人地址
	  * @param   secret      哈希锁明文
	  * @param   confirmMsg  确认消息，双方锁定交易hash的连接，格式："<chainId>:<txHash>+<chainId>:<txHash>+...+<chainId>:<txHash>"
	  * @param   preSigStr   先签名方对confirmMsg的签名
	  * @param   postSigStr  后签名方对confirmMsg+preSigStr的签名
	  * @return  资金赎回成功与否
	*/
	function withdraw(address from, string memory secret, string memory confirmMsg, string memory preSigStr, string memory postSigStr) public returns(bool success) {
		bytes32 secretHash = keccak256(abi.encodePacked(secret));
		TxInfo storage tx_tmp = txPool[from][secretHash];
		require(tx_tmp.value != 0, "Wrong secret!");
		require(tx_tmp.to == msg.sender, "No right to withdraw!");
		// 统计confirmMsg中包含交易数量
		strings.slice memory confirm = confirmMsg.toSlice();
		strings.slice memory plus = "+".toSlice();
		uint txHashCnt = confirm.count(plus) + 1;
		require(txHashCnt == tx_tmp.txCnt, "Wrong transaction count!");
		// 计算后签名方并检查两个签名的合法性
		bool isPostSigner = checkSigAndJudgeSigner(from, msg.sender, confirmMsg, preSigStr, postSigStr);
		// 根据签名的先后顺序，进行两阶段取款时间判断
		if(isPostSigner == true){
			require(block.number <= tx_tmp.secBlockNumber, "SecTime passed, transaction end!");
		} else {
			require(block.number <= tx_tmp.expBlockNumber, "ExpTime passed, transaction end!");
		}
		ERC20 token = ERC20(tx_tmp.tokenAddr);
		require(token.transfer(msg.sender, tx_tmp.value), "Transfer failed!");
		emit Withdraw(from, msg.sender, tx_tmp.value, tx_tmp.tokenAddr);
		delete txPool[from][secretHash];
		return true;
	}

	/**
	  * @notice  检查两层签名正确与否，判断转账接收人是否为后签名方
	  * @param   from        转账发起人地址
	  * @param   to          转账接收人地址
	  * @param   confirmMsg  确认消息，双方锁定交易hash的连接，格式："<chainId>:<txHash>+<chainId>:<txHash>+...+<chainId>:<txHash>"
	  * @param   preSigStr   先签名方对confirmMsg的签名
	  * @param   postSigStr  后签名方对confirmMsg+preSigStr的签名
	  * @return  转账接收人是否为后签名方，true则为后签名方，false则为先签名方
	*/
	function checkSigAndJudgeSigner(address from, address to, string memory confirmMsg, string memory preSigStr, string memory postSigStr) internal view returns(bool) {
		// 签名string->bytes格式转换
		bytes memory preSig = fromHex(preSigStr);
		bytes memory postSig = fromHex(postSigStr);
		// 从消息与签名恢复出先签名方
		bytes32 preMsgHash = hashEIP191(bytes(confirmMsg), byte(0x45));
		address preSigner = recoverSigner(preMsgHash, preSig);
		// confirmMsg + preSigStr
		string memory postSignMsg = confirmMsg.toSlice().concat(preSigStr.toSlice());
		// 从消息与签名恢复出后签名方
		bytes32 postMsgHash = hashEIP191(bytes(postSignMsg), byte(0x45));
		address postSigner = recoverSigner(postMsgHash, postSig);

		bool isPostSigner = false;
		// 检查两个签名分别与from、to是否匹配
		if(postSigner == to){ // 接收方后签的名
			isPostSigner = true;
			require(preSigner == from, "You are postSigner，but preSig not right!");
		} else if(postSigner == from){ // 发送方后签的名
			require(preSigner == to, "You are preSigner, but preSig not right!");
		} else {
			revert("Both Sigs are invalid!");
		}
		return isPostSigner;
	}

	/**
	  * @notice  对签名进行分离得到原始的(v,r,s)
	  * @param   sig 签名
	  * @return  对原交易散列进行签名后得到的(v,r,s)
	*/
	function splitSignature(bytes memory sig) internal pure returns(uint8 v, bytes32 r, bytes32 s) {
		require(sig.length == 65);
		assembly {
			// first 32 bytes, after the length prefix.
			r := mload(add(sig, 32))
			// second 32 bytes.
			s := mload(add(sig, 64))
			// final byte (first byte of the next 32 bytes).
			v := byte(0, mload(add(sig, 96)))
		}
		if (v < 27) {
			v += 27;
		}
		require(v == 27 || v == 28);
		return (v, r, s);
	}

	/**
	  * @notice  由交易原始信息和签名，恢复签名私钥对应的地址
	  * @param   msgHash 被签名信息，是prefix+原信息做散列后的值
	  * @param   sig 签名
	  * @return  address 签名私钥对应的地址
	*/
	function recoverSigner(bytes32 msgHash, bytes memory sig) internal pure returns(address) {
		(uint8 v, bytes32 r, bytes32 s) = splitSignature(sig);//sign<r,s,v>

		return ecrecover(msgHash, v, r, s);
	}

	function hashEIP191(bytes memory _message, byte _version) internal view returns(bytes32 result) {
		// Version 0: Data with intended validator
		if(_version == byte(0x00)){
			address validator = address(this);
			return keccak256(abi.encodePacked(byte(0x19), byte(0x00), validator, _message));
		} else if(_version == byte(0x45)) {  // Version E: personal_sign messages
			uint256 length = _message.length;
			require(
				length > 0,
				"Empty message not allowed for version E"
			);
			// Compute text-encoded length of message
			uint256 digits = 0;
			while(length != 0){
				digits++;
				length /= 10;
			}
			bytes memory lengthAsText = new bytes(digits);
			length = _message.length;
			uint256 index = digits - 1;
			while (length != 0) {
				lengthAsText[index--] = byte(uint8(48 + length % 10));
				length /= 10;
			}
			return keccak256(abi.encodePacked(byte(0x19), "Ethereum Signed Message:\n", lengthAsText, _message));
		} else {
			revert("Unsupported EIP191 version");
		}
	}

	// Convert an hexadecimal character to their value
    function fromHexChar(uint8 c) internal pure returns(uint8) {
        if (bytes1(c) >= bytes1('0') && bytes1(c) <= bytes1('9')) {
            return c - uint8(bytes1('0'));
        }
        if (bytes1(c) >= bytes1('a') && bytes1(c) <= bytes1('f')) {
            return 10 + c - uint8(bytes1('a'));
        }
        if (bytes1(c) >= bytes1('A') && bytes1(c) <= bytes1('F')) {
            return 10 + c - uint8(bytes1('A'));
        }
    }
    
    // Convert an hexadecimal string to raw bytes
    function fromHex(string memory s) internal pure returns(bytes memory) { // s不可以有0x前缀 
        bytes memory ss = bytes(s);
        require(ss.length%2 == 0); // length must be even
        bytes memory r = new bytes(ss.length/2);
        for (uint i=0; i<ss.length/2; i++) {
            r[i] = bytes1(fromHexChar(uint8(ss[2*i])) * 16 + fromHexChar(uint8(ss[2*i+1])));
        }
        return r;
    }
}
