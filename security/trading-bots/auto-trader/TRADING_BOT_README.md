# 🚀 Nextia Trading Bot - Auto Trader

## 📋 Quick Start Guide

### 1. Initial Setup

# Run the setup script (first time only)
./setup_environment.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
2. Configure Your Environment
bash
# Edit the .env file with your API keys
# Use SANDBOX keys for testing!
nano .env

# Configure trading parameters
nano configs/bot_config.json
3. Run Tests

# Comprehensive system test
python tests/test_setup.py

# If all tests pass, you're ready!
4. Daily Usage
bash
# Always activate the virtual environment first
source venv/bin/activate

# Run tests to verify system
python tests/test_setup.py

# Proceed with development...
🏗️ Project Structure
text
auto-trader/
├── 🤖 core/                    # Trading engine components
├── 📊 data/                    # Market data handlers
├── 📈 strategies/              # Trading strategies
├── ⚙️ utils/                   # Utilities (logger, config, etc.)
├── 🔧 configs/                 # Configuration files
├── 📝 tests/                   # Test suites
├── 📊 logs/                    # Application logs
└── 📚 backtester/             # Backtesting engine
🔐 Security Notes
✅ Use SANDBOX API keys for development

✅ Never commit .env file to Git

✅ Enable 2FA on exchange accounts

✅ Use separate API keys for trading bot

✅ Regular security audits recommended

🆘 Troubleshooting
Virtual environment issues: Delete venv/ and rerun setup

Import errors: Check Python path and activate venv

API errors: Verify sandbox mode and key permissions

Test failures: Check error messages in logs/trading_bot.log

🎯 Next Phase: Data Engine
After successful setup, we'll build:

Real-time market data feeds

WebSocket connections to exchanges

Historical data collection

Data processing pipelines

Nextia Trading Ecosystem - Professional Grade Automated Trading
EOF
