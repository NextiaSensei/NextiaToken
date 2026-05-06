async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with account:", deployer.address);

  const NextiaToken = await ethers.getContractFactory("NextiaToken");
  const initialSupply = ethers.parseEther("1000000");
  const nxtToken = await NextiaToken.deploy(initialSupply, deployer.address);
  await nxtToken.waitForDeployment();

  console.log("NextiaToken deployed to:", nxtToken.target);

  const Governance = await ethers.getContractFactory("Governance");
  const governance = await Governance.deploy(nxtToken.target, deployer.address);
  await governance.waitForDeployment();

  console.log("Governance deployed to:", governance.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

