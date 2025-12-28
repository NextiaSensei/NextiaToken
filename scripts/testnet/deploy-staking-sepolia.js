const hre = require("hardhat");

async function main() {
  const tokenAddress = "0x889C1eA94F67588c7bC733Dc368D3059DE9891CE";
  const [deployer] = await hre.ethers.getSigners();
  
  console.log("Deploying Staking on Sepolia with owner:", deployer.address);
  
  const Staking = await hre.ethers.getContractFactory("Staking");
  const staking = await Staking.deploy(tokenAddress, deployer.address);
  
  await staking.waitForDeployment();
  const stakingAddress = await staking.getAddress();
  
  console.log("✅ Staking deployed on Sepolia:", stakingAddress);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
