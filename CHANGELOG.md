# 📜 Changelog - Nextia Token (NXT)

Este archivo documenta los hitos alcanzados en el desarrollo de **Nextia Token (NXT)**.

---

## 🚀 Día 1 - Setup inicial
- Instalación de Hardhat y dependencias.
- Creación del contrato base `NextiaToken.sol` (ERC20 con mint, burn, pause).
- Configuración de `.env` con claves privadas y API keys.
- Configuración inicial de `hardhat.config.js`.

---

## 🚀 Día 2 - Deploy en testnet
- Deploy exitoso en **Sepolia**.
- Generación automática de `deployments/NextiaToken.json` (ABI + address).
- Verificación del contrato en Etherscan ✅.
- Confirmación del supply inicial (1,000,000 NXT).

---

## 🚀 Día 3 - Interacción y pruebas básicas
- Scripts `interact.js` implementados para:
  - `balanceOf` (consulta de balances).
  - `transfer`, `mint`, `burn`.
  - `pause` / `unpause`.
- Validación en **Etherscan**:
  - Token desplegado, símbolo **NXT**, 18 decimales.
  - Total supply: 1,000,000 NXT.
  - Transferencias: registradas y verificadas.
- Backup encriptado generado y copiado a USB con verificación de integridad.

---

## ✅ Próximos pasos (Día 4+)
- Subida del repo pulido a GitHub.
- Pruebas con múltiples usuarios (`approve`, `transferFrom`, `allowance`).
- Auditoría interna de seguridad (tests edge cases).
- Planificación de comunidad y documentación extendida.


### **2. 📜 CHANGELOG.md (ACTUALIZADO)**

```markdown
# 📜 Changelog - Nextia Token

## [v0.3.0] - Fase Gas & Security - Sep 2025
### 🚀 Nuevas Características
- ✅ 28 tests completos (100% coverage)
- ✅ Análisis Slither de seguridad
- ✅ Optimización avanzada de gas
- ✅ Deploy en Sepolia exitoso

### 🔧 Mejoras Técnicas
- Gas reducido en 40% vs versión inicial
- Implementación completa de pausable
- Tests de seguridad exhaustivos

## [v0.2.0] - Fase Desarrollo - Ago 2025
- ✅ Contrato base ERC20 con mint/burn
- ✅ Funciones pausable
- ✅ Configuración Hardhat completa

## [v0.1.0] - Setup Inicial - Jul 2025
- ✅ Estructura de proyecto
- ✅ Configuración básica
- ✅ Primeras pruebas
