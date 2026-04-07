# 🚀 Nextia Token (NXT)
# 🧠 NextiaToken — Developer Documentation (v0.6 Pre-Mainnet)

![Network](https://img.shields.io/badge/network-Sepolia-blue)
![Tests](https://img.shields.io/badge/tests-33%2F33-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Status](https://img.shields.io/badge/status-pre--mainnet-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📌 Overview

This repository contains the **core ERC-20 smart contract** for **NextiaToken (NXT)**,  
the utility token powering the **Nextia ecosystem**.

Current version **v0.6** represents a **Pre-Mainnet, production-ready** stage:
- Fully tested (33/33 across 4 suites)
- Gas-optimized
- Deployed on Sepolia
- Public and verifiable

> ⚠️ Important: An **external independent audit** is recommended before any mainnet deployment.

---

## 🔒 Audit Report — 33/33 Tests

The full Mochawesome v6.3.0 test report is published on the presale landing:

> 🌐 **[nextia-marketing.vercel.app/#audit](https://nextia-marketing.vercel.app/#audit)**

| Suite | File | Tests | Time |
|-------|------|-------|------|
| Advanced & Edge Cases | `NextiaToken.extra.test.js` | 9/9 ✅ | 119ms |
| Gas Tests ⛽ | `NextiaToken.gas.test.js` | 6/6 ✅ | 28ms |
| Security Tests 🔒 | `NextiaToken.security.test.js` | 13/13 ✅ | 102ms |
| Core Tests | `NextiaToken.test.js` | 5/5 ✅ | 29ms |
| **TOTAL** | 4 suites | **33/33** | **~278ms** |

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
git clone https://github.com/NextiaSensei/NextiaToken.git
cd NextiaToken
npm install
```

## 🚀 3. Core Commands

| Command | Description |
|---------|-------------|
| `npx hardhat compile` | Compile contracts |
| `npx hardhat test` | Run full test suite |
| `npx hardhat coverage` | Solidity coverage |
| `REPORT_GAS=true npx hardhat test` | Gas report |
| `npx hardhat run scripts/deploy.js --network sepolia` | Deploy |
| `npx hardhat verify --network sepolia <address>` | Verify |

## 🧪 4. Project Structure

```
NextiaToken/
├── contracts/
│   └── NextiaToken.sol
├── test/
│   ├── NextiaToken.extra.test.js
│   ├── NextiaToken.gas.test.js
│   ├── NextiaToken.security.test.js
│   └── NextiaToken.test.js
├── scripts/
│   ├── deploy.js
│   └── verify.js
├── hardhat.config.js
├── README_developer.md
└── README_INVESTORS.md
```

## 🔐 5. Security Model

- ERC-20 compliant
- Ownable + Pausable
- Controlled mint & burn
- Events fully indexed
- No proxy / no upgrade risk
- Explicit revert conditions

**Testing:**
- 33/33 tests passing
- 100% line & branch coverage (local)

| Network | Status |
|---------|--------|
| Hardhat local | Active |
| Sepolia Testnet | Deployed |
| Ethereum Mainnet | Planned (post-audit) |

## 🤝 6. Contributing

1. Fork the repo
2. Create a feature branch
3. Ensure tests pass
4. Open a Pull Request

## 📞 Contact

**Nextia Labs**  
🌐 https://nextiamarketing.com y https://tokenlab.nextiamarketing.com  
📧 jsensei@tokenlab.nextiamarketing.com  
💬 Telegram: @nextiatoken_presale_bot

## 🪙 License

MIT — free to use, fork and build.
