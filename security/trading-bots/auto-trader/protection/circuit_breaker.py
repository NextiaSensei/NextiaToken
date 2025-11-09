import logging
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(self, config):
        self.volatility_threshold = config['volatility_threshold']  # 3%
        self.max_price_change = config['max_price_change']  # 5% en 1 min
        self.price_history = deque(maxlen=60)  # Últimos 60 segundos
        
    def analyze_market_conditions(self, current_prices):
        """Analizar condiciones del mercado"""
        if len(self.price_history) < 10:
            return "NORMAL"
            
        # Calcular volatilidad reciente
        recent_volatility = self.calculate_volatility()
        
        # Verificar movimientos abruptos
        abrupt_moves = self.detect_abrupt_moves(current_prices)
        
        if recent_volatility > self.volatility_threshold or abrupt_moves:
            return "HIGH_VOLATILITY"
            
        return "NORMAL"
    
    def calculate_volatility(self):
        """Calcular volatilidad basada en el historial de precios"""
        if len(self.price_history) < 2:
            return 0
        returns = [self.price_history[i] / self.price_history[i-1] - 1 for i in range(1, len(self.price_history))]
        volatility = np.std(returns) * 100  # Volatilidad en porcentaje
        return volatility
    
    def detect_abrupt_moves(self, current_prices):
        """Detectar movimientos abruptos de precios"""
        # Implementar lógica para detectar movimientos bruscos
        # Por ejemplo, si el precio cambia más de max_price_change en un minuto
        if len(self.price_history) < 2:
            return False
        
        latest_price = current_prices.get('BTCUSDT')  # Ejemplo con BTC, deberías iterar sobre todos los símbolos
        if latest_price is None:
            return False
        
        # Agregar el precio actual al historial
        self.price_history.append(latest_price)
        
        # Calcular el cambio porcentual en el último minuto
        if len(self.price_history) >= 60:
            old_price = self.price_history[0]
            price_change = (latest_price - old_price) / old_price * 100
            if abs(price_change) > self.max_price_change:
                return True
        
        return False
    
    def should_activate_circuit_breaker(self, market_condition):
        """Decidir si activar circuit breaker"""
        return market_condition == "HIGH_VOLATILITY"
