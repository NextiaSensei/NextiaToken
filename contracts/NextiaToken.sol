// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NextiaToken is ERC20, ERC20Burnable, ERC20Pausable, Ownable {
    constructor(uint256 initialSupply, address initialOwner)
        ERC20("NextiaToken", "NXT")
        Ownable(initialOwner)
    {
        _mint(initialOwner, initialSupply);
    }

    // ✅ funciones públicas para pausar / despausar
    
    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }
    
    // ✅ permitir mintear tokens nuevos (solo el owner)
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
    
    function approve(address spender, uint256 amount) public override whenNotPaused returns (bool) {
    return super.approve(spender, amount);
}


    // ✅ sobrescribir _update para integrar la pausa en transferencias
    function _update(address from, address to, uint256 value)
        internal
        override(ERC20, ERC20Pausable)
    {
        super._update(from, to, value);
    }
}

