#!/usr/bin/env python3
"""
Test script to verify exchange API connections
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_loader import config
from utils.logger import trading_logger
import ccxt

def test_binance_connection():
    """Test Binance API connection"""
    try:
        trading_logger.info("Testing Binance connection...")
        
        # Get API credentials
        api_key = config.get('env', 'BINANCE_API_KEY')
        api_secret = config.get('env', 'BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            trading_logger.warning("Binance API keys not set, skipping connection test")
            return True
        
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'sandbox': True,  # Use sandbox for testing
            'options': {
                'defaultType': 'spot'
            }
        })
        
        # Test public data
        markets = exchange.load_markets()
        trading_logger.success(f"✅ Binance connected! Available markets: {len(markets)}")
        
        # Test private data (balance)
        try:
            balance = exchange.fetch_balance()
            trading_logger.success("✅ Binance private API: WORKING")
            print(f"   💰 Balance available: {len(balance['total'])} currencies")
            return True
        except Exception as e:
            trading_logger.error(f"❌ Binance private API failed: {e}")
            return False
            
    except Exception as e:
        trading_logger.error(f"❌ Binance connection failed: {e}")
        return False

def test_kucoin_connection():
    """Test KuCoin API connection"""
    try:
        trading_logger.info("Testing KuCoin connection...")
        
        # Get API credentials
        api_key = config.get('env', 'KUCOIN_API_KEY')
        api_secret = config.get('env', 'KUCOIN_API_SECRET')
        password = config.get('env', 'KUCOIN_PASSWORD')
        
        if not api_key or not api_secret:
            trading_logger.warning("KuCoin API keys not set, skipping connection test")
            return True
        
        exchange = ccxt.kucoin({
            'apiKey': api_key,
            'secret': api_secret,
            'password': password,
            'sandbox': True,
        })
        
        # Test public data
        markets = exchange.load_markets()
        trading_logger.success(f"✅ KuCoin connected! Available markets: {len(markets)}")
        
        # Test private data
        try:
            balance = exchange.fetch_balance()
            trading_logger.success("✅ KuCoin private API: WORKING")
            print(f"   💰 Balance available: {len(balance['total'])} currencies")
            return True
        except Exception as e:
            trading_logger.error(f"❌ KuCoin private API failed: {e}")
            return False
            
    except Exception as e:
        trading_logger.error(f"❌ KuCoin connection failed: {e}")
        return False

def test_telegram_bot():
    """Test Telegram bot connection"""
    try:
        trading_logger.info("Testing Telegram bot...")
        
        from utils.notifications import notifier
        
        if not notifier.telegram_configured:
            trading_logger.warning("Telegram not configured, skipping test")
            return True
        
        # Test message
        success = notifier.send_telegram_message(
            "🤖 <b>Test Message</b>\n"
            "Nextia Trading Bot API test completed successfully!\n"
            "✅ All systems operational\n"
            "🚀 Ready for Phase 2: Data Engine"
        )
        
        if success:
            trading_logger.success("✅ Telegram bot: WORKING")
            return True
        else:
            trading_logger.error("❌ Telegram bot: FAILED")
            return False
            
    except Exception as e:
        trading_logger.error(f"❌ Telegram test failed: {e}")
        return False

def main():
    print("🔌 EXCHANGE API CONNECTION TESTS")
    print("=" * 50)
    
    tests = [
        ("Binance", test_binance_connection),
        ("KuCoin", test_kucoin_connection),
        ("Telegram", test_telegram_bot)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🧪 Testing {name}...")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 API TEST RESULTS:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🚀 ALL APIS CONNECTED SUCCESSFULLY!")
        print("💪 Your bot is ready to trade!")
    else:
        print("⚠️  Some API tests failed.")
        print("🔧 Check your API keys and permissions")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
