import json
import os
from dotenv import load_dotenv
from .logger import trading_logger

# Load environment variables
load_dotenv()

class ConfigLoader:
    def __init__(self):
        self.configs = {}
        self.load_all_configs()
    
    def load_all_configs(self):
        """Load all configuration files"""
        try:
            # Load bot configuration
            self.load_bot_config()
            
            # Load exchanges configuration
            self.load_exchanges_config()
            
            # Load environment variables
            self.load_environment_vars()
            
            trading_logger.success("All configurations loaded successfully")
            
        except Exception as e:
            trading_logger.error(f"Failed to load configurations: {e}")
            raise
    
    def load_bot_config(self):
        """Load bot configuration"""
        config_path = 'configs/bot_config.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.configs['bot'] = json.load(f)
            trading_logger.success("Bot config loaded")
        else:
            trading_logger.warning("Bot config file not found, using defaults")
            self.configs['bot'] = self.get_default_bot_config()
    
    def load_exchanges_config(self):
        """Load exchanges configuration"""
        config_path = 'configs/exchanges.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.configs['exchanges'] = json.load(f)
            trading_logger.success("Exchanges config loaded")
        else:
            trading_logger.warning("Exchanges config file not found, using defaults")
            self.configs['exchanges'] = self.get_default_exchanges_config()
    
    def load_environment_vars(self):
        """Load environment variables"""
        self.configs['env'] = {
            'BINANCE_API_KEY': os.getenv('BINANCE_API_KEY', ''),
            'BINANCE_API_SECRET': os.getenv('BINANCE_API_SECRET', ''),
            'KUCOIN_API_KEY': os.getenv('KUCOIN_API_KEY', ''),
            'KUCOIN_API_SECRET': os.getenv('KUCOIN_API_SECRET', ''),
            'KUCOIN_PASSWORD': os.getenv('KUCOIN_PASSWORD', ''),
            'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
            'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', '')
        }
        
        # Check if essential API keys are present
        if not self.configs['env']['BINANCE_API_KEY']:
            trading_logger.warning("Binance API key not found in environment variables")
    
    def get_default_bot_config(self):
        """Default bot configuration"""
        return {
            "exchange": "binance",
            "initial_capital": 1000,
            "max_position_size": 0.1,
            "max_daily_loss": 0.05,
            "stop_loss_pct": 0.02,
            "take_profit_pct": 0.04,
            "symbols": ["BTC/USDT", "ETH/USDT", "ADA/USDT"],
            "strategy": "mean_reversion",
            "timeframe": "5m",
            "test_mode": True
        }
    
    def get_default_exchanges_config(self):
        """Default exchanges configuration"""
        return {
            "binance": {
                "api_key": "",
                "api_secret": "",
                "sandbox": True,
                "rate_limit": 1200
            },
            "kucoin": {
                "api_key": "",
                "api_secret": "",
                "password": "",
                "sandbox": True
            }
        }
    
    def get(self, section, key=None):
        """Get configuration value"""
        if section not in self.configs:
            trading_logger.error(f"Config section not found: {section}")
            return None
        
        if key:
            return self.configs[section].get(key)
        return self.configs[section]
    
    def update(self, section, key, value):
        """Update configuration value"""
        if section in self.configs:
            self.configs[section][key] = value
            trading_logger.info(f"Updated config: {section}.{key} = {value}")
        else:
            trading_logger.error(f"Cannot update, section not found: {section}")
    
    def save_bot_config(self):
        """Save bot configuration to file"""
        try:
            with open('configs/bot_config.json', 'w') as f:
                json.dump(self.configs['bot'], f, indent=4)
            trading_logger.success("Bot config saved to file")
            return True
        except Exception as e:
            trading_logger.error(f"Failed to save bot config: {e}")
            return False

# Global config instance
config = ConfigLoader()
