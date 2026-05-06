async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying Governance with account:", deployer.address);

  const Governance = await ethers.getContractFactory("Governance");
  const governance = await Governance.deploy("TU_DIRECCION_TOKEN", deployer.address); // Reemplaza TU_DIRECCION_TOKEN

  await governance.deployed();

  console.log("Governance deployed to:", governance.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
