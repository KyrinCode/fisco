pragma solidity >=0.4.22;
 
import "./tokenERC20.sol"; 

contract TokenB is TokenERC20 {
    constructor() TokenERC20(100000000, "TokenB", "B") public {}
}