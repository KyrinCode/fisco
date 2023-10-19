pragma solidity >=0.4.25;

interface ERC20 {
	function transferFrom(address _from, address _to, uint256 _value) external returns(bool);
	function transfer(address _to, uint256 _value) external returns(bool);
}

contract testSpeed {

	// event TestPeak(address from, address to, uint value, uint cnt, address tokenAddr);

	// function testPeak(address tokenAddr, address to, uint value, uint cnt) public returns(bool success) {
	// 	require(value != 0, "Zero value!");
	// 	ERC20 token = ERC20(tokenAddr);
	// 	for (uint i = 0; i < cnt; i++) {
	// 		require(token.transferFrom(msg.sender, to, value), "Balance not enough!");
	// 	}
	// 	emit TestPeak(msg.sender, to, value, cnt, tokenAddr);
	// 	return true;
	// }

	event TestPeak(address from, address to, uint value, address tokenAddr);
	event TestPeakCompress(address from, address to, uint value, address tokenAddr, uint cnt);
	event TestETH(address from, address to, uint value, address tokenAddr, uint logic_id);

	function testPeak(address tokenAddr, address to, uint value) public returns(bool success) {
		require(value != 0, "Zero value!");
		ERC20 token = ERC20(tokenAddr);
		require(token.transferFrom(msg.sender, to, value), "Balance not enough!");
		emit TestPeak(msg.sender, to, value, tokenAddr);
		return true;
	}

	function testPeakCompress(address tokenAddr, address to, uint value, uint cnt) public returns(bool success) {
		require(value != 0, "Zero value!");
		ERC20 token = ERC20(tokenAddr);
		for (uint i = 0; i < cnt; i++) {
			require(token.transferFrom(msg.sender, to, value), "Balance not enough!");
		}
		emit TestPeakCompress(msg.sender, to, value, tokenAddr, cnt);
		return true;
	}

	function testETH(address tokenAddr, address to, uint value, uint logic_id) public returns(bool success) {
		require(value != 0, "Zero value!");
		ERC20 token = ERC20(tokenAddr);
		require(token.transferFrom(msg.sender, to, value), "Balance not enough!");
		emit TestETH(msg.sender, to, value, tokenAddr, logic_id);
		return true;
	}
}
