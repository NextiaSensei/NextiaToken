# profit_manager.py
import json
import logging
from datetime import datetime

class ProfitManager:
    def __init__(self, config_path='config/trading_sessions.json'):
        self.config_path = config_path
        self.profit_targets = {}
        self.stop_losses = {}
        self.load_config()
        
    def load_config(self):
        """Carga la configuración de profit targets y stop losses"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.profit_targets = config.get('profit_targets', {})
                self.stop_losses = config.get('stop_losses', {})
            logging.info("ProfitManager config loaded successfully")
        except Exception as e:
            logging.error(f"Error loading ProfitManager config: {e}")
    
    def check_profit_target(self, symbol, current_price, entry_price):
        """Verifica si se alcanzó el profit target"""
        if symbol in self.profit_targets:
            target_percent = self.profit_targets[symbol]
            profit_percent = ((current_price - entry_price) / entry_price) * 100
            return profit_percent >= target_percent
        return False
    
    def check_stop_loss(self, symbol, current_price, entry_price):
        """Verifica si se activó el stop loss"""
        if symbol in self.stop_losses:
            stop_percent = self.stop_losses[symbol]
            loss_percent = ((entry_price - current_price) / entry_price) * 100
            return loss_percent >= stop_percent
        return False
    
    def should_close_position(self, symbol, current_price, entry_price, position_type):
        """Determina si cerrar posición por profit/stop"""
        if position_type == 'long':
            return (self.check_profit_target(symbol, current_price, entry_price) or 
                    self.check_stop_loss(symbol, current_price, entry_price))
        # Para short positions (invertir la lógica)
        elif position_type == 'short':
            return (self.check_profit_target(symbol, entry_price, current_price) or 
                    self.check_stop_loss(symbol, entry_price, current_price))
        return False
