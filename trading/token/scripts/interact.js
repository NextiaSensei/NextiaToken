const hre = require("hardhat");
const ethers = hre.ethers;
const fs = require("fs");
const path = require("path");

// 📂 Leer deployments/NextiaToken.json
function getDeployment() {
  const filePath = path.join(__dirname, "..", "deployments", "NextiaToken.json");
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

async function getContract() {
  const deployment = getDeployment();
  const [owner] = await ethers.getSigners();
  return new ethers.Contract(deployment.address, deployment.abi, owner);
}

async function main() {
  const [owner, addr1, addr2] = await ethers.getSigners();
  const token = await getContract();

  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case "balanceOf": {
      const who =
        args[1] === "owner"
          ? owner.address
          : args[1] === "addr1"
          ? addr1.address
          : addr2.address;

      const bal = await token.balanceOf(who);
      console.log(`Balance de ${args[1]}:`, ethers.formatUnits(bal, 18));
      break;
    }

    case "transfer": {
      const to = args[1] === "addr1" ? addr1.address : addr2.address;
      const amount = ethers.parseUnits(args[2], 18);
      const tx = await token.transfer(to, amount);
      await tx.wait();
      console.log(`✅ Transferidos ${args[2]} tokens a ${args[1]}`);
      break;
    }

    case "mint": {
      const mintAmount = ethers.parseUnits(args[1], 18);
      const tx = await token.mint(owner.address, mintAmount);
      await tx.wait();
      console.log(`✅ Mint ${args[1]} al owner`);
      break;
    }

    case "burn": {
      const burnAmount = ethers.parseUnits(args[1], 18);
      const tx = await token.connect(addr1).burn(burnAmount);
      await tx.wait();
      console.log(`🔥 Addr1 quemó ${args[1]}`);
      break;
    }

    case "pause":
      await token.pause();
      console.log("⏸️ Token pausado");
      break;

    case "unpause":
      await token.unpause();
      console.log("▶️ Token despausado");
      break;
      
          case "totalSupply": {
      const supply = await token.totalSupply();
      console.log(`🌍 Suministro total: ${ethers.formatUnits(supply, 18)} NXT`);
      break;
    }

    case "approve": {
      // spender puede ser "addr1" / "addr2" o una dirección completa
      const spenderArg = args[1];
      const spender =
        spenderArg === "addr1" ? addr1.address :
        spenderArg === "addr2" ? addr2.address :
        spenderArg; // si pasas una dirección directa

      if (!spender) {
        console.log("Uso: node scripts/interact.js approve [addr1|addr2|0xADDRESS] [cantidad]");
        break;
      }

      const amountStr = args[2];
      if (!amountStr) {
        console.log("Especifica la cantidad. Ej: approve addr1 100");
        break;
      }

      const amount = ethers.parseUnits(amountStr, 18);
      const tx = await token.approve(spender, amount);
      await tx.wait();
      console.log(`✅ Owner aprobó ${amountStr} NXT a ${spender}`);
      break;
    }

    case "allowance": {
      // ownerArg y spenderArg pueden ser owner/addr1/addr2 o direcciones
      const ownerArg = args[1];
      const spenderArg2 = args[2];

      const ownerAddr =
        ownerArg === "owner" ? owner.address :
        ownerArg === "addr1" ? addr1.address :
        ownerArg === "addr2" ? addr2.address :
        ownerArg;

      const spenderAddr =
        spenderArg2 === "owner" ? owner.address :
        spenderArg2 === "addr1" ? addr1.address :
        spenderArg2 === "addr2" ? addr2.address :
        spenderArg2;

      if (!ownerAddr || !spenderAddr) {
        console.log("Uso: node scripts/interact.js allowance [owner|addr1|addr2|0xOWNER] [addr1|addr2|0xSPENDER]");
        break;
      }

      const allow = await token.allowance(ownerAddr, spenderAddr);
      console.log(`📜 Allowance (${ownerAddr} → ${spenderAddr}): ${ethers.formatUnits(allow, 18)} NXT`);
      break;
    }


    case "test-suite": {
      console.log("🚀 Ejecutando test-suite...\n");

      let bOwner = await token.balanceOf(owner.address);
      console.log("Owner balance inicial:", ethers.formatUnits(bOwner, 18));

      const tx1 = await token.transfer(addr1.address, ethers.parseUnits("100", 18));
      await tx1.wait();
      console.log("✅ Transferidos 100 a addr1");

      let b1 = await token.balanceOf(addr1.address);
      console.log("Balance addr1:", ethers.formatUnits(b1, 18));

      const tx2 = await token.mint(owner.address, ethers.parseUnits("500", 18));
      await tx2.wait();
      console.log("✅ Mint 500 al owner");

      const tx3 = await token.connect(addr1).burn(ethers.parseUnits("50", 18));
      await tx3.wait();
      console.log("🔥 Addr1 quemó 50");

      await token.pause();
      console.log("⏸️ Token pausado");

      try {
        const tx4 = await token.transfer(addr2.address, ethers.parseUnits("1", 18));
        await tx4.wait();
        console.log("❌ ERROR: se transfirió mientras pausado");
      } catch {
        console.log("✅ Transfer bloqueado mientras pausado");
      }

      await token.unpause();
      console.log("▶️ Token despausado");

      const tx5 = await token.transfer(addr2.address, ethers.parseUnits("1", 18));
      await tx5.wait();
      console.log("✅ Transfer luego de unpause OK");

      let b2 = await token.balanceOf(addr2.address);
      console.log("Balance addr2:", ethers.formatUnits(b2, 18));
      break;
    }

    default:
      console.log("❓ Comando no reconocido. Usa:");
      console.log(" balanceOf [owner|addr1|addr2]");
      console.log(" transfer [addr1|addr2] [cantidad]");
      console.log(" mint [cantidad]");
      console.log(" burn [cantidad]");
      console.log(" pause");
      console.log(" unpause");
      console.log(" test-suite");
  }
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});

