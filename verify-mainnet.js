// scripts/verify-mainnet.js
require("dotenv").config();
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const deploymentsPath = path.join(__dirname, "..", "deployments", "NextiaToken_mainnet.json");
  let address;
  let owner;
  if (fs.existsSync(deploymentsPath)) {
    const json = JSON.parse(fs.readFileSync(deploymentsPath, "utf8"));
    address = json.address || json.addresses || json.contract;
    owner = json.deployer || json.owner || process.env.DEPLOYER_ADDRESS;
  }

  if (!address) {
    address = process.argv[2];
    if (!address) throw new Error("Falta la dirección del contrato. Usa: node scripts/verify-mainnet.js <address>");
  }

  const initialSupply = hre.ethers.parseUnits("1000000", 18).toString();
  owner = owner || process.env.DEPLOYER_ADDRESS;
  if (!owner) throw new Error("Falta DEPLOYER_ADDRESS en .env");

  console.log("🔎 Verificando contrato en Mainnet...");
  try {
    await hre.run("verify:verify", {
      address,
      constructorArguments: [initialSupply, owner],
    });
    console.log("✅ Verificación completada en Mainnet:", address);
  } catch (err) {
    console.warn("⚠️ Verificación fallida o en cola:");
    console.warn(err.message || err);
  }
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
