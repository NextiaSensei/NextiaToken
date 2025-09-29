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

# 🚀 NextiaToken

Smart contract ERC20 con funciones extendidas (mint, burn, pause, unpause) y pruebas de gas.  
Proyecto basado en **Hardhat** para medición, testeo y optimización.

---

## 📦 Instalación

Clona el repo y entra a la carpeta:

```bash
git clone https://github.com/https://github.com/NextiaSensei/NextiaToken.git
cd nextia-token

npm install

⚙️ Configuración

Crea archivo .env en la raíz (no subir a GitHub 🚫).

Asegúrate de tener node.js >= 18 y hardhat instalado.

Configura hardhat.config.js con tus redes (ej. hardhat, sepolia, holesky).

🧪 Tests de Gas

Ejecuta los tests de gas:

npx hardhat test test/NextiaToken.gas.test.js --network hardhat

✅ Ejemplo de salida:
  NextiaToken Gas Tests ⛽
⛽ Deploy gas used: 1363956
⛽ Transfer gas used: 54443
⛽ Mint gas used: 54533
⛽ Burn gas used: 36519
⛽ Pause gas used: 28191
⛽ Unpause gas used: 28144

  6 passing (338ms)

📂 Estructura del proyecto
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

📝 Checklist de la versión actual (v0.1 – "Gas Ready")

 Configuración de entorno Hardhat.

 Scripts para medir gas (gasReport.js, test-gas-helpers.js).

 Tests unitarios de gas (NextiaToken.gas.test.js).

 Deploy y ejecución correcta de todas las funciones.

 Repo preparado para GitHub.

🔮 Lo que sigue (v0.2)

Integrar hardhat-gas-reporter para reportes automáticos.

Añadir solidity-coverage para cobertura de pruebas.

Configurar GitHub Actions para CI/CD con tests automáticos.

Optimizar consumo de gas (unchecked, mappings, storage vs memory).

Subir a testnet (Sepolia/Holesky).

🤝 Contribución

Pull requests son bienvenidos.
Para cambios importantes, abre primero un issue para discutir qué te gustaría mejorar.

📜 Licencia

MIT © Nextia

28/09/2025


📈 Resultados observados (ejemplos locales)

Ejemplos de una ejecución local del benchmark (Hardhat):

Deploy: ~1,405,708 gas

Transfer: ~54,443 gas

Mint: ~37,383 gas

Burn: ~36,469 gas

Pause: ~28,213 gas

Unpause: ~28,166 gas

Nota: Los valores varían por compilador, configuración y plugins (estos son números observados en tu entorno local). Reportes y archivos con las métricas están en ./reports/ y la salida del benchmark en consola.

🛡️ Seguridad y buenas prácticas

Owner → usar multisig (Gnosis Safe) antes de mainnet.

Auditoría: tests pasan y cobertura 100%, pero se recomienda auditoría externa (Slither + auditor independiente).

No subir .env. Si accidentalmente lo subes: revocar claves y rotarlas.

Revisar roles (mint/pause) y considerar timelock/vesting para asignaciones.

✅ Checklist (corto)

 Hardhat + gas reporter integrado

 Solidity coverage integrado (100%)

 Tests unitarios & seguridad (28/28)

 Benchmark script: scripts/benchmarkGas.js

 Micro-optimizaciones aplicadas (sin romper OpenZeppelin)

🔜 Próximos pasos (prioridad)

Auditoría automática + manual (slither, revisión manual de roles).

Deploy en testnet pública (Sepolia / Holesky).

Scripts de deploy robustos (scripts/deploy.js con verificación etherscan).

CI/CD (GitHub Actions): compile → test → coverage → gas.

Revisión legal/compliance si se busca inversión pública.

🔗 Referencias locales

Cobertura: ./coverage/

Reports de gas: ./reports/ (si configurado)

Benchmark script: scripts/benchmarkGas.js

Tests: test/NextiaToken.test.js y test/NextiaToken.gas.test.js
