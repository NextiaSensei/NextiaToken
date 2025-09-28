const { ethers } = require("hardhat");

describe("NextiaToken Gas Tests ⛽", function () {
  let Token, token, owner, addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    Token = await ethers.getContractFactory("NextiaToken");
    token = await Token.deploy(
      ethers.parseUnits("1000000", 18), // supply inicial
      owner.address                     // dueño inicial
    );
    if (token.waitForDeployment) await token.waitForDeployment();

    // Guardamos la tx de deploy para medir gas
    this.deployTx = token.deploymentTransaction();
  });

  it("⛽ Gas de deploy", async function () {
    const receipt = await this.deployTx.wait();
    console.log("⛽ Deploy gas used:", receipt.gasUsed.toString());
  });

  it("⛽ Gas de transfer", async function () {
    const tx = await token.transfer(addr1.address, 100);
    const receipt = await tx.wait();
    console.log("⛽ Transfer gas used:", receipt.gasUsed.toString());
  });

  it("⛽ Gas de mint", async function () {
    const tx = await token.mint(addr1.address, ethers.parseUnits("1000", 18));
    const receipt = await tx.wait();
    console.log("⛽ Mint gas used:", receipt.gasUsed.toString());
  });

  it("⛽ Gas de burn", async function () {
    await token.transfer(addr1.address, ethers.parseUnits("500", 18));
    const tx = await token.connect(addr1).burn(ethers.parseUnits("100", 18));
    const receipt = await tx.wait();
    console.log("⛽ Burn gas used:", receipt.gasUsed.toString());
  });

  it("⛽ Gas de pause", async function () {
    const tx = await token.pause();
    const receipt = await tx.wait();
    console.log("⛽ Pause gas used:", receipt.gasUsed.toString());
  });

  it("⛽ Gas de unpause", async function () {
    await token.pause();
    const tx = await token.unpause();
    const receipt = await tx.wait();
    console.log("⛽ Unpause gas used:", receipt.gasUsed.toString());
  });
});

