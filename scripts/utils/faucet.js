const hre = require("hardhat");

async function main() {
  let recipientAddress = process.env.RECIPIENT || "0x369214aD6ddc2a2E6906e75f40CF5A58aF4a7ce1";
  
  // Valida y corrige el checksum
  recipientAddress = hre.ethers.getAddress(recipientAddress);
  
  const amountToSend = "1000";
  const tokenAddress = "0x889C1eA94F67588c7bC733Dc368D3059DE9891CE";

  const [deployer] = await hre.ethers.getSigners();
  
  console.log(`Deployer: ${deployer.address}`);
  
  const token = await hre.ethers.getContractAt("NextiaToken", tokenAddress);
  
  console.log(`🚰 Enviando ${amountToSend} NXT a ${recipientAddress}...`);
  
  const tx = await token.transfer(
    recipientAddress,
    hre.ethers.parseEther(amountToSend)
  );
  
  await tx.wait();
  
  console.log(`✅ Transacción exitosa: ${tx.hash}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
