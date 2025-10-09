const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("🚀 Iniciando despliegue en red:", hre.network.name);

  // 👤 Cuenta que despliega
  const [deployer] = await hre.ethers.getSigners();
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("👤 Deployer:", deployer.address);
  console.log("💰 Balance disponible:", hre.ethers.formatEther(balance), "ETH");

  // ⚙️ Preparar contrato
  const NextiaToken = await hre.ethers.getContractFactory("NextiaToken");

  // ✅ Supply inicial — 1 millón de tokens con 18 decimales
  const initialSupply = hre.ethers.parseUnits("1000000", 18);

  console.log("⏳ Desplegando contrato NextiaToken...");
  const token = await NextiaToken.deploy(initialSupply, deployer.address, {
    gasLimit: 3_500_000, // límite manual para evitar fallos en Sepolia/Mainnet
  });

  // Esperar confirmación
  await token.waitForDeployment();

  const contractAddress = await token.getAddress();
  console.log("✅ Contrato desplegado en:", contractAddress);

  // ---- Guardar datos de despliegue ----
  const deploymentsDir = path.join(__dirname, "..", "deployments");
  if (!fs.existsSync(deploymentsDir)) fs.mkdirSync(deploymentsDir);

  const deploymentData = {
    name: "NextiaToken",
    address: contractAddress,
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    abi: JSON.parse(token.interface.formatJson()),
  };

  const filePath = path.join(deploymentsDir, `NextiaToken_${hre.network.name}.json`);
  fs.writeFileSync(filePath, JSON.stringify(deploymentData, null, 2));

  console.log("📂 Datos guardados en:", filePath);
  console.log("🎉 Despliegue exitoso 🚀");

  // ---- Verificación automática en Etherscan ----
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    const waitBlocks = parseInt(process.env.VERIFY_WAIT_BLOCKS || "5");
    console.log(`⏱ Esperando ${waitBlocks} bloques antes de verificar en Etherscan...`);
    await hre.network.provider.send("hardhat_waitForConfirmations", [waitBlocks]);

    try {
      console.log("🔎 Verificando contrato en Etherscan...");
      await hre.run("verify:verify", {
        address: contractAddress,
        constructorArguments: [initialSupply, deployer.address],
      });
      console.log("✅ Verificación completada con éxito");
    } catch (err) {
      console.warn("⚠️ Verificación fallida o ya verificada.");
      console.warn(err.message || err);
    }
  } else {
    console.log("🧪 Red local detectada — verificación omitida.");
  }
}

// Ejecución controlada
main().catch((err) => {
  console.error("❌ Error en el despliegue:", err);
  process.exitCode = 1;
});


