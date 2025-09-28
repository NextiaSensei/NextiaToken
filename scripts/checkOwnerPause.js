const hre = require("hardhat");

async function main() {
  const address = process.argv[2];
  if(!address) { console.error("Usage: node checkOwnerPause.js <contractAddress>"); process.exit(1); }

  const Nextia = await hre.ethers.getContractFactory("NextiaToken");
  const token = await Nextia.attach(address);

  // chequea si ABI tiene pause
  try {
    token.interface.getFunction("pause");
    console.log("ABI: pause() FOUND");
  } catch { console.log("ABI: pause() NOT FOUND"); }

  try {
    token.interface.getFunction("unpause");
    console.log("ABI: unpause() FOUND");
  } catch { console.log("ABI: unpause() NOT FOUND"); }

  // chequea owner() si existe
  try {
    const o = await token.owner();
    console.log("owner():", o);
  } catch (e) {
    console.log("owner() call failed:", e.message);
  }
}
main().catch(e=>{ console.error(e); process.exit(1); });
