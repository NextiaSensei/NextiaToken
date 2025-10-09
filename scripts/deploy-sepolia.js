// scripts/deploy-sepolia.js
require("dotenv").config();
const hre = require("hardhat");

async function main() {
  console.log("🚀 Iniciando despliegue de NextiaToken en Sepolia...");

  // === Configura valores de inicialización ===
  const initialSupply = hre.ethers.parseUnits("1000000", 18); // 1 millón de tokens
  const initialOwner = process.env.DEPLOYER_ADDRESS;

  if (!initialOwner) {
    throw new Error("❌ Falta DEPLOYER_ADDRESS en el archivo .env");
  }

  // === Despliegue ===
  const NextiaToken = await hre.ethers.getContractFactory("NextiaToken");
  const nextiaToken = await NextiaToken.deploy(initialSupply, initialOwner);

  // ✅ Esperar confirmación
  await nextiaToken.waitForDeployment();

  const deployedAddress = await nextiaToken.getAddress();
  console.log(`✅ NextiaToken desplegado en Sepolia: ${deployedAddress}`);
  console.log(`👑 Propietario inicial: ${initialOwner}`);
  console.log(`💰 Suministro inicial: ${hre.ethers.formatUnits(initialSupply, 18)} NXT`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Error en despliegue:", error);
    process.exit(1);
  });

