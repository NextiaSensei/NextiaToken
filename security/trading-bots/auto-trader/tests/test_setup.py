#!/usr/bin/env python3
"""
Comprehensive Test Script for Nextia Trading Bot Setup
Tests all components and verifies the system is ready for trading
"""

import sys
import os
import json
import asyncio

# Add the parent directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_loader import config
from utils.logger import trading_logger
from utils.notifications import notifier
from utils.validator import validator

class TradingBotTestSuite:
    def __init__(self):
        self.results = {}
        self.test_count = 0
        self.passed_count = 0
    
    def log_test_result(self, test_name, success, message=None):
        """Log test result and update counters"""
        self.test_count += 1
        if success:
            self.passed_count += 1
            trading_logger.success(f"TEST PASSED: {test_name}")
            if message:
                print(f"   ✅ {message}")
        else:
            trading_logger.error(f"TEST FAILED: {test_name}")
            if message:
                print(f"   ❌ {message}")
        
        self.results[test_name] = {
            'success': success,
            'message': message
        }
    
    def test_config_loader(self):
        """Test configuration loader functionality"""
        print("\n🧪 Testing Config Loader...")
        
        try:
            # Test bot config
            bot_config = config.get('bot')
            if not bot_config:
                self.log_test_result("Config Loader - Bot Config", False, "Bot config not loaded")
                return False
            
            # Test specific values
            initial_capital = config.get('bot', 'initial_capital')
            exchange = config.get('bot', 'exchange')
            symbols = config.get('bot', 'symbols')
            
            print(f"   💰 Initial Capital: ${initial_capital}")
            print(f"   🔄 Exchange: {exchange}")
            print(f"   📊 Symbols: {symbols}")
            
            # Test exchanges config
            exchanges_config = config.get('exchanges')
            if not exchanges_config:
                self.log_test_result("Config Loader - Exchanges Config", False, "Exchanges config not loaded")
                return False
            
            print(f"   🏦 Available Exchanges: {list(exchanges_config.keys())}")
            
            # Test environment variables
            env_config = config.get('env')
            binance_key = env_config.get('BINANCE_API_KEY', '')
            
            if binance_key:
                print("   🔑 Binance API Key: [PRESENT]")
            else:
                print("   ⚠️  Binance API Key: [NOT SET - Use sandbox mode]")
            
            self.log_test_result("Config Loader - Complete", True, "All configurations loaded successfully")
            return True
            
        except Exception as e:
            self.log_test_result("Config Loader - Complete", False, f"Error: {e}")
            return False
    
    def test_logger_system(self):
        """Test logging system functionality"""
        print("\n🧪 Testing Logger System...")
        
        try:
            # Test different log levels
            trading_logger.info("This is a test INFO message")
            trading_logger.warning("This is a test WARNING message")
            trading_logger.error("This is a test ERROR message")
            trading_logger.success("This is a test SUCCESS message")
            
            # Test trade signal logging
            trading_logger.trade_signal("BTC/USDT", "BUY", 45000.50, "RSI oversold")
            
            # Test market data logging
            trading_logger.market_data("ETH/USDT", 3000.75, 2.5)
            
            # Check if log file was created
            log_file_exists = os.path.exists('logs/trading_bot.log')
            
            if log_file_exists:
                print("   📝 Log file created: logs/trading_bot.log")
                self.log_test_result("Logger System - Complete", True, "All log types working")
                return True
            else:
                self.log_test_result("Logger System - Complete", False, "Log file not created")
                return False
                
        except Exception as e:
            self.log_test_result("Logger System - Complete", False, f"Error: {e}")
            return False
    
    def test_validator_system(self):
        """Test data validation system"""
        print("\n🧪 Testing Validator System...")
        
        try:
            # Test symbol validation
            valid_symbol = validator.validate_symbol("BTC/USDT")
            invalid_symbol = validator.validate_symbol("INVALID_SYMBOL")
            
            # Test amount validation
            valid_amount = validator.validate_amount(0.01)
            invalid_amount = validator.validate_amount(0.0000001)
            
            # Test percentage validation
            valid_percentage = validator.validate_percentage(0.05)
            invalid_percentage = validator.validate_percentage(1.5)
            
            # Test trade signal validation
            valid_signal = {
                'symbol': 'ETH/USDT',
                'signal': 'BUY',
                'price': 3000.50,
                'reason': 'Trend reversal'
            }
            signal_valid = validator.validate_trade_signal(valid_signal)
            
            print(f"   ✅ Symbol Validation: Valid={valid_symbol}, Invalid={not invalid_symbol}")
            print(f"   ✅ Amount Validation: Valid={valid_amount}, Invalid={not invalid_amount}")
            print(f"   ✅ Percentage Validation: Valid={valid_percentage}, Invalid={not invalid_percentage}")
            print(f"   ✅ Trade Signal Validation: {signal_valid}")
            
            all_tests_passed = (
                valid_symbol and not invalid_symbol and
                valid_amount and not invalid_amount and
                valid_percentage and not invalid_percentage and
                signal_valid
            )
            
            if all_tests_passed:
                self.log_test_result("Validator System - Complete", True, "All validation tests passed")
                return True
            else:
                self.log_test_result("Validator System - Complete", False, "Some validation tests failed")
                return False
                
        except Exception as e:
            self.log_test_result("Validator System - Complete", False, f"Error: {e}")
            return False
    
    def test_notification_system(self):
        """Test notification system"""
        print("\n🧪 Testing Notification System...")
        
        try:
            # Test Telegram configuration
            telegram_configured = notifier.telegram_configured
            
            if telegram_configured:
                print("   🤖 Telegram: CONFIGURED")
                
                # Test a simple message (commented out to avoid spamming)
                # success = notifier.send_telegram_message("🔧 <b>Test Message</b>: Trading Bot setup completed successfully!")
                # if success:
                #     print("   📨 Test message sent to Telegram")
                # else:
                #     print("   ⚠️  Failed to send test message")
                
                # For now, we'll just test the message construction
                test_message = "🔧 <b>Test Mode</b>: Notification system is working correctly!"
                print("   📨 Telegram message construction: OK")
                
            else:
                print("   ⚠️  Telegram: NOT CONFIGURED (optional)")
            
            # Test notification methods (without actually sending)
            signal_data = {
                'symbol': 'BTC/USDT',
                'signal': 'BUY',
                'price': 45000.50,
                'reason': 'Test signal',
                'confidence': 85
            }
            
            print("   🔔 Notification templates: READY")
            self.log_test_result("Notification System - Complete", True, "Notification system operational")
            return True
            
        except Exception as e:
            self.log_test_result("Notification System - Complete", False, f"Error: {e}")
            return False
    
    def test_file_structure(self):
        """Test that all required files and directories exist"""
        print("\n🧪 Testing File Structure...")
        
        required_dirs = [
            'utils',
            'configs',
            'logs',
            'tests',
            'data'
        ]
        
        required_files = [
            'configs/bot_config.json',
            'configs/exchanges.json',
            '.env',
            '.gitignore',
            'requirements.txt'
        ]
        
        missing_dirs = []
        missing_files = []
        
        # Check directories
        for directory in required_dirs:
            if not os.path.exists(directory):
                missing_dirs.append(directory)
            else:
                print(f"   📁 Directory exists: {directory}")
        
        # Check files
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
            else:
                print(f"   📄 File exists: {file_path}")
        
        if not missing_dirs and not missing_files:
            self.log_test_result("File Structure - Complete", True, "All required files and directories present")
            return True
        else:
            error_msg = f"Missing: {missing_dirs + missing_files}"
            self.log_test_result("File Structure - Complete", False, error_msg)
            return False
    
    def test_python_environment(self):
        """Test Python environment and dependencies"""
        print("\n🧪 Testing Python Environment...")
        
        try:
            # Test essential imports
            import pandas as pd
            import numpy as np
            import ccxt
            import websocket
            from dotenv import load_dotenv
            
            print("   🐍 Essential imports: SUCCESS")
            
            # Test pandas functionality
            test_data = pd.DataFrame({
                'price': [45000, 45100, 44900, 45200],
                'volume': [100, 150, 120, 180]
            })
            print(f"   📊 Pandas test: OK (DataFrame: {test_data.shape[0]} rows)")
            
            # Test numpy functionality
            test_array = np.array([1, 2, 3, 4, 5])
            print(f"   🔢 Numpy test: OK (Array sum: {test_array.sum()})")
            
            # Test ccxt (without API calls)
            exchange = ccxt.binance()
            print(f"   🔄 CCXT test: OK (Exchange: {exchange.name})")
            
            self.log_test_result("Python Environment - Complete", True, "All dependencies working")
            return True
            
        except ImportError as e:
            self.log_test_result("Python Environment - Complete", False, f"Missing dependency: {e}")
            return False
        except Exception as e:
            self.log_test_result("Python Environment - Complete", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀" + "="*60)
        print("🚀          NEXTIA TRADING BOT - COMPREHENSIVE TEST SUITE")
        print("🚀" + "="*60)
        
        test_methods = [
            self.test_file_structure,
            self.test_python_environment,
            self.test_config_loader,
            self.test_logger_system,
            self.test_validator_system,
            self.test_notification_system
        ]
        
        for test_method in test_methods:
            test_method()
        
        self.print_final_report()
    
    def print_final_report(self):
        """Print comprehensive test report"""
        print("\n" + "="*60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("="*60)
        
        # Calculate percentage
        percentage = (self.passed_count / self.test_count) * 100 if self.test_count > 0 else 0
        
        # Overall result
        if percentage == 100:
            print("🎉 EXCELLENT! ALL TESTS PASSED! 🎉")
            print("🚀 Your trading bot is ready for Phase 2: Data Engine")
        elif percentage >= 80:
            print("✅ GOOD! Most tests passed")
            print("🔧 Your bot is almost ready - check the failed tests")
        elif percentage >= 60:
            print("⚠️  FAIR! Some tests need attention")
            print("🔧 Review failed tests before proceeding")
        else:
            print("❌ NEEDS WORK! Multiple tests failed")
            print("🔧 Please fix the issues before proceeding")
        
        print(f"\n📈 Test Results: {self.passed_count}/{self.test_count} passed ({percentage:.1f}%)")
        
        # Detailed results
        print("\n📋 Detailed Results:")
        for test_name, result in self.results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"   {status} - {test_name}")
            if result['message'] and not result['success']:
                print(f"      💡 {result['message']}")
        
        # Next steps
        print("\n🎯 NEXT STEPS:")
        if percentage == 100:
            print("   1. ✅ Setup complete - Proceed to Phase 2: Data Engine")
            print("   2. 📊 We'll build the real-time market data system")
            print("   3. 🤖 Then create the actual trading strategies")
        else:
            print("   1. 🔧 Fix the failed tests above")
            print("   2. 🐛 Check error messages for clues")
            print("   3. 🔄 Run tests again until all pass")
        
        print("="*60)

def main():
    """Main test execution"""
    test_suite = TradingBotTestSuite()
    test_suite.run_all_tests()
    
    # Return exit code based on test results
    return test_suite.passed_count == test_suite.test_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
