# 📘 Tokenomics PRO — NextiaToken (NXT)

*Última actualización: 2025-09-22*  

---

## Resumen ejecutivo
**Nombre:** NextiaToken (NXT)  
**Ticker:** NXT  
**Decimals:** 18  
**Funcionalidad principal:** medio de pago interno (Nextia Market), acceso a servicios premium, staking e incentivos para la comunidad.  
**Objetivo:** Alinear adopción de la comunidad con crecimiento sostenible de la plataforma Nextia (marketing, shop, trading).

---

## 1 — Supply & parámetros básicos
- **Initial supply:** 1,000,000 NXT (mint inicial al deployer)  
- **Max supply:** *[definir]* — opciones:
  - **Fijo** (sin mint futuro): seguridad y predictibilidad.
  - **Dinámico** (mint controlado): flexibilidad para incentivos; requiere límites estrictos.
- **Decimals:** 18

---

## 2 — Política de mint & burn
- **Mint:** [Sí/No] — *recomendado:* `Sí` controlado por **multisig** con límites anuales (ej. max 5% del supply por año).  
- **Burn:** Permitido para usuarios (función `burn()`); posible mecanismo de quema por fees/operaciones (definir %).

---

## 3 — Distribución inicial (ejemplo)
- **40% Liquidez (DEX / Provisionamiento)** — 400,000 NXT  
- **25% Equipo & Desarrollo** — 250,000 NXT (vesting 24 meses, cliff 3-6 meses)  
- **20% Comunidad & Recompensas** — 200,000 NXT (airdrops, staking rewards)  
- **10% Reservas / Tesorería** — 100,000 NXT (timelocked)  
- **5% Marketing & Partners** — 50,000 NXT

> Ajusta porcentajes según estrategia de crecimiento y necesidades de liquidez.

---

## 4 — Vesting / Time-lock
- **Equipo:** vesting lineal 24 meses, cliff 3 meses. Desbloqueo mensual después del cliff.  
- **Reservas:** bloqueadas 12 meses, liberación trimestral.  
- **Multisig + Timelock:** cambios críticos (mint, burn, transfer ownership) deben pasar por multisig + timelock (ej. 48-72 horas).

---

## 5 — Gobernanza y control
- **Owner inicial:** EOA del deploy (temporal).  
- **Plan obligatorio antes de testnet→mainnet:** migrar a **Gnosis Safe (multisig)** y añadir **timelock**.  
- **Governance:** roadmap para evaluar DAO/DAO-lite después de adopción y comunidad activa.

---

## 6 — Usos & utilidades (on-chain / off-chain)
- **Pago de servicios** en Nextia Market (descuentos por pagar con NXT).  
- **Acceso premium** (clases, reports, señales) mediante staking.  
- **Staking rewards**: incentivar holders con recompensas en NXT o revenue-share.  
- **Incentivos para creadores** y afiliados.  
- **Integración futura:** pagos P2P, fees reducidos para holders.

---

## 7 — Mecanismos económicos (incentivos)
- **Staking:** lock > obtener rewards (definir APR objetivo).  
- **Rewards por actividad:** campañas, referrals, uso del shop.  
- **Quema periódica:** porcentaje de fees convertido a NXT y quemado (si se decide).

---

## 8 — Riesgos & mitigaciones (para inversionistas)
- **Riesgo de mint ilimitado:** Mitigar con multisig + límites anuales + auditoría.  
- **Dump inicial:** mitigación con vesting y programas de incentivos a largo plazo.  
- **Riesgos técnicos:** auditoría de smart contracts, tests exhaustivos y bounty program.  
- **Exposición de claves privadas:** usar gestores y hardware wallets; no subir .env.

---

## 9 — Roadmap operativo (pre-mainnet)
1. Completar tests (unitarios e integraciones).  
2. Auditoría (externa) + fixes.  
3. Implementar multisig (Gnosis Safe) y timelock.  
4. Deploy en testnet (Sepolia / Mumbai).  
5. Revisar analytics / explorer y corregir.  
6. Plan de lanzamiento (liquidity, exchanges, marketing).  

---

## 10 — Checklist para deploy final
- [ ] Tests 100% verdes (unit + integration).  
- [ ] Auditoría externa realizada.  
- [ ] Owner migrado a multisig.  
- [ ] Timelock configurado.  
- [ ] Contract verified en Etherscan.  
- [ ] Backups cifrados + signatures de release.  
- [ ] Tokenomics final aprobado por el equipo.

---

## 11 — Notas legales & compliance
- Revisar regulación en jurisdicciones objetivo.  
- Preparar T&C para uso de token en la plataforma.  
- Consultar con abogado para KYC/AML si habrá compra/venta directa.

---

*Este documento es un borrador pro — rellena números, límites y políticas exactas antes de mainnet.*


# 📊 Tokenomics — Nextia Token

## 1. Resumen Ejecutivo
Breve explicación del propósito del token y su papel dentro del ecosistema Nextia.

---

## 2. Suministro Total
- **Cantidad Máxima (hard cap):** X,XXX,XXX tokens
- **Suministro Inicial:** X,XXX,XXX tokens
- **Modelo de Emisión:** [Deflacionario / Inflacionario controlado / Suministro fijo]

---

## 3. Utilidad del Token
- Medio de pago en el ecosistema
- Staking y recompensas
- Acceso a funciones premium
- Gobernanza (votaciones sobre decisiones del proyecto)
- Incentivos para adopción temprana

---

## 4. Distribución del Token
| Categoría             | Porcentaje | Tokens Asignados | Detalles de Desbloqueo |
|------------------------|------------|------------------|-------------------------|
| Equipo                | XX%        | X,XXX,XXX        | Vesting 24 meses        |
| Inversores privados   | XX%        | X,XXX,XXX        | Vesting 12 meses        |
| Liquidez inicial      | XX%        | X,XXX,XXX        | Liberación inmediata    |
| Tesorería             | XX%        | X,XXX,XXX        | Liberación parcial      |
| Comunidad & Recompensas | XX%      | X,XXX,XXX        | Reparto progresivo      |
| Marketing & Alianzas  | XX%        | X,XXX,XXX        | Flexible según estrategia|

---

## 5. Estructuras de Incentivos
- **Staking Rewards:** APY inicial del X%
- **Burn Mechanism:** X% de cada transacción se quema
- **Liquidity Mining:** recompensas a proveedores de liquidez
- **Gamificación:** puntos y niveles para holders fieles

---

## 6. Gobernanza
- Votaciones on-chain
- Propuestas de mejora (NIPs - Nextia Improvement Proposals)
- Sistema de reputación para votantes

---

## 7. Seguridad y Transparencia
- Smart contracts auditados
- Reservas visibles on-chain
- Reportes trimestrales para la comunidad

---

## 8. Roadmap Financiero
- Q1: Venta privada
- Q2: IDO / IEO
- Q3: Expansión de utilidad real del token
- Q4: Integración con exchanges centralizados


