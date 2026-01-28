# 🚀 Nextia Token (NXT)
# 🧠 NextiaToken — Developer Documentation (v0.6 Pre-Mainnet)

![Network](https://img.shields.io/badge/network-Sepolia-blue)
![Tests](https://img.shields.io/badge/tests-28%2F28-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Status](https://img.shields.io/badge/status-pre--mainnet-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📌 Overview

This repository contains the **core ERC-20 smart contract** for **NextiaToken (NXT)**,  
the utility token powering the **Nextia ecosystem**.

Current version **v0.6** represents a **Pre-Mainnet, production-ready** stage:
- Fully tested
- Gas-optimized
- Deployed on Sepolia
- Public and verifiable

> ⚠️ Important: An **external independent audit** is recommended before any mainnet deployment.

---

## ⚙️ 1. Requirements

- Node.js **18.x (recommended 18.16.x)**
- npm ≥ 9
- Git
- Hardhat
- MetaMask (Sepolia enabled)
- Alchemy account

---

## 🧩 2. Installation & Setup

```bash
git clone https://github.com/NextiaLabs/NextiaToken.git
cd NextiaToken
npm install

🚀 3. Core Commands
| Command                                               | Description         |
| ----------------------------------------------------- | ------------------- |
| `npx hardhat compile`                                 | Compile contracts   |
| `npx hardhat test`                                    | Run full test suite |
| `npx hardhat coverage`                                | Solidity coverage   |
| `REPORT_GAS=true npx hardhat test`                    | Gas report          |
| `npx hardhat run scripts/deploy.js --network sepolia` | Deploy              |
| `npx hardhat verify --network sepolia <address>`      | Verify              |

🧪 4. Project Structure

NextiaToken/
├── contracts/
│   └── NextiaToken.sol
├── test/
│   ├── security.test.js
│   ├── gas.test.js
│   └── core.test.js
├── scripts/
│   ├── deploy.js
│   └── verify.js
├── hardhat.config.js
├── README_developer.md
└── README_investors.md

🔐 5. Security Model

ERC-20 compliant

Ownable + Pausable

Controlled mint & burn

Events fully indexed

No proxy / no upgrade risk

Explicit revert conditions

Testing:

28/28 tests passing

100% line & branch coverage (local)

| Network          | Status               |
| ---------------- | -------------------- |
| Hardhat local    | Active               |
| Sepolia Testnet  | Deployed             |
| Ethereum Mainnet | Planned (post-audit) |

🤝 7. Contributing

1. Fork the repo

2.Create a feature branch

3. Ensure tests pass

4. Open a Pull Request

## 📞 Contact

**Nextia Labs**  
🌐 https://nextiamarketing.com y https://tokenlab.nextiamarketing.com
📧 jsensei@tokenlab.nextiamarketing.com 
💬 Telegram: @nextiatoken_presale_bot

🪙 License

MIT — free to use, fork and build.
