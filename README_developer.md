# 🚀 Nextia Token (NXT)

![Security](https://img.shields.io/badge/Audit-In_Progress-yellow)
![Status](https://img.shields.io/badge/Status-Testnet_Deployed-green)
![Tests](https://img.shields.io/badge/Tests-28%2F28_Passing-brightgreen)

## 📖 Tabla de Contenidos
- [🎯 Visión del Proyecto](#-visión-del-proyecto)
- [🚀 Estado Actual](#-estado-actual)
- [🛠 Instalación y Uso](#-instalación-y-uso)
- [📊 Métricas Técnicas](#-métricas-técnicas)
- [🔐 Seguridad](#-seguridad)
- [🤝 Para Inversionistas](#-para-inversionistas)
- [📈 Roadmap](#-roadmap)

## 🎯 Visión del Proyecto

Nextia Token es el **token utility** del ecosistema Nextia, diseñado para:

### 🎯 Objetivos Principales
- **🔐 Seguridad y Confianza**: Token auditado y verificado
- **🔄 Utilidad Real**: Servicios de marketing, trading y data science
- **👥 Comunidad Activa**: Governance y participación comunitaria
- **🌐 Multi-servicio**: Integración con shop online, IA y trading

### 💡 Casos de Uso
1. **Pagos en servicios Nextia Marketing**
2. **Acceso a herramientas IA de data science**
3. **Recompensas en plataforma de trading**
4. **Governance y votación comunitaria**

## 🚀 Estado Actual

### ✅ **LOGROS COMPLETADOS**
- [x] Contrato ERC20 desplegado en **Sepolia**
- [x] 28/28 tests pasando (100% coverage)
- [x] Análisis de seguridad con Slither
- [x] Optimización de gas completada
- [x] Verificación en Etherscan

### 🔄 **EN PROGRESO**
- [ ] Corrección script de deploy
- [ ] Documentación completa
- [ ] Preparación para mainnet

### 📊 **MÉTRICAS CLAVE**
```bash
📍 Contrato: 0x070E012007a0A523807be9b7BF7589C7395AdEE2
🔗 Blockchain: Ethereum Sepolia
💎 Token: NXT (18 decimales)
📈 Supply: 1,000,000 NXT

🛠 Instalación y Uso
node.js >= 18
npm install

🔧 Comandos Esenciales
# Compilar
npx hardhat compile

# Tests
npx hardhat test

# Deploy local
npx hardhat run scripts/deploy.js --network localhost

# Deploy Sepolia
npx hardhat run scripts/deploy.js --network sepolia

⚙️ Configuración
Crear archivo .env:
# 🔑 Clave privada de la wallet (testnet)
# Formato: 0x seguido de 64 caracteres hexadecimales (ejemplo, generado desde tu MetaMask en Sepolia)
PRIVATE_KEY=TU_PRIVATE_KEY_AQUI

# wallets extra para pruebas multiusuario en Sepolia
TEST_WALLET_2_PRIVATE_KEY
TEST_WALLET_3_PRIVATE_KEY

# 🔌 API key de Alchemy (para conectarte a la red Sepolia)
ALCHEMY_API_KEY=tu_key

# 📜 API key de Etherscan (para verificar contratos si quieres)
ETHERSCAN_API_KEY=tu_etherscan_key

# 📝 Dirección del contrato desplegado (opcional, se llenará después del deploy)
NOMBRE_CONTRACT=TU_DIRECCIÓN_DE_CONTRATO

COINMARKETCAP_API_KEY=TU_API_KEY
REPORT_GAS=true
VERITY_WAIT_BLOCKS=5
HOLESKY_RPC=https://ethereum-holesky-rpc.publicnode.com  # opcional, usa tu pro>

📊 Métricas Técnicas
⛽ Optimización de Gas
Función	Gas Used	Estado
Deploy	815,697	✅ Óptimo
Transfer	53,772	✅ Excelente
Mint	53,816	✅ Excelente
Burn	36,124	✅ Excelente
Pause	27,787	✅ Excelente
🧪 Coverage de Tests
Tests Funcionales: 9/9 ✅

Tests Seguridad: 13/13 ✅

Tests Gas: 6/6 ✅

Total: 28/28 (100%) ✅

🔐 Seguridad
✅ Implementado
Pausable pattern

Role-based access control

Comprehensive testing

Slither analysis

🛡 Próximas Mejoras
Auditoría externa

Multisig implementation

Timelock controller

🤝 Para Inversionistas
💼 Oportunidad de Inversión
Nextia Token representa la columna vertebral del ecosistema Nextia, integrando:

Nextia Marketing (Servicios existentes)

Nextia Trading (Plataforma en desarrollo)

Nextia AI (Asistentes de data science)

Nextia Shop (E-commerce)

📈 Tokenomics (Propuesta)
Concepto	Detalles
Total Supply	1,000,000 NXT
Initial Distribution	TBD
Use Cases	Payments, Governance, Staking
Vesting	Plan por implementar
🔗 Contacto Inversiones
Email: nextiacorp33@gmail.com
Telegram: @JorgeSensei
Sitio Web: https://nextiamarketing.com/

📈 Roadmap
🟢 FASE 1: FUNDAMENTOS (COMPLETADA)
Contrato ERC20 básico

Tests de seguridad

Deploy en testnet

🟡 FASE 2: ECOSISTEMA (EN PROGRESO)
Definición tokenomics completa

Desarrollo DApp básica

Programa de recompensas comunidad

🟠 FASE 3: CRECIMIENTO (PRÓXIMA)
Launch en mainnet

Listado en DEXs

Integración con servicios existentes

🔴 FASE 4: EXPANSIÓN (FUTURO)
Nextia AI integration

Cross-chain implementation

Enterprise solutions

📜 Licencia
MIT © Nextia 2025

❓ Soporte
Para consultas técnicas: Issues en GitHub
Para negocios: nextiacorp33@gmail.com


📂 Estructura del proyecto

    ├── contracts/         # Contratos inteligentes (NextiaToken.sol)
    ├── scripts/           # Scripts de deploy (deploy.js)
    ├── test/              # Tests en JS/TS
    ├── deployments/       # JSON con direcciones y ABI tras cada deploy
    ├── node_modules/      # Dependencias de npm (ignorar en git)
    ├── hardhat.config.js  # Configuración principal
    ├── package.json       # Dependencias y scripts npm
    ├── .env               # Variables privadas (no subir a git)
    └── README.md          # Documentación del proyecto


nextia-token/
│── contracts/
│   └── NextiaToken.sol       # Contrato ERC20
│── scripts/
│   ├── gasReport.js          # Script para medir gas
│   └── test-gas-helpers.js   # Helper de gas
│── test/
│   └── NextiaToken.gas.test.js # Pruebas de gas
│── hardhat.config.js
│── package.json
│── .env                      # Variables privadas (ignorado en Git)
│── .gitignore


