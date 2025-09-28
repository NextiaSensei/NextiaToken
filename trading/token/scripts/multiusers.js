// scripts/multiusers.js
require("dotenv").config();
const hre = require("hardhat");
const ethers = hre.ethers;
const fs = require("fs");
const path = require("path");

function getDeployment() {
  const filePath = path.join(__dirname, "..", "deployments", "NextiaToken.json");
  if (!fs.existsSync(filePath)) throw new Error("deployments/NextiaToken.json no encontrado. Haz deploy primero.");
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

async function attachContract() {
  const deployment = getDeployment();
  const provider = ethers.provider;
  const signers = await ethers.getSigners(); // en localhost hay varios; en Sepolia normalmente 1 (si config. PRIVATE_KEY)

  // owner signer: preferir signers[0], si no crear Wallet desde PRIVATE_KEY
  let ownerSigner = signers && signers.length > 0 ? signers[0] : null;
  if (!ownerSigner) {
    if (!process.env.PRIVATE_KEY) throw new Error("No hay owner signer y PRIVATE_KEY no definida en .env");
    ownerSigner = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
  }

  // addr1 signer: preferir signers[1], si no crear Wallet desde TEST_WALLET_1_PRIVATE_KEY
  let addr1Signer = signers && signers.length > 1 ? signers[1] : null;
  if (!addr1Signer) {
    if (!process.env.TEST_WALLET_1_PRIVATE_KEY) throw new Error("No hay addr1 signer y TEST_WALLET_1_PRIVATE_KEY no definida en .env");
    addr1Signer = new ethers.Wallet(process.env.TEST_WALLET_1_PRIVATE_KEY, provider);
  }

  // addr2 signer: preferir signers[2], si no crear Wallet desde TEST_WALLET_2_PRIVATE_KEY
  let addr2Signer = signers && signers.length > 2 ? signers[2] : null;
  if (!addr2Signer) {
    if (!process.env.TEST_WALLET_2_PRIVATE_KEY) throw new Error("No hay addr2 signer y TEST_WALLET_2_PRIVATE_KEY no definida en .env");
    addr2Signer = new ethers.Wallet(process.env.TEST_WALLET_2_PRIVATE_KEY, provider);
  }

  // Contract object ligado al provider (use .connect(signer) para tx)
  const token = new ethers.Contract(deployment.address, deployment.abi, provider);

  return { token, ownerSigner, addr1Signer, addr2Signer, deployment };
}

async function main() {
  console.log("🔎 Multiuser flow - NextiaToken");
  const { token, ownerSigner, addr1Signer, addr2Signer, deployment } = await attachContract();

  const ownerAddress = await ownerSigner.getAddress();
  const addr1Address = await addr1Signer.getAddress();
  const addr2Address = await addr2Signer.getAddress();

  console.log("Contrato:", deployment.address, "Network:", hre.network.name);
  console.log("Owner:", ownerAddress);
  console.log("Addr1:", addr1Address);
  console.log("Addr2:", addr2Address);

  // 1) Balances iniciales
  const balOwner0 = await token.balanceOf(ownerAddress);
  console.log("Owner balance:", ethers.formatUnits(balOwner0, 18));

  // 2) Owner aprueba a addr1 para gastar 200 NXT
  const ownerToken = token.connect(ownerSigner);
  const approveAmount = ethers.parseUnits("200", 18);
  console.log(`-> Owner aprueba ${ethers.formatUnits(approveAmount,18)} NXT a addr1`);
  let tx = await ownerToken.approve(addr1Address, approveAmount);
  await tx.wait();
  console.log("  approve: mined");

  // 3) Ver allowance
  const allow = await token.allowance(ownerAddress, addr1Address);
  console.log("Allowance (owner -> addr1):", ethers.formatUnits(allow, 18));

  // 4) addr1 usa transferFrom para transferir 50 NXT de owner -> addr2
  const addr1Token = token.connect(addr1Signer);
  const transferFromAmount = ethers.parseUnits("50", 18);
  console.log(`-> addr1 transferFrom owner -> addr2 : ${ethers.formatUnits(transferFromAmount,18)} NXT`);
  tx = await addr1Token.transferFrom(ownerAddress, addr2Address, transferFromAmount);
  await tx.wait();
  console.log("  transferFrom: mined");

  // 5) Balances después
  console.log("Owner balance (post):", ethers.formatUnits(await token.balanceOf(ownerAddress), 18));
  console.log("Addr2 balance (post):", ethers.formatUnits(await token.balanceOf(addr2Address), 18));

  // 6) Probar pause: owner pausa y addr1 intenta transferFrom (debe fallar)
  console.log("-> owner pausar token...");
  await ownerToken.pause();
  try {
    tx = await addr1Token.transferFrom(ownerAddress, addr2Address, ethers.parseUnits("1", 18));
    await tx.wait();
    console.log("❌ ERROR: transferFrom tuvo éxito mientras pausado (no debería)");
  } catch (e) {
    console.log("✅ Transfer bloqueado mientras pausado (esperado). Error:", e.message.split("\n")[0]);
  }

  // 7) Unpause
  await ownerToken.unpause();
  console.log("-> owner despausa token");

  // 8) Final balances
  console.log("Final Owner:", ethers.formatUnits(await token.balanceOf(ownerAddress), 18));
  console.log("Final Addr2:", ethers.formatUnits(await token.balanceOf(addr2Address), 18));
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});

