import requests
import json
from .config_loader import config
from .logger import trading_logger

class NotificationManager:
    def __init__(self):
        self.telegram_configured = self.check_telegram_config()
        
        if self.telegram_configured:
            trading_logger.success("Telegram notifications configured")
        else:
            trading_logger.warning("Telegram notifications not configured")
    
    def check_telegram_config(self):
        """Check if Telegram is properly configured"""
        token = config.get('env', 'TELEGRAM_BOT_TOKEN')
        chat_id = config.get('env', 'TELEGRAM_CHAT_ID')
        return bool(token and chat_id)
    
    def send_telegram_message(self, message, parse_mode='HTML'):
        """Send message via Telegram bot"""
        if not self.telegram_configured:
            trading_logger.warning("Telegram not configured, skipping message")
            return False
        
        try:
            token = config.get('env', 'TELEGRAM_BOT_TOKEN')
            chat_id = config.get('env', 'TELEGRAM_CHAT_ID')
            
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                trading_logger.info("Telegram message sent successfully")
                return True
            else:
                trading_logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            trading_logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def send_trade_signal(self, symbol, signal, price, reason, confidence=None):
        """Send trade signal notification"""
        confidence_text = f" | Confidence: {confidence}%" if confidence else ""
        
        message = f"""
🚨 <b>TRADE SIGNAL DETECTED</b> 🚨

💱 <b>Symbol:</b> <code>{symbol}</code>
📊 <b>Signal:</b> <b>{signal}</b>
💰 <b>Current Price:</b> <code>${price:.2f}</code>
📝 <b>Reason:</b> {reason}{confidence_text}

⏰ <i>Nextia Trading Bot - Automated System</i>
        """
        return self.send_telegram_message(message)
    
    def send_order_execution(self, symbol, side, quantity, price, order_id):
        """Send order execution notification"""
        message = f"""
✅ <b>ORDER EXECUTED</b> ✅

💱 <b>Symbol:</b> <code>{symbol}</code>
📈 <b>Action:</b> <b>{side.upper()}</b>
📦 <b>Quantity:</b> <code>{quantity:.6f}</code>
💰 <b>Price:</b> <code>${price:.2f}</code>
🆔 <b>Order ID:</b> <code>{order_id}</code>

⚡ <i>Nextia Trading Bot - Live Trading</i>
        """
        return self.send_telegram_message(message)
    
    def send_error_alert(self, error_message, context=None):
        """Send error alert"""
        context_text = f"\n🔧 <b>Context:</b> {context}" if context else ""
        
        message = f"""
❌ <b>SYSTEM ERROR ALERT</b> ❌

🚨 <b>Error Message:</b>
<code>{error_message}</code>{context_text}

🆘 <i>Nextia Trading Bot - Requires Immediate Attention</i>
        """
        return self.send_telegram_message(message)
    
    def send_system_status(self, status_data):
        """Send system status update"""
        message = f"""
📊 <b>SYSTEM STATUS UPDATE</b> 📊

🔄 <b>Bot Status:</b> <code>{status_data.get('status', 'Unknown')}</code>
💼 <b>Portfolio Value:</b> <code>${status_data.get('portfolio_value', 0):.2f}</code>
📈 <b>Active Trades:</b> <code>{status_data.get('active_trades', 0)}</code>
📉 <b>Today's P&L:</b> <code>${status_data.get('daily_pnl', 0):.2f}</code>

🖥️ <i>Nextia Trading Bot - Status Report</i>
        """
        return self.send_telegram_message(message)

# Global notification instance
notifier = NotificationManager()
