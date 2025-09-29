const { ethers } = require("hardhat");

async function main() {
    const [owner, addr1] = await ethers.getSigners();
    const Token = await ethers.getContractFactory("NextiaToken");

    console.log("=== Deploy ===");
    const deployTx = await Token.deploy(
        ethers.parseUnits("1000000", 18),
        owner.address
    );
    const deployReceipt = await deployTx.deploymentTransaction().wait();
    console.log("Gas usado deploy:", deployReceipt.gasUsed.toString());

    console.log("=== Transfer ===");
    const transferTx = await deployTx.transfer(addr1.address, 100);
    const transferReceipt = await transferTx.wait();
    console.log("Gas usado transfer:", transferReceipt.gasUsed.toString());

    console.log("=== Mint ===");
    const mintTx = await deployTx.mint(addr1.address, 100);
    const mintReceipt = await mintTx.wait();
    console.log("Gas usado mint:", mintReceipt.gasUsed.toString());

    console.log("=== Burn ===");
    const burnTx = await deployTx.burn(50);
    const burnReceipt = await burnTx.wait();
    console.log("Gas usado burn:", burnReceipt.gasUsed.toString());

    console.log("=== Pause ===");
    const pauseTx = await deployTx.pause();
    const pauseReceipt = await pauseTx.wait();
    console.log("Gas usado pause:", pauseReceipt.gasUsed.toString());

    console.log("=== Unpause ===");
    const unpauseTx = await deployTx.unpause();
    const unpauseReceipt = await unpauseTx.wait();
    console.log("Gas usado unpause:", unpauseReceipt.gasUsed.toString());
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
