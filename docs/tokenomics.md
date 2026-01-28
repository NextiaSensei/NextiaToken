# 📘 Tokenomics — NextiaToken (NXT)

**Estado:** Draft técnico  
**Última actualización:** 2026-01-28  
**Versión:** v0.6  
**Network objetivo:** Ethereum (ERC-20)

---

## 1. Resumen Ejecutivo

**NextiaToken (NXT)** es el activo nativo del ecosistema Nextia.  
Su diseño económico prioriza:

- Sostenibilidad a largo plazo  
- Control del riesgo inflacionario  
- Incentivos alineados entre equipo, comunidad y adopción real  

El token está pensado como **utility-first**, con gobernanza progresiva y control de riesgos mediante multisig y timelocks.

---

## 2. Parámetros Base del Token

- **Nombre:** NextiaToken  
- **Símbolo:** NXT  
- **Standard:** ERC-20  
- **Decimals:** 18  
- **Initial Supply:** 1,000,000 NXT  
- **Mint inicial:** Al deployer (temporal)

---

## 3. Política de Supply

### 3.1 Max Supply
**Modelo:** Supply dinámico controlado  

- Mint **permitido**, pero:
  - Solo vía **multisig**
  - Con **límites anuales**
  - Sujeto a **timelock**
  - Visible on-chain

> El max supply definitivo será fijado mediante gobernanza antes de mainnet.

---

## 4. Mint & Burn Policy

### Mint
- Habilitado únicamente para:
  - Incentivos de ecosistema
  - Recompensas de staking
  - Expansión controlada del protocolo
- Límite sugerido: **≤ 5% anual**

### Burn
- Función `burn()` habilitada para holders
- Posible quema futura vía:
  - Fees de plataforma
  - Revenue share
  - Decisión de gobernanza

---

## 5. Distribución Inicial (Escenario Base)

| Categoría                  | %    | NXT     | Condiciones |
|---------------------------|------|---------|-------------|
| Liquidez inicial          | 40%  | 400,000 | DEX / LP |
| Equipo & Desarrollo       | 25%  | 250,000 | Vesting |
| Comunidad & Recompensas   | 20%  | 200,000 | Distribución progresiva |
| Tesorería / Reservas      | 10%  | 100,000 | Timelock |
| Marketing & Partners      | 5%   | 50,000  | Uso estratégico |

> Los porcentajes pueden ajustarse vía gobernanza antes de mainnet.

---

## 6. Vesting & Time-locks

### Equipo
- Vesting lineal: **24 meses**
- Cliff: **3 meses**
- Unlock mensual post-cliff

### Tesorería
- Lock inicial: **12 meses**
- Liberación: trimestral

---

## 7. Gobernanza & Control

- **Owner inicial:** EOA (temporal)
- **Antes de mainnet:**
  - Migración obligatoria a **Gnosis Safe**
  - Implementación de **Timelock**
- **Gobernanza futura:**
  - DAO-lite → DAO completa
  - Propuestas formales (NIPs)

---

## 8. Utilidad del Token

- Pagos dentro de Nextia Market
- Acceso a servicios premium
- Staking
- Incentivos a creadores y afiliados
- Reducción de fees
- Gobernanza (fase futura)

---

## 9. Riesgos y Mitigaciones

| Riesgo | Mitigación |
|------|-----------|
| Inflación excesiva | Límite anual + multisig |
| Dump inicial | Vesting y locks |
| Riesgo técnico | Tests + auditoría |
| Custodia de claves | Hardware wallets + multisig |

---

## 10. Checklist Pre-Mainnet

- [ ] Tests unitarios e integración completos  
- [ ] Auditoría externa  
- [ ] Multisig activo  
- [ ] Timelock configurado  
- [ ] Tokenomics aprobado por gobernanza  
- [ ] Contrato verificado en Etherscan  

---

**Este documento es técnico y versionable.  
Los parámetros finales se fijan antes de mainnet.**

