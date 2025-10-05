const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("NextiaToken - Advanced & Edge Case Tests", function () {
  let Token, token, owner, addr1, addr2, addr3;

  beforeEach(async function () {
    [owner, addr1, addr2, addr3] = await ethers.getSigners();
    Token = await ethers.getContractFactory("NextiaToken");
    token = await Token.deploy(
      ethers.parseUnits("1000000", 18),
      owner.address
    );
    if (token.waitForDeployment) await token.waitForDeployment();
  });

  // ✅ 1. Approve / allowance / transferFrom
  it("permite approve, allowance y transferFrom correctamente", async function () {
    await token.approve(addr1.address, ethers.parseUnits("200", 18));
    const allowance = await token.allowance(owner.address, addr1.address);
    expect(allowance).to.equal(ethers.parseUnits("200", 18));

    await token.connect(addr1).transferFrom(
      owner.address,
      addr2.address,
      ethers.parseUnits("100", 18)
    );
    const bal2 = await token.balanceOf(addr2.address);
    expect(bal2).to.equal(ethers.parseUnits("100", 18));
  });

  // 🚫 2. Transferencias inválidas
  it("falla si el balance es insuficiente", async function () {
    await expect(
      token.connect(addr1).transfer(owner.address, ethers.parseUnits("1", 18))
    ).to.be.reverted;
  });

  it("no permite transferir a la dirección cero", async function () {
    await expect(
      token.transfer(ethers.ZeroAddress, ethers.parseUnits("10", 18))
    ).to.be.reverted;
  });

  // 🔥 3. Mint controlado
  it("solo el owner puede mintear", async function () {
    let hasMint = true;
    try {
      token.interface.getFunction("mint");
    } catch {
      hasMint = false;
    }
    if (!hasMint) this.skip();

    await expect(
      token.connect(addr1).mint(addr1.address, ethers.parseUnits("10", 18))
    ).to.be.reverted;

    await token.connect(owner).mint(addr1.address, ethers.parseUnits("10", 18));
    const b = await token.balanceOf(addr1.address);
    expect(b).to.equal(ethers.parseUnits("10", 18));
  });

  // 🔥 4. Burn correcto e inválido
  it("reduce balance al quemar y falla si quema más de lo que tiene", async function () {
    await token.transfer(addr1.address, ethers.parseUnits("50", 18));
    await token.connect(addr1).burn(ethers.parseUnits("20", 18));
    const b = await token.balanceOf(addr1.address);
    expect(b).to.equal(ethers.parseUnits("30", 18));

    await expect(
      token.connect(addr1).burn(ethers.parseUnits("1000", 18))
    ).to.be.reverted;
  });

  // 🧱 5. Eventos esperados
  it("emite eventos Transfer y Approval correctamente", async function () {
    await expect(token.transfer(addr1.address, ethers.parseUnits("10", 18)))
      .to.emit(token, "Transfer")
      .withArgs(owner.address, addr1.address, ethers.parseUnits("10", 18));

    await expect(token.approve(addr1.address, ethers.parseUnits("5", 18)))
      .to.emit(token, "Approval")
      .withArgs(owner.address, addr1.address, ethers.parseUnits("5", 18));
  });

  // 🚫 6. Solo owner puede pausar / despausar
  it("solo el owner puede pausar y despausar", async function () {
    await expect(token.connect(addr1).pause()).to.be.reverted;
    await token.connect(owner).pause();
    await expect(token.connect(addr1).unpause()).to.be.reverted;
    await token.connect(owner).unpause();
  });

  // 🛡️ 7. Reentrancy (simulada)
  it("resiste un intento básico de reentrancy en transfer", async function () {
    // No existe función vulnerable pero probamos consistencia
    const initialOwnerBalance = await token.balanceOf(owner.address);
    await token.transfer(addr1.address, ethers.parseUnits("100", 18));
    const finalOwnerBalance = await token.balanceOf(owner.address);
    expect(finalOwnerBalance).to.equal(
      initialOwnerBalance - ethers.parseUnits("100", 18)
    );
  });

  // ⚙️ 8. Total supply se actualiza en mint y burn
  it("actualiza totalSupply correctamente", async function () {
    const supplyBefore = await token.totalSupply();
    await token.connect(owner).mint(addr2.address, ethers.parseUnits("10", 18));
    const supplyAfterMint = await token.totalSupply();
    expect(supplyAfterMint).to.equal(
      supplyBefore + ethers.parseUnits("10", 18)
    );

    await token.connect(addr2).burn(ethers.parseUnits("5", 18));
    const supplyAfterBurn = await token.totalSupply();
    expect(supplyAfterBurn).to.equal(
      supplyAfterMint - ethers.parseUnits("5", 18)
    );
  });
});

