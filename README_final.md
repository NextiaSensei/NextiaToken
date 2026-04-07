# 💎 NextiaToken — v0.6 Pre-Mainnet

**NextiaToken ($NXT)** es el activo digital central del ecosistema **Nextia**, un proyecto que fusiona tecnología, creatividad y valor real para construir una economía web3 autónoma.

> “No solo un token. Una llave para acceder al futuro.”  
> — *Nextia Labs, 2025*

---

## 🌍 1. Visión

NextiaToken busca conectar **innovación, comunidad y crecimiento** dentro del universo Nextia.  
Su propósito: **potenciar proyectos de marketing, desarrollo y comunidad descentralizada.**

---

## 🧭 2. Roadmap

| Fase | Objetivo | Estado |
|------|-----------|--------|
| **v0.1 – v0.4** | Contrato base, auditorías y pruebas internas | ✅ Completado |
| **v0.5** | Pre-Mainnet + documentación técnica + dashboard dev | ✅ Completado |
| **v0.6 (actual)** | 33/33 tests • Reporte de auditoría público • Presale activa | 🚀 Activa |
| **v0.7** | Staking & ecosistema integration | 🔮 Planeado |
| **v1.0** | Mainnet + DAO-lite | 🔮 Planeado |

---

## 🪙 3. Tokenomics

| Parámetro | Valor |
|------------|--------|
| **Símbolo** | NXT |
| **Red actual** | Ethereum (Sepolia Testnet) |
| **Suministro total** | 1,000,000 NXT |
| **Propiedad inicial** | Nextia Labs |
| **Política de emisión** | Controlado por `onlyOwner` |
| **Funciones clave** | Mint / Burn / Pause / Unpause |

---

## 🔐 4. Seguridad y transparencia

- **33/33 tests automatizados pasados** — 4 suites (Advanced, Gas, Security, Core)
- 100% cobertura de pruebas
- Contrato verificado públicamente en Sepolia
- Protección ante reentrancy
- Control de roles y pausas
- Eventos ERC-20 (`Transfer`, `Approval`, `Mint`, `Burn`)

> 🔒 **Reporte completo de auditoría → [nextia-marketing.vercel.app/#audit](https://nextia-marketing.vercel.app/#audit)**

| Suite | Tests | Resultado |
|-------|-------|-----------|
| Advanced & Edge Cases | 9/9 | ✅ |
| Gas Tests ⛽ | 6/6 | ✅ |
| Security Tests 🔒 | 13/13 | ✅ |
| Core Tests | 5/5 | ✅ |
| **Total** | **33/33** | **✅ Sin fallos** |

---

## 🧠 5. Developer Docs (Resumen)

```bash
# Instalar dependencias
npm install

# Compilar contrato
npx hardhat compile

# Ejecutar tests
npx hardhat test

# Ver consumo de gas
REPORT_GAS=true npx hardhat test

# Desplegar en Sepolia
npx hardhat run scripts/deploy.js --network sepolia

# Verificar en Etherscan
npx hardhat verify --network sepolia <address>
```

💡 Framework principal: Hardhat  
🧩 Compilador: Solidity 0.8.20  
⚙️ Testnet activa: Sepolia

---

## 🧪 6. Arquitectura técnica

```
NextiaToken/
│
├── contracts/
│   └── NextiaToken.sol
│
├── test/
│   ├── NextiaToken.extra.test.js
│   ├── NextiaToken.security.test.js
│   ├── NextiaToken.gas.test.js
│   └── NextiaToken.test.js
│
├── scripts/
│   ├── deploy.js
│   ├── verify.js
│   └── status.js
│
├── .env
├── hardhat.config.js
└── README_final.md
```

---

## 🌐 7. Ecosistema Nextia

NextiaToken es parte del ecosistema Nextia, compuesto por:

- **Nextia Marketing:** servicios web3 y economía digital
- **TokenLab:** incubadora de proyectos blockchain
- **NextiaVerse:** comunidad global, NFT y metaverso

Cada módulo impulsa el valor de NXT dentro del ecosistema.

---

## 📊 8. Datos técnicos

| Dato | Valor |
|------|-------|
| Contrato (Sepolia) | `0x61d0969006E0Fd98De6b378Fcd42C449397Fc044` |
| Framework | Hardhat |
| Lenguaje | Solidity 0.8.20 |
| Gas promedio deploy | 815,697 gas |
| Cobertura de tests | 100% líneas / funciones / branches |
| Tests totales | **33/33** (4 suites) |

---

## 🤝 9. Contribución

1. Haz fork del repo
2. Crea una rama (`feature/nueva-funcionalidad`)
3. Envía tu PR con descripción técnica
4. Antes de subir: ejecuta `npx hardhat test` y asegúrate que todo pase ✅

---

## 💰 10. Contacto e inversión

🌐 Web: https://nextiamarketing.com  
📧 Email: jsensei@tokenlab.nextiamarketing.com  
💬 Telegram: @nextiatoken_presale_bot  
GitHub: https://github.com/NextiaSensei  

> 🔒 Reporte de auditoría: [nextia-marketing.vercel.app/#audit](https://nextia-marketing.vercel.app/#audit)

---

## 🪙 11. Licencia

Este proyecto se distribuye bajo la licencia MIT.  
Libre uso y modificación con atribución.

> “Invertir en NextiaToken es apostar por la unión entre código, arte y comunidad.”  
> — Nextia Labs, 2026
