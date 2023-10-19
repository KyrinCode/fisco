pragma solidity >=0.4.0 <0.7.0;

interface ERC20 {
	function transferFrom(address _from, address _to, uint256 _value) external returns(bool success);
}

contract testApprove {
	function depositApprove (address tokenAddr, uint value) public returns(bool success){
		ERC20 token = ERC20(tokenAddr);
		require(token.transferFrom(msg.sender, address(this), value), "No token was approved!");
		return true;
	}
}