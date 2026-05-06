const hre = require("hardhat");

async function main() {
  console.log("🚀 Desplegando Staking...");
  const [deployer] = await hre.ethers.getSigners();
  const NEXTIA_TOKEN_ADDRESS = "0xaE2401dF47E78328CF80b5Ae55D4A1b7A509DD66";

  const Staking = await hre.ethers.getContractFactory("Staking");
  const staking = await Staking.deploy(NEXTIA_TOKEN_ADDRESS, deployer.address);
  await staking.waitForDeployment();

  console.log("✅ Staking deployado en:", staking.target);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
