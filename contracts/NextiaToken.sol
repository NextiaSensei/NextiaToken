// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title NextiaToken (NXT)
 * @dev ERC20 con burn, pause y ventana de mint cerrable de forma irreversible.
 * Supply fijo verificable una vez finalizado el mint.
 */
contract NextiaToken is ERC20, ERC20Burnable, ERC20Pausable, Ownable {
    // ===== Metadata =====
    string public constant TOKEN_NAME = "NextiaToken";
    string public constant TOKEN_SYMBOL = "NXT";

    // ===== Estado de mint =====
    bool public mintingFinished;

    // ===== Eventos =====
    event MintingFinished();

    constructor(
        uint256 initialSupply,
        address initialOwner
    )
        ERC20(TOKEN_NAME, TOKEN_SYMBOL)
        Ownable(initialOwner)
    {
        _mint(initialOwner, initialSupply);
        mintingFinished = false;
    }

    // ===== Control =====
    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    // ===== Mint controlado =====
    function mint(address to, uint256 amount) external onlyOwner {
        require(!mintingFinished, "Minting is finished");
        _mint(to, amount);
    }

    /**
     * @dev Cierra el mint de forma irreversible.
     * Una vez ejecutado, el supply queda matemáticamente fijo.
     */
    function finishMinting() external onlyOwner {
        require(!mintingFinished, "Minting already finished");
        mintingFinished = true;
        emit MintingFinished();
    }

    // ===== Overrides =====
    function approve(
        address spender,
        uint256 amount
    ) public override whenNotPaused returns (bool) {
        return super.approve(spender, amount);
    }

    function _update(
        address from,
        address to,
        uint256 value
    )
        internal
        override(ERC20, ERC20Pausable)
    {
        unchecked {
            super._update(from, to, value);
        }
    }
}

