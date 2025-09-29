// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NextiaToken is ERC20, ERC20Burnable, ERC20Pausable, Ownable {
    // ===== Variables constantes e inmutables =====
    string public constant TOKEN_NAME = "NextiaToken";
    string public constant TOKEN_SYMBOL = "NXT";

    constructor(uint256 initialSupply, address initialOwner)
        ERC20(TOKEN_NAME, TOKEN_SYMBOL)
        Ownable(initialOwner)
    {
        _mint(initialOwner, initialSupply);
    }

    // ===== Funciones externas optimizadas =====
    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }
    
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    function approve(address spender, uint256 amount) public override whenNotPaused returns (bool) {
    return super.approve(spender, amount);
}

    // ===== Transferencias internas =====
    function _update(address from, address to, uint256 value)
        internal
        override(ERC20, ERC20Pausable)
    {
        // Usamos unchecked en restas donde ya validamos con require en ERC20
        unchecked {
            super._update(from, to, value);
        }
    }
}

