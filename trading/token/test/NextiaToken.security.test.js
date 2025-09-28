const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("NextiaToken Security Tests 🔒", function () {
  let NextiaToken, token, owner, addr1, addr2;

beforeEach(async function () {
  [owner, addr1, addr2, addr3] = await ethers.getSigners();
  Token = await ethers.getContractFactory("NextiaToken");
  token = await Token.deploy(
    ethers.parseUnits("1000000", 18), // supply inicial
    owner.address                     // dueño inicial
  );
  if (token.waitForDeployment) await token.waitForDeployment();
});

  // --- Eventos ---
  it("Debe emitir evento Transfer al transferir tokens", async function () {
    await expect(token.transfer(addr1.address, 100))
      .to.emit(token, "Transfer")
      .withArgs(owner.address, addr1.address, 100n);
  });

  it("Debe emitir evento Approval al aprobar allowance", async function () {
    await expect(token.approve(addr1.address, 200))
      .to.emit(token, "Approval")
      .withArgs(owner.address, addr1.address, 200n);
  });

  it("Debe emitir evento Transfer al hacer mint", async function () {
    await expect(token.mint(owner.address, 500))
      .to.emit(token, "Transfer")
      .withArgs(ethers.ZeroAddress, owner.address, 500n);
  });

  it("Debe emitir evento Transfer al quemar tokens", async function () {
    await token.transfer(addr1.address, 100);
    await expect(token.connect(addr1).burn(50))
      .to.emit(token, "Transfer")
      .withArgs(addr1.address, ethers.ZeroAddress, 50n);
  });

  // --- Roles / Seguridad ---
  it("Solo el owner puede pausar", async function () {
    await expect(token.connect(addr1).pause()).to.be.reverted;
    await expect(token.connect(owner).pause()).to.not.be.reverted;
  });

  it("Solo el owner puede despausar", async function () {
    await token.pause();
    await expect(token.connect(addr1).unpause()).to.be.reverted;
    await expect(token.connect(owner).unpause()).to.not.be.reverted;
  });

  it("Solo el owner puede mintear", async function () {
    await expect(token.connect(addr1).mint(addr1.address, 1000)).to.be.reverted;
    await expect(token.mint(owner.address, 1000)).to.not.be.reverted;
  });

  // --- Edge cases extremos ---
  it("No debe permitir transferir más de lo que se tiene", async function () {
    await expect(token.connect(addr1).transfer(addr2.address, 100)).to.be.reverted;
  });

  it("No debe permitir burn mayor al balance", async function () {
    await token.transfer(addr1.address, 100);
    await expect(token.connect(addr1).burn(200)).to.be.reverted;
  });

  it("Debe fallar transferencias gigantes que excedan uint256", async function () {
    const bigAmount = ethers.MaxUint256;
    await expect(token.transfer(addr1.address, bigAmount)).to.be.reverted;
  });

  it("Debe fallar si se intenta transferir cuando el contrato está pausado", async function () {
    await token.pause();
    await expect(token.transfer(addr1.address, 100)).to.be.reverted;
  });

  it("Debe fallar si se intenta aprobar allowance estando pausado", async function () {
    await token.pause();
    await expect(token.approve(addr1.address, 100)).to.be.reverted;
  });

  it("Debe fallar transferFrom cuando está pausado", async function () {
    await token.approve(addr1.address, 100);
    await token.pause();
    await expect(
      token.connect(addr1).transferFrom(owner.address, addr2.address, 50)
    ).to.be.reverted;
  });
});
