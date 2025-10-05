# 💎 NextiaToken — v0.5 Pre-Mainnet

**NextiaToken ($NXTA)** es el activo digital central del ecosistema **Nextia**, un proyecto que fusiona tecnología, creatividad y valor real para construir una economía web3 autónoma.

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
| **v0.1 - v0.4** | Contrato base, auditorías y pruebas internas | ✅ Completado |
| **v0.5 (actual)** | Pre-Mainnet + documentación técnica + dashboard dev | 🚀 Activa |
| **v0.6** | CI/CD + despliegue en Ethereum Mainnet | 🕓 En curso |
| **v0.7+** | Integración con dApps Nextia y staking | 🔮 Planeado |

---

## 🪙 3. Tokenomics

| Parámetro | Valor |
|------------|--------|
| **Símbolo** | NXTA |
| **Red actual** | Ethereum (Sepolia Testnet) |
| **Suministro total** | 1,000,000 NXTA |
| **Propiedad inicial** | Nextia Labs |
| **Política de emisión** | Controlado por `onlyOwner` |
| **Funciones clave** | Mint / Burn / Pause / Unpause |

---

## 🔐 4. Seguridad y transparencia

- Auditoría interna completa  
- 100% cobertura de pruebas automatizadas  
- Contrato verificado públicamente  
- Protección ante reentrancy  
- Control de roles y pausas  
- Eventos ERC-20 (`Transfer`, `Approval`, `Mint`, `Burn`)  

> Seguridad, eficiencia y claridad son los pilares de NextiaToken.

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

💡 Framework principal: Hardhat
🧩 Compilador: Solidity 0.8.20
⚙️ Testnet activa: Sepolia

🧪 6. Arquitectura técnica

NextiaToken/
│
├── contracts/
│   └── NextiaToken.sol
│
├── test/
│   ├── NextiaToken.extra.test.js
│   ├── NextiaToken.security.test.js
│   └── NextiaToken.gas.test.js
│
├── scripts/
│   ├── deploy.js
│   ├── verify.js
│   └── status.js
│
├── .env
├── hardhat.config.js
└── README_final.md

🌐 7. Ecosistema Nextia

NextiaToken es parte del ecosistema Nextia, compuesto por:

Nextia Marketing: servicios web3 y economía digital

TokenLab: incubadora de proyectos blockchain

NextiaVerse: comunidad global, NFT y metaverso

Cada módulo impulsa el valor de NXTA dentro del ecosistema.

📊 8. Datos técnicos
Dato	Valor
Contrato (Sepolia)	0x61d0969006E0Fd98De6b378Fcd42C449397Fc044
Framework	Hardhat
Lenguaje	Solidity 0.8.20
Gas promedio deploy	815,697 gas
Cobertura de tests	100% líneas / funciones / branches
🤝 9. Contribución

Haz fork del repo

Crea una rama (feature/nueva-funcionalidad)

Envía tu PR con descripción técnica

Antes de subir: ejecuta npx hardhat test y asegúrate de que todo pase ✅

💰 10. Contacto e inversión

🌐 Web: https://nextiamarketing.com

🐦 X/Twitter: @NextiaLabs

📧 Email: contact@nextiamarketing.com

💬 Telegram: @NextiaCommunity

🪙 11. Licencia

Este proyecto se distribuye bajo la licencia MIT.
Libre uso y modificación con atribución.

“Invertir en NextiaToken es apostar por la unión entre código, arte y comunidad.”
— Nextia Labs, 2025


---

## ✅ **2️⃣ Checklist antes del commit final**

| Elemento | Estado |
|-----------|--------|
| `README.md` actualizado | ✅ |
| `README_developer.md` creado | ✅ |
| `README_investors.md` creado | ✅ |
| `README_final.md` creado | ✅ |
| `.env` validado con claves correctas | ✅ |
| `hardhat.config.js` funcional y actualizado | ✅ |
| Tests (`npx hardhat test`) 100% pasados | ✅ |
| Último commit documentado como versión v0.5 Pre-Mainnet | 🕓 Pendiente |
| Push al repo remoto | 🕓 Pendiente |

---

## 🧾 **3️⃣ Commit y push**

Ejecuta esto:

```bash
git add .
git commit -m "📘 v0.5 Pre-Mainnet — Documentación final y preparación para dashboard dev (fase 5.3)"
git push origin main
