const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Staking Contract", function () {
  let nxtToken, staking, owner, addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const NextiaToken = await ethers.getContractFactory("NextiaToken");
    nxtToken = await NextiaToken.deploy(ethers.parseEther("1000000"), owner.address);

    const Staking = await ethers.getContractFactory("Staking");
    staking = await Staking.deploy(nxtToken.target, owner.address);

    await nxtToken.transfer(addr1.address, ethers.parseEther("1000"));
    await nxtToken.transfer(staking.target, ethers.parseEther("500000"));
  });

  it("Should deposit NXT", async function () {
    const amount = ethers.parseEther("100");
    await nxtToken.connect(addr1).approve(staking.target, amount);
    await staking.connect(addr1).deposit(amount);
    expect(await staking.getStakedAmount(addr1.address)).to.equal(amount);
  });

  it("Should fail deposit with 0", async function () {
    await expect(staking.connect(addr1).deposit(0)).to.be.revertedWith("Amount > 0");
  });

  it("Should withdraw", async function () {
    const amount = ethers.parseEther("100");
    await nxtToken.connect(addr1).approve(staking.target, amount);
    await staking.connect(addr1).deposit(amount);
    await staking.connect(addr1).withdraw(ethers.parseEther("50"));
    expect(await staking.getStakedAmount(addr1.address)).to.equal(ethers.parseEther("50"));
  });
});
