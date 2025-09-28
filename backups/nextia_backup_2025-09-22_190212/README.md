# Nextia Token

Este repositorio contiene el código y configuración del token ERC20
`NextiaToken`, desarrollado con Hardhat.

## 🚀 Cómo levantar el entorno

1.  Clona el repositorio.

2.  Instala dependencias:

    ``` bash
    npm install
    ```

3.  Configura variables de entorno en `.env`:

    ``` env
    ALCHEMY_API_KEY=tu_api_key
    PRIVATE_KEY=tu_private_key
    ETHERSCAN_API_KEY=tu_etherscan_key
    ```

## 📂 Estructura de carpetas

    proyectos/nextia/trading/token/
    ├── contracts/         # Contratos inteligentes (NextiaToken.sol)
    ├── scripts/           # Scripts de deploy (deploy.js)
    ├── test/              # Tests en JS/TS
    ├── deployments/       # JSON con direcciones y ABI tras cada deploy
    ├── node_modules/      # Dependencias de npm (ignorar en git)
    ├── hardhat.config.js  # Configuración principal
    ├── package.json       # Dependencias y scripts npm
    ├── .env               # Variables privadas (no subir a git)
    └── README.md          # Documentación del proyecto

## 🔑 Comandos esenciales

-   Compilar contrato:

    ``` bash
    npx hardhat compile
    ```

-   Correr tests:

    ``` bash
    npx hardhat test
    ```

-   Levantar nodo local:

    ``` bash
    npx hardhat node
    ```

-   Deploy en localhost:

    ``` bash
    npx hardhat run scripts/deploy.js --network localhost
    ```

-   Deploy en Sepolia:

    ``` bash
    npx hardhat run scripts/deploy.js --network sepolia
    ```

-   Verificar contrato en Etherscan:

    ``` bash
    npx hardhat verify --network sepolia <ADDRESS_DEPLOY> "NombreToken" "SYM" 1000000
    ```

## 📜 ABI y direcciones

Tras cada deploy, el contrato y su ABI quedarán guardados en:

    deployments/NextiaToken.json

Ese archivo contiene:\
- Dirección del contrato.\
- ABI.\
- Red de despliegue.

⚠️ **Haz backup offline de este archivo tras cada deploy importante.**

## 🛡️ Seguridad y buenas prácticas

-   **Permisos de mint/burn:** define si solo el `owner` puede mintear y
    si eso es limitado.\

-   **Owner único:** evita tener un solo dueño en mainnet. Usa multisig
    (ej. Gnosis Safe).\

-   **Timelock y vesting:** importante para distribuciones y
    actualizaciones.\

-   **Auditoría interna:** más tests (casos edge, ataques comunes).\

-   **Verificación en Etherscan:** aumenta la confianza de la
    comunidad.\

-   **Nunca subas `.env`:**

    ``` bash
    git ls-files --error-unmatch .env
    ```

    Si aparece, bórralo del repo y rota las claves.

## ✅ Próximos pasos

1.  Añadir más tests (transferFrom, allowance, casos fallidos).\
2.  Pulir tokenomics (suministro inicial, quién recibe tokens).\
3.  Preparar despliegue en testnet (Sepolia).\
4.  Verificar en Etherscan.\
5.  Revisar seguridad (multisig, permisos, vesting).
