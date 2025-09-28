// scripts/gasReport.js
const fs = require("fs");
const path = require("path");
const { ethers } = require("hardhat");

// Función para obtener el costo de gas de una transacción
async function getGasCost(txResponse) {
  const txReceipt = await txResponse.wait();

  console.log("📋 Debug receipt:", {
    gasUsed: txReceipt.gasUsed,
    effectiveGasPrice: txReceipt.effectiveGasPrice,
  });

  // Aseguramos conversión segura
  const gasUsed = txReceipt.gasUsed
    ? BigInt(txReceipt.gasUsed.toString())
    : 0n;
  const effectiveGasPrice = txReceipt.effectiveGasPrice
    ? BigInt(txReceipt.effectiveGasPrice.toString())
    : 0n;

  // ⚡ multiplicamos como BigInt
  const gasCost = gasUsed * effectiveGasPrice;

  return {
    gasUsed: gasUsed.toString(),
    gasCostEth: ethers.formatEther(gasCost.toString()),
  };
}

// Función para guardar el reporte en JSON
function saveGasReport(data) {
  const reportsDir = path.join(__dirname, "..", "reports");
  if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir);
  }

  const filePath = path.join(reportsDir, "gas-report.json");

  let existingData = {};
  if (fs.existsSync(filePath)) {
    const fileContent = fs.readFileSync(filePath, "utf8");
    try {
      existingData = JSON.parse(fileContent);
    } catch (error) {
      console.error("Error leyendo el JSON existente:", error.message);
    }
  }

  const finalData = { ...existingData, ...data };

  fs.writeFileSync(filePath, JSON.stringify(finalData, null, 2));
  console.log(`📊 Reporte de gas actualizado en: ${filePath}`);
}

module.exports = {
  getGasCost,
  saveGasReport,
};


