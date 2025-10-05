const { execSync } = require("child_process");

function run(cmd){
  console.log("\n$ " + cmd);
  execSync(cmd, { stdio: "inherit" });
}

try {
  run("npx hardhat compile");
  run("npx hardhat test");
  run("REPORT_GAS=true npx hardhat test");
  run("npx hardhat coverage");
  console.log("📌 Para desplegar manualmente: npx hardhat run scripts/deploy.js --network sepolia");
} catch (e) {
  console.error("Error:", e.message);
  process.exit(1);
}
