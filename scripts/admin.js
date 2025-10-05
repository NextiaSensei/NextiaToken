const { ethers } = require("hardhat");
require("dotenv").config();

async function main() {
  // === CONFIGURACIÓN ===
  const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS; // la dirección del contrato desplegado
  const ACTION = process.env.ACTION || "status"; // acción: mint | pause | unpause | status
  const AMOUNT = process.env.AMOUNT || "0"; // cantidad para mint (si aplica)
  const RECEIVER = process.env.RECEIVER || ""; // dirección destino para mint

  if (!CONTRACT_ADDRESS) {
    throw new Error("❌ No se encontró CONTRACT_ADDRESS en el .env");
  }

  const [owner] = await ethers.getSigners();
  const NextiaToken = await ethers.getContractFactory("NextiaToken");
  const token = NextiaToken.attach(CONTRACT_ADDRESS);

  console.log(`\n👑 Ejecutando acción '${ACTION}' como: ${owner.address}`);
  console.log(`📄 Contrato: ${CONTRACT_ADDRESS}\n`);

  // === ACCIONES ===
  if (ACTION === "mint") {
    if (!RECEIVER || AMOUNT === "0") {
      throw new Error("⚠️ Para mintear necesitas definir RECEIVER y AMOUNT en .env");
    }
    const tx = await token.mint(RECEIVER, ethers.parseEther(AMOUNT));
    await tx.wait();
    console.log(`✅ Mint completado: ${AMOUNT} NXT para ${RECEIVER}`);

  } else if (ACTION === "pause") {
    const tx = await token.pause();
    await tx.wait();
    console.log("⏸️ Contrato pausado correctamente.");

  } else if (ACTION === "unpause") {
    const tx = await token.unpause();
    await tx.wait();
    console.log("▶️ Contrato reactivado correctamente.");

  } else if (ACTION === "status") {
    const paused = await token.paused();
    const totalSupply = await token.totalSupply();
    console.log(`ℹ️ Estado actual: ${paused ? "PAUSADO" : "ACTIVO"}`);
    console.log(`💰 Total Supply: ${ethers.formatEther(totalSupply)} NXT`);

  } else {
    console.log("⚠️ Acción no reconocida. Usa: mint | pause | unpause | status");
  }
}

main().catch((error) => {
  console.error("❌ Error al ejecutar admin.js:", error);
  process.exitCode = 1;
});

