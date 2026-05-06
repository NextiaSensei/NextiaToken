const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Governance Contract", function () {
  let nxtToken, governance, owner, addr1, addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    
    const NextiaToken = await ethers.getContractFactory("NextiaToken");
    nxtToken = await NextiaToken.deploy(ethers.parseEther("1000000"), owner.address);
    await nxtToken.waitForDeployment();

    const Governance = await ethers.getContractFactory("Governance");
    governance = await Governance.deploy(nxtToken.target, owner.address);
    await governance.waitForDeployment();

    // Transferir tokens a addr1 para que pueda proponer
    await nxtToken.transfer(addr1.address, ethers.parseEther("2000"));
    
    // addr2 NO recibe tokens, así tendrá saldo insuficiente
  });

  it("allows eligible user to propose", async function () {
    await governance.connect(addr1).proposeGovernanceChange("Increase APY");
    const count = await governance.proposalCount();
    expect(count).to.equal(1);
  });

  it("rejects proposal if user has insufficient tokens", async function () {
    // addr2 no tiene tokens, debería fallar
    await expect(
      governance.connect(addr2).proposeGovernanceChange("Bad Proposal")
    ).to.be.revertedWith("Insufficient NXT");
  });

  it("allows voting on proposal", async function () {
    await governance.connect(addr1).proposeGovernanceChange("Test Proposal");
    await governance.connect(addr1).castVote(0, 1);
    const info = await governance.getProposalInfo(0);
    expect(info[2]).to.be.gt(0); // forVotes > 0
  });

  it("rejects voting if user already voted", async function () {
    await governance.connect(addr1).proposeGovernanceChange("Test Proposal");
    await governance.connect(addr1).castVote(0, 1);
    
    // Intentar votar de nuevo debería fallar
    await expect(
      governance.connect(addr1).castVote(0, 0)
    ).to.be.revertedWith("Already voted");
  });

  it("allows voting against proposal", async function () {
    await governance.connect(addr1).proposeGovernanceChange("Test Proposal");
    await governance.connect(addr1).castVote(0, 0); // 0 = against
    const info = await governance.getProposalInfo(0);
    expect(info[3]).to.be.gt(0); // againstVotes > 0
  });
});

