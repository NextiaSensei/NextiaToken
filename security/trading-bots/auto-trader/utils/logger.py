import logging
import sys
from datetime import datetime
import os

class TradingLogger:
    def __init__(self):
        self.setup_directories()
        self.setup_logger()
    
    def setup_directories(self):
        """Create necessary directories"""
        directories = ['logs', 'data', 'configs']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"📁 Created directory: {directory}")
    
    def setup_logger(self):
        """Setup comprehensive logging system"""
        
        # Create logger
        self.logger = logging.getLogger('nextia_trading_bot')
        self.logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler (detailed)
        file_handler = logging.FileHandler('logs/trading_bot.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler (simple)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Info level logging"""
        self.logger.info(message)
    
    def warning(self, message):
        """Warning level logging"""
        self.logger.warning(f"⚠️  {message}")
    
    def error(self, message):
        """Error level logging"""
        self.logger.error(f"❌ {message}")
    
    def success(self, message):
        """Success level logging"""
        self.logger.info(f"✅ {message}")
    
    def trade_signal(self, symbol, signal, price, reason):
        """Log trade signals"""
        self.logger.info(f"🎯 TRADE SIGNAL - {symbol} | {signal} | ${price:.2f} | {reason}")
    
    def market_data(self, symbol, price, change):
        """Log market data updates"""
        self.logger.info(f"📊 MARKET - {symbol}: ${price:.2f} ({change:+.2f}%)")

# Global logger instance
trading_logger = TradingLogger()
