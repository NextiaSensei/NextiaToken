import logging
from .emergency_stop import EmergencyStop
from .kill_switch import KillSwitch
from .circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)

class ProtectionSystem:
    def __init__(self, trade_engine, risk_manager, config):
        self.emergency_stop = EmergencyStop(trade_engine, risk_manager)
        self.kill_switch = KillSwitch(config)
        self.circuit_breaker = CircuitBreaker(config)
        self.protection_active = True
        
    async def run_protection_checks(self, current_balance, current_prices):
        """Ejecutar todas las verificaciones de protección"""
        if not self.protection_active:
            return
            
        # 1. Verificar Kill Switch
        kill_status = self.kill_switch.update_balance(current_balance)
        if kill_status != "OK":
            await self.emergency_stop.emergency_stop(f"Kill Switch: {kill_status}")
            return
            
        # 2. Verificar Circuit Breaker
        market_condition = self.circuit_breaker.analyze_market_conditions(current_prices)
        if self.circuit_breaker.should_activate_circuit_breaker(market_condition):
            await self.emergency_stop.emergency_stop(f"Circuit Breaker: {market_condition}")
            return
            
        # 3. Verificar otras condiciones de riesgo
        await self.check_additional_risk_conditions()

    async def check_additional_risk_conditions(self):
        # Aquí puedes agregar más verificaciones de riesgo
        pass

    def get_status(self):
        return {
            "protection_active": self.protection_active,
            "emergency_stop": self.emergency_stop.get_status(),
            "kill_switch": {
                "daily_loss_limit": self.kill_switch.daily_loss_limit,
                "max_drawdown": self.kill_switch.max_drawdown,
                "daily_starting_balance": self.kill_switch.daily_starting_balance,
                "peak_balance": self.kill_switch.peak_balance
            },
            "circuit_breaker": {
                "volatility_threshold": self.circuit_breaker.volatility_threshold,
                "max_price_change": self.circuit_breaker.max_price_change
            }
        }

    def enable_protection(self):
        self.protection_active = True

    def disable_protection(self):
        self.protection_active = False
