# 🚀 Nextia Token (NXT)
# 🧠 NextiaToken — Developer Documentation (v0.5 Pre-Mainnet)

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

Bienvenido al **repositorio de desarrollo de NextiaToken**, el token central del ecosistema Nextia.  
Este documento guía a los desarrolladores que deseen **compilar, testear, desplegar o auditar** el contrato.

---

## ⚙️ 1. Requisitos previos

Asegúrate de tener instalado:

- **Node.js** ≥ 18.0.0  
- **npm** ≥ 9  
- **Hardhat**  
- **Git**  
- **Cuenta en [Alchemy](https://www.alchemy.com)**  
- **Wallet MetaMask (con red Sepolia)**  

> ⚠️ Nota: Hardhat no recomienda versiones de Node.js superiores a 18.16 — idealmente usa `18.16.x` para evitar advertencias.

---

## 🧩 2. Clonar y configurar entorno

```bash
git clone https://github.com/NextiaLabs/NextiaToken.git
cd NextiaToken
npm install

Crea tu archivo .env (o copia el ejemplo .env.example):
PRIVATE_KEY=0x...
ALCHEMY_API_KEY=...
ETHERSCAN_API_KEY=...
COINMARKETCAP_API_KEY=...
REPORT_GAS=true


🚀 3. Comandos esenciales
Comando	Acción
npx hardhat compile	Compila los contratos Solidity
npx hardhat test	Ejecuta todas las pruebas (Mocha/Chai)
npx hardhat coverage	Genera reporte de cobertura (solidity-coverage)
REPORT_GAS=true npx hardhat test	Muestra consumo de gas por operación
npx hardhat run scripts/deploy.js --network sepolia	Despliega contrato en Sepolia
npx hardhat verify --network sepolia <address>	Verifica contrato en Etherscan

🧪 4. Estructura de archivos

NextiaToken/
│
├── contracts/
│   └── NextiaToken.sol
│
├── test/
│   ├── NextiaToken.extra.test.js
│   ├── NextiaToken.gas.test.js
│   ├── NextiaToken.security.test.js
│   └── ...
│
├── scripts/
│   ├── deploy.js
│   ├── verify.js
│   └── status.js
│
├── .env
├── hardhat.config.js
└── README_developer.md


🛡️ 5. Seguridad y auditoría
El contrato incluye:

Patrón Ownable + Pausable (control total del owner)

Eventos Transfer y Approval verificados

Protección contra reentrancy

Control estricto de mint y burn

Pruebas completas (100% coverage)

Para auditorías externas, recomendamos:

MythX

Slither

Solhint

🌐 6. Redes soportadas
Red	Status	Explorador
Hardhat local	✅ activo	—
Sepolia Testnet	✅ activo	https://sepolia.etherscan.io
Ethereum Mainnet	🕓 planificado (fase v0.6)	—

🤝 7. Contribución
Si deseas contribuir:

Crea un fork del repo

Crea una rama feature/nueva-funcionalidad

Envía tu Pull Request

Antes de enviar, asegúrate de que todos los tests pasen (npx hardhat test).

🧭 8. Estado actual del proyecto
Módulo	Estado	Cobertura
Core ERC20	✅ Completado	100%
Seguridad	✅ Completado	100%
Gas Optimization	✅ Completado	—
Dashboard Dev	⚙️ En desarrollo (fase 5.1)	
Documentación	✅ Pre-Mainnet (fase 5.2)	
CI/CD	🕓 Próxima fase (v0.6)	

🪙 9. Licencia
Este proyecto está bajo licencia MIT — libre uso y modificación con atribución.


