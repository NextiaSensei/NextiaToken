const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("🚀 Iniciando despliegue en red:", hre.network.name);

  // 📌 Cuenta que va a desplegar
  const [deployer] = await hre.ethers.getSigners();
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("👤 Deployer:", deployer.address);
  console.log("💰 Balance (ETH):", hre.ethers.formatEther(balance));

  // ⚙️ Preparar contrato
  const NextiaToken = await hre.ethers.getContractFactory("NextiaToken");

  // ✅ Inicial supply de 1 millón (con 18 decimales)
  const initialSupply = hre.ethers.parseUnits("1000000", 18);

  console.log("⏳ Desplegando contrato NextiaToken...");
  const token = await NextiaToken.deploy(initialSupply, deployer.address);

  // Esperar confirmación
  await token.waitForDeployment();

  const contractAddress = await token.getAddress();
  console.log("✅ NextiaToken desplegado en:", contractAddress);

  // ---- Guardar datos de despliegue ----
  const deploymentsDir = path.join(__dirname, "..", "deployments");
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir);
  }

  const deploymentData = {
    name: "NextiaToken",
    address: contractAddress,
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    abi: JSON.parse(token.interface.formatJson()), // Guardamos ABI
  };

  const filePath = path.join(deploymentsDir, "NextiaToken.json");
  fs.writeFileSync(filePath, JSON.stringify(deploymentData, null, 2));

  console.log("📂 Guardado en:", filePath);
  console.log("🎉 Deploy finalizado correctamente.");

  // ---- Verificación opcional en Etherscan ----
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    const waitBlocks = process.env.VERIFY_WAIT_BLOCKS
      ? parseInt(process.env.VERIFY_WAIT_BLOCKS)
      : 5;
    console.log(`⏱ Esperando ${waitBlocks} bloques antes de verificar en Etherscan...`);
    await token.deployTransaction.wait(waitBlocks);

    try {
      console.log("🔎 Verificando contrato en Etherscan...");
      await hre.run("verify:verify", {
        address: contractAddress,
        constructorArguments: [initialSupply, deployer.address],
      });
      console.log("✅ Verificación finalizada");
    } catch (err) {
      console.warn("⚠️ Verificación fallida o ya verificada. Error:");
      console.warn(err.message || err);
    }
  } else {
    console.log("Local network — se omite verificación.");
  }
}

main().catch((err) => {
  console.error("❌ Error en el despliegue:", err);
  process.exitCode = 1;
});



