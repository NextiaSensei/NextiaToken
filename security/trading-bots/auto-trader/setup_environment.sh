#!/bin/bash
# Nextia Trading Bot - Environment Setup Script

echo "🚀 Nextia Trading Bot - Environment Setup"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the auto-trader directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running system tests..."
python tests/test_setup.py

# Display next steps
echo ""
echo "🎯 NEXT STEPS:"
echo "   1. Configure your API keys in .env file"
echo "   2. Customize bot settings in configs/bot_config.json"
echo "   3. Run tests again to verify everything works"
echo ""
echo "💡 TIP: Always activate the virtual environment first:"
echo "      source venv/bin/activate"
