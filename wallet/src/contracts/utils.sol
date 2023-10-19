pragma solidity >=0.4.25;

import "./strings.sol";

contract utils {
    using strings for *;
    
	function getSecretHash(string memory secret) public pure returns(bytes32) {
		bytes32 secretHash = keccak256(abi.encodePacked(secret));
		return secretHash;
	}

	function getBlockNumber() public view returns(uint) {
		return block.number;
	}
	
	function testRequire(uint value) public pure returns(uint) {
	    require(value != 0, "Zero value!");
	}
	
	function bytes2string(bytes memory b) public pure returns(string) {
	    string memory s = string(b);
	    return s;
	}
	
	function string2bytes(string memory s) public pure returns(bytes) {
	    bytes memory b = bytes(s);
	    return b;
	}
	
// 	function testSign(string memory confirmMsg, bytes memory sig) public view returns(address) {
// 	   // bytes memory sig = bytes(sigStr);
// 	    bytes32 msgHash = hashEIP191(bytes(confirmMsg), byte(0x45));
// 	    address signer = recoverSigner(msgHash, sig);
// 	    return signer;
// 	}
	
	function testSign(string memory confirmMsg, string memory sigStr) public view returns(address) {
	    bytes memory sig = fromHex(sigStr);
	    bytes32 msgHash = hashEIP191(bytes(confirmMsg), byte(0x45));
	    address signer = recoverSigner(msgHash, sig);
	    return signer;
	}
	
	function testMsgNum(string memory confirmMsg) public pure returns(uint) {
	    strings.slice memory confirm = confirmMsg.toSlice();
		strings.slice memory plus = "+".toSlice();
		uint txHashCnt = confirm.count(plus) + 1;
		return txHashCnt;
	}
	
	// Convert an hexadecimal character to their value
    function fromHexChar(uint8 c) internal pure returns (uint8) {
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
    function fromHex(string memory s) public pure returns (bytes memory) { // s不可以有0x前缀 
        bytes memory ss = bytes(s);
        require(ss.length%2 == 0); // length must be even
        bytes memory r = new bytes(ss.length/2);
        for (uint i=0; i<ss.length/2; ++i) {
            r[i] = bytes1(fromHexChar(uint8(ss[2*i])) * 16 +
                        fromHexChar(uint8(ss[2*i+1])));
        }
        return r;
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
}