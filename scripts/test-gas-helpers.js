// scripts/test-gas-helpers.js
const hre = require("hardhat");
const { getGasCost, saveGasReport } = require("./gasReport");

async function main() {
  const { ethers } = hre;

  // 👥 cuentas
  const [owner, addr1] = await ethers.getSigners();

  // 🏗️ deploy
  const NextiaToken = await ethers.getContractFactory("NextiaToken");
  const initialSupply = ethers.parseUnits("1000000", 18);
  const token = await NextiaToken.deploy(initialSupply, owner.address);
  await token.waitForDeployment();

  console.log("✅ Contrato desplegado en:", await token.getAddress());

  // ⛽ costo deploy
  const deployTx = token.deploymentTransaction();
  const deployCost = await getGasCost(deployTx);
  console.log("⛽ Costo del deploy:", deployCost);

  // 🔄 transferencia
  const tx = await token
    .connect(owner)
    .transfer(addr1.address, ethers.parseUnits("1", 18));
  const transferCost = await getGasCost(tx);
  console.log("⛽ Costo de transferencia:", transferCost);

  // 📝 guardar reporte
  saveGasReport({
    deployCost,
    transferCost,
    ts: new Date().toISOString(),
  });
}

main().catch((e) => {
  console.error("❌ Error en el script:", e);
  process.exit(1);
});

