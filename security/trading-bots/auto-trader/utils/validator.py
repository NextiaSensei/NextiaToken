import re
import numbers
from .logger import trading_logger

class TradingValidator:
    def __init__(self):
        self.supported_symbols = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'DOT/USDT', 'LINK/USDT']
        self.supported_timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
    
    def validate_symbol(self, symbol):
        """Validate trading symbol format and support"""
        if not isinstance(symbol, str):
            trading_logger.error(f"Symbol must be string, got {type(symbol)}")
            return False
        
        # Basic format validation
        pattern = r'^[A-Za-z0-9]+/[A-Za-z0-9]+$'
        if not re.match(pattern, symbol):
            trading_logger.error(f"Invalid symbol format: {symbol}")
            return False
        
        # Check if symbol is supported
        if symbol not in self.supported_symbols:
            trading_logger.warning(f"Symbol {symbol} not in supported list, but format is valid")
            # We don't return False here as we might want to support custom symbols
        
        trading_logger.info(f"Symbol validation passed: {symbol}")
        return True
    
    def validate_amount(self, amount, symbol=None, min_amount=0.0001):
        """Validate trade amount"""
        if not isinstance(amount, numbers.Number):
            trading_logger.error(f"Amount must be numeric, got {type(amount)}")
            return False
        
        if amount < min_amount:
            trading_logger.error(f"Amount too small: {amount} (min: {min_amount})")
            return False
        
        # Symbol-specific validation could be added here
        if symbol == 'BTC/USDT' and amount < 0.0001:
            trading_logger.warning("BTC amount seems very small")
        
        trading_logger.info(f"Amount validation passed: {amount} {symbol if symbol else ''}")
        return True
    
    def validate_price(self, price, min_price=0.000001):
        """Validate price value"""
        if not isinstance(price, numbers.Number):
            trading_logger.error(f"Price must be numeric, got {type(price)}")
            return False
        
        if price <= min_price:
            trading_logger.error(f"Price too low: {price} (min: {min_price})")
            return False
        
        return True
    
    def validate_percentage(self, value, max_value=1.0, min_value=0.0):
        """Validate percentage values (0-1 by default)"""
        if not isinstance(value, numbers.Number):
            trading_logger.error(f"Percentage must be numeric, got {type(value)}")
            return False
        
        if not min_value <= value <= max_value:
            trading_logger.error(f"Percentage out of range: {value} (allowed: {min_value}-{max_value})")
            return False
        
        return True
    
    def validate_timeframe(self, timeframe):
        """Validate trading timeframe"""
        if timeframe not in self.supported_timeframes:
            trading_logger.error(f"Unsupported timeframe: {timeframe}. Supported: {self.supported_timeframes}")
            return False
        return True
    
    def validate_api_credentials(self, exchange, api_key, api_secret):
        """Validate API credentials format"""
        if not api_key or not api_secret:
            trading_logger.error(f"{exchange}: API key or secret is empty")
            return False
        
        if len(api_key) < 10 or len(api_secret) < 10:
            trading_logger.error(f"{exchange}: API key or secret too short")
            return False
        
        # Basic format validation for Binance
        if exchange.lower() == 'binance':
            if not api_key.startswith('binance-') and len(api_key) != 64:
                trading_logger.warning("Binance API key format might be incorrect")
        
        trading_logger.info(f"{exchange} API credentials validation passed")
        return True
    
    def validate_trade_signal(self, signal_data):
        """Validate complete trade signal"""
        required_fields = ['symbol', 'signal', 'price', 'reason']
        
        for field in required_fields:
            if field not in signal_data:
                trading_logger.error(f"Missing required field in trade signal: {field}")
                return False
        
        if not self.validate_symbol(signal_data['symbol']):
            return False
        
        if signal_data['signal'] not in ['BUY', 'SELL', 'HOLD']:
            trading_logger.error(f"Invalid signal type: {signal_data['signal']}")
            return False
        
        if not self.validate_price(signal_data['price']):
            return False
        
        trading_logger.success(f"Trade signal validation passed: {signal_data['symbol']} - {signal_data['signal']}")
        return True

# Global validator instance
validator = TradingValidator()
