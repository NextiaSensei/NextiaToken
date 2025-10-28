# test_new_modules.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

from profit_manager import ProfitManager
from session_scheduler import SessionScheduler
import json

def test_profit_manager():
    print("🧪 Testing ProfitManager...")
    pm = ProfitManager('config/trading_sessions.json')
    
    # Test profit target
    btc_entry = 50000
    btc_current = 51250  # 2.5% profit
    result = pm.check_profit_target('BTCUSDT', btc_current, btc_entry)
    print(f"BTC Profit Target (2.5%): {result} - Expected: True")
    
    # Test stop loss
    btc_current_loss = 49250  # 1.5% loss
    result = pm.check_stop_loss('BTCUSDT', btc_current_loss, btc_entry)
    print(f"BTC Stop Loss (1.5%): {result} - Expected: True")
    
    # Test position close logic
    should_close = pm.should_close_position('BTCUSDT', btc_current, btc_entry, 'long')
    print(f"Should close BTC position: {should_close}")

def test_session_scheduler():
    print("\n🧪 Testing SessionScheduler...")
    ss = SessionScheduler('config/trading_sessions.json')
    
    # Test session checking
    is_active = ss.is_session_active()
    print(f"Trading session active: {is_active}")
    
    # Test time parsing
    test_time = ss.parse_time("14:30")
    print(f"Parsed time 14:30: {test_time}")

def test_config_file():
    print("\n📋 Testing config file...")
    try:
        with open('config/trading_sessions.json', 'r') as f:
            config = json.load(f)
            print("✅ Config file loaded successfully")
            print(f"Profit targets: {list(config['profit_targets'].keys())}")
            print(f"Trading sessions: {len(config['trading_sessions'])}")
    except Exception as e:
        print(f"❌ Error loading config: {e}")

if __name__ == "__main__":
    print("🚀 TESTING NEW MODULES...\n")
    test_config_file()
    test_profit_manager() 
    test_session_scheduler()
    print("\n✅ All tests completed!")
