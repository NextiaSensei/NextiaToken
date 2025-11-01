import logging
from collections import deque

logger = logging.getLogger(__name__)

class KillSwitch:
    def __init__(self, config):
        self.daily_loss_limit = config['daily_loss_limit']  # 2%
        self.max_drawdown = config['max_drawdown']  # 5%
        self.daily_starting_balance = None
        self.peak_balance = None
        
    def update_balance(self, current_balance):
        """Actualizar balance y verificar drawdown"""
        if self.daily_starting_balance is None:
            self.daily_starting_balance = current_balance
            self.peak_balance = current_balance
            
        self.peak_balance = max(self.peak_balance, current_balance)
        
        # Calcular drawdown actual
        drawdown = (self.peak_balance - current_balance) / self.peak_balance * 100
        
        # Verificar límites
        daily_loss = (self.daily_starting_balance - current_balance) / self.daily_starting_balance * 100
        
        if daily_loss >= self.daily_loss_limit:
            return "DAILY_LOSS_LIMIT"
        elif drawdown >= self.max_drawdown:
            return "MAX_DRAWDOWN"
            
        return "OK"
