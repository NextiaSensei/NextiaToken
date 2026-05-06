require("dotenv").config();
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("🚀 Iniciando despliegue en SEPOLIA Testnet...");

  const [deployer] = await hre.ethers.getSigners();
  console.log("👤 Cuenta deployer:", deployer.address);

  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("💰 Balance actual:", hre.ethers.formatEther(balance), "ETH");

  const NextiaToken = await hre.ethers.getContractFactory("NextiaToken");
  const initialSupply = hre.ethers.parseUnits("1000000", 18);

  console.log("📦 Desplegando contrato...");
  const token = await NextiaToken.deploy(initialSupply, deployer.address);
  await token.waitForDeployment();

  const address = await token.getAddress();
  console.log("✅ Contrato desplegado correctamente en SEPOLIA:", address);

  const deploymentsPath = path.join(__dirname, "..", "deployments", "NextiaToken_testnet.json");
  fs.writeFileSync(deploymentsPath, JSON.stringify({ address, deployer: deployer.address }, null, 2));

  console.log("💾 Guardado en:", deploymentsPath);
}

main().catch((error) => {
  console.error("❌ Error en el despliegue:", error);
  process.exit(1);
});
