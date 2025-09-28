const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("NextiaToken - extra tests", function () {
  let Token, token, owner, addr1, addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    Token = await ethers.getContractFactory("NextiaToken");
    token = await Token.deploy(
      ethers.parseUnits("1000000", 18),
      owner.address
    );
    // En ethers v6, waitForDeployment puede existir; si existe, esperamos.
    if (token.waitForDeployment) await token.waitForDeployment();
  });

  it("approve, allowance y transferFrom funcionan", async function () {
    // Owner aprueba 200 a addr1
    await token.approve(addr1.address, ethers.parseUnits("200", 18));
    const allowance = await token.allowance(owner.address, addr1.address);
    expect(allowance).to.equal(ethers.parseUnits("200", 18));

    // addr1 hace transferFrom por 100
    await token.connect(addr1).transferFrom(owner.address, addr2.address, ethers.parseUnits("100", 18));
    const bal2 = await token.balanceOf(addr2.address);
    expect(bal2).to.equal(ethers.parseUnits("100", 18));
  });

  it("transfer falla si el balance es insuficiente", async function () {
    await expect(
      token.connect(addr1).transfer(owner.address, ethers.parseUnits("1", 18))
    ).to.be.reverted;
  });

  it("mint solo owner (si la función mint existe)", async function () {
    // Si el contrato no tiene mint, saltamos este test
    let hasMint = true;
    try {
      token.interface.getFunction("mint");
    } catch (e) {
      hasMint = false;
    }
    if (!hasMint) this.skip();

    // mint desde addr1 debe fallar
    await expect(
      token.connect(addr1).mint(addr1.address, ethers.parseUnits("10", 18))
    ).to.be.reverted;

    // mint desde owner debe funcionar
    await token.connect(owner).mint(addr1.address, ethers.parseUnits("10", 18));
    const b = await token.balanceOf(addr1.address);
    expect(b).to.equal(ethers.parseUnits("10", 18));
  });

  it("burn reduce balance y falla si intenta quemar más que tiene", async function () {
    // damos 50 a addr1
    await token.transfer(addr1.address, ethers.parseUnits("50", 18));
    await token.connect(addr1).burn(ethers.parseUnits("20", 18));
    const b = await token.balanceOf(addr1.address);
    expect(b).to.equal(ethers.parseUnits("30", 18));

    // intentar quemar más del balance debe revertir
    await expect(token.connect(addr1).burn(ethers.parseUnits("1000", 18))).to.be.reverted;
  });
});
