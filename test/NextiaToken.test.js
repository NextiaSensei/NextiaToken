const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("NextiaToken", function () {
  let Token, token, owner, addr1;

  const INITIAL_SUPPLY = ethers.parseUnits("1000000", 18);

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();

    Token = await ethers.getContractFactory("NextiaToken");
    token = await Token.deploy(INITIAL_SUPPLY, owner.address);
  });

  it("assigns initial supply to deployer (owner)", async function () {
    const ownerBalance = await token.balanceOf(owner.address);
    expect(ownerBalance).to.equal(INITIAL_SUPPLY);
  });

  it("allows transfers between accounts", async function () {
    await token.transfer(addr1.address, 100);
    expect(await token.balanceOf(addr1.address)).to.equal(100);
  });

  it("allows burning tokens", async function () {
    await token.burn(100);
    expect(await token.balanceOf(owner.address)).to.equal(
      INITIAL_SUPPLY - 100n
    );
  });

  it("allows pausing and blocks transfers", async function () {
    await token.pause();
    await expect(
      token.transfer(addr1.address, 100)
    ).to.be.revertedWithCustomError(token, "EnforcedPause");
  });

  it("allows unpausing and resuming transfers", async function () {
    await token.pause();
    await token.unpause();
    await token.transfer(addr1.address, 100);
    expect(await token.balanceOf(addr1.address)).to.equal(100);
  });

  // ===== Mint tests =====

  it("allows owner to mint before minting is finished", async function () {
    await token.mint(addr1.address, 1000);
    expect(await token.balanceOf(addr1.address)).to.equal(1000);
  });

  it("prevents non-owner from minting", async function () {
    await expect(
      token.connect(addr1).mint(addr1.address, 1000)
    ).to.be.revertedWithCustomError(token, "OwnableUnauthorizedAccount");
  });

  it("allows owner to finish minting", async function () {
    await token.finishMinting();
    expect(await token.mintingFinished()).to.equal(true);
  });

  it("prevents minting after minting is finished", async function () {
    await token.finishMinting();
    await expect(
      token.mint(addr1.address, 1000)
    ).to.be.revertedWith("Minting is finished");
  });

  it("prevents finishing minting twice", async function () {
    await token.finishMinting();
    await expect(
      token.finishMinting()
    ).to.be.revertedWith("Minting already finished");
  });

  it("total supply remains constant after minting is finished", async function () {
    const supplyBefore = await token.totalSupply();
    await token.finishMinting();

    await expect(
      token.mint(owner.address, 1000)
    ).to.be.reverted;

    const supplyAfter = await token.totalSupply();
    expect(supplyAfter).to.equal(supplyBefore);
  });
});

