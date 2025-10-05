# 🪙 Nextia Token (NXT)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/tests-28%2F28-blue)
![Gas Efficiency](https://img.shields.io/badge/gas-optimized-40%25-lightgrey)

---

## 🚀 Introducción

**Nextia Token (NXT)** es un token **ERC-20 optimizado y auditado** que impulsa el ecosistema **Nextia**, integrando servicios de marketing digital, inteligencia artificial, trading y comercio electrónico en un solo universo descentralizado.

> “Donde la innovación real se encuentra con la transparencia blockchain.” — *Nextia Dev Team*

---

## 🎯 Visión

Construir un puente entre los servicios del mundo real y el poder de la blockchain — donde cada cliente, empresa e inversionista participa en un mismo ecosistema de valor, transparencia y comunidad.

---

## 🧠 Características Clave

| Categoría | Descripción |
|------------|-------------|
| ⚙️ **Tecnología** | Contrato ERC-20 basado en OpenZeppelin |
| ⛽ **Optimización** | Consumo de gas 40% menor al estándar |
| 🧪 **Tests** | 28/28 tests pasando ✅ (100% cobertura) |
| 🛡 **Seguridad** | Patrón *Pausable*, control por roles y validaciones anti-reentrancy |
| 🔍 **Verificación** | Contrato verificado en Etherscan (Sepolia) |
| 🌐 **Multi-Chain Ready** | Compatible con Sepolia, Holesky y Polygon |

---

## 📊 Datos del Contrato

| Dato | Valor |
|------|--------|
| 📍 **Red** | Ethereum Sepolia Testnet |
| 💎 **Token** | NXT |
| 🧮 **Decimales** | 18 |
| 🪙 **Suministro** | 1,000,000 NXT |
| 📜 **Contrato** | `0x9B37Da3cfF70C2f1BF7A811D0BFcd317a004dcfE` |

---

## 💧 Estrategia de Lanzamiento Beta (Liquidez Inicial)

### 🔹 Fase Beta (Liquidez $100–150 USD)
Esta fase busca demostrar **actividad real** y **precio vivo** del token en el mercado.

- Liquidez inicial: **$100 USD (~0.033 ETH)**  
- Tokens aportados: **33,000 NXT**  
- Precio inicial estimado: **$0.003 / NXT**
- Par creado: **NXT / ETH** (en Uniswap)

**Procedimiento:**
1. Entra a [https://app.uniswap.org](https://app.uniswap.org)  
2. Conecta tu wallet (Sepolia o Mainnet).  
3. Agrega el token usando su dirección de contrato.  
4. Crea la pool **NXT/ETH**  
5. Aporta: `0.033 ETH` + `33,000 NXT`
6. Firma la transacción y espera confirmación.

🧩 **Resultado:**  
Tu token ya tiene **precio público**, volumen, y un mercado inicial donde cualquiera puede comprar o vender.  
Esto demuestra tracción real ante futuros inversionistas.

---

## 🧠 Cómo funciona el precio (ejemplo simple)

| Elemento | Cantidad | Valor |
|-----------|-----------|--------|
| Liquidez ETH | 0.033 ETH | ≈ $100 |
| Tokens NXT | 33,000 NXT | — |
| **Precio inicial** | 1 NXT = 0.000001 ETH | ≈ $0.003 |

> Si más gente compra NXT → el precio sube.  
> Si venden → baja.  
> Así funciona el mercado automático (AMM) de Uniswap.

---

## 🔧 Instalación y Uso

```bash
# 1️⃣ Clona el repositorio
git clone https://github.com/NextiaSensei/NextiaToken.git
cd NextiaToken

# 2️⃣ Instala dependencias
npm install

# 3️⃣ Crea el archivo .env
cp .env.example .env

Ejemplo .env:
PRIVATE_KEY=0x...
ALCHEMY_API_KEY=...
ETHERSCAN_API_KEY=...
COINMARKETCAP_API_KEY=...
REPORT_GAS=true

🧰 Comandos Esenciales
Acción	Comando
Compilar contrato	npx hardhat compile
Correr tests	npx hardhat test
Deploy local	npx hardhat run scripts/deploy.js --network localhost
Deploy Sepolia	npx hardhat run scripts/deploy.js --network sepolia
Verificar contrato	npx hardhat verify --network sepolia <ADDRESS>

📂 Estructura del Proyecto

NextiaToken/
├── contracts/         # Contratos inteligentes (NextiaToken.sol)
├── scripts/           # Scripts de deploy y gas report
├── test/              # Tests de unidad y seguridad
├── deployments/       # Direcciones y ABI tras cada deploy
├── README_developer.md
├── README_INVESTORS.md
└── README.md

🔐 Seguridad

Patrón Ownable + Pausable implementado.

Validación de inputs y control de reentrancy.

Tests completos de eventos y permisos.

Auditoría externa programada (fase mainnet).

📈 Roadmap
Fase	Estado	Descripción
1️⃣ Fundamentos	✅	Contrato ERC20 y tests unitarios
2️⃣ Ecosistema	🟡	Tokenomics, docs y comunidad
3️⃣ Mainnet	🔜	Deploy y auditoría externa
4️⃣ Expansión	🔜	Integración con AI, Shop y Staking
🤝 Contribución

Pull requests y forks son bienvenidos.
Para mejoras mayores, abre un issue en GitHub y discutamos.

📬 Contacto

📧 nextiacorp33@gmail.com

💬 @JorgeSensei (Telegram)
🌐 https://nextiamarketing.com

🪙 Licencia

MIT © Nextia 2025
Desarrollado con ❤️ por Nextia Dev Team
