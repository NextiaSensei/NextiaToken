require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();
require("hardhat-gas-reporter");
require("solidity-coverage");

const {
  ALCHEMY_API_KEY,
  PRIVATE_KEY_TEST,
  PRIVATE_KEY_MAIN,
  ETHERSCAN_API_KEY,
  COINMARKETCAP_API_KEY
} = process.env;

module.exports = {
  defaultNetwork: "hardhat",
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: { enabled: true, runs: 200 }
    }
  },
  networks: {
    hardhat: {},
    localhost: { url: "http://127.0.0.1:8545" },
    sepolia: {
      url: `https://eth-sepolia.g.alchemy.com/v2/${ALCHEMY_API_KEY}`,
      accounts: PRIVATE_KEY_TEST ? [PRIVATE_KEY_TEST] : []
    },
    mainnet: {
      url: `https://eth-mainnet.g.alchemy.com/v2/${ALCHEMY_API_KEY}`,
      accounts: PRIVATE_KEY_MAIN ? [PRIVATE_KEY_MAIN] : []
    }
  },
  etherscan: {
    apiKey: ETHERSCAN_API_KEY || ""
  },
  gasReporter: {
    enabled: true,
    currency: "USD",
    coinmarketcap: COINMARKETCAP_API_KEY || "",
    outputFile: "gas-report.html",
    noColors: true,
    showTimeSpent: true,
    reportFormats: ["txt", "html"],
    gasPriceApi: `https://api.etherscan.io/api?module=proxy&action=eth_gasPrice&apikey=${ETHERSCAN_API_KEY}`
  },
  mocha: {
    timeout: 20000,
    reporter: "mochawesome",
    reporterOptions: {
      reportDir: "reports",
      reportFilename: "index",
      quiet: true,
      overwrite: true,
      html: true,
      json: true
    }
  }
};


