const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("NextiaToken", function () {
  let Token, token, owner, addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();

    Token = await ethers.getContractFactory("NextiaToken");
    token = await Token.deploy(
      ethers.parseUnits("1000000", 18), // supply inicial
      owner.address                     // dueño inicial
    );
  });

  it("assigns initial supply to deployer (owner)", async function () {
    const ownerBalance = await token.balanceOf(owner.address);
    expect(ownerBalance).to.equal(ethers.parseUnits("1000000", 18));
  });

  it("allows transfers between accounts", async function () {
    await token.transfer(addr1.address, 100);
    const addr1Balance = await token.balanceOf(addr1.address);
    expect(addr1Balance).to.equal(100);
  });

  it("allows burning tokens", async function () {
    await token.burn(100);
    const balance = await token.balanceOf(owner.address);
    expect(balance).to.equal(ethers.parseUnits("1000000", 18) - 100n);
  });

  it("allows pausing and prevents transfers when paused", async function () {
    await token.connect(owner).pause();
    await expect(
  token.transfer(addr1.address, 100)
).to.be.revertedWithCustomError(token, "EnforcedPause");

  });

  it("allows unpausing and resuming transfers", async function () {
    await token.connect(owner).pause();
    await token.connect(owner).unpause();
    await token.transfer(addr1.address, 100);
    const addr1Balance = await token.balanceOf(addr1.address);
    expect(addr1Balance).to.equal(100);
  });
});

