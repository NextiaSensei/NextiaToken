import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmergencyStop:
    def __init__(self, trade_engine, risk_manager):
        self.trade_engine = trade_engine
        self.risk_manager = risk_manager
        self.emergency_activated = False
        self.emergency_time = None
        
    async def emergency_stop(self, reason="Manual activation"):
        """Parada inmediata de todas las operaciones"""
        self.emergency_activated = True
        self.emergency_time = datetime.now()
        
        # 1. Cancelar todas las órdenes abiertas
        await self.trade_engine.cancel_all_orders()
        
        # 2. Cerrar todas las posiciones
        await self.trade_engine.close_all_positions()
        
        # 3. Desactivar motor de trading
        self.trade_engine.set_trading_active(False)
        
        # 4. Notificación Telegram
        await self.send_emergency_notification(reason)
        
        logger.critical(f"🚨 EMERGENCY STOP ACTIVATED: {reason}")

    async def send_emergency_notification(self, reason):
        # Aquí integras con tu sistema de notificaciones Telegram
        # Por ejemplo:
        # await self.telegram_bot.send_message(f"🚨 EMERGENCY STOP: {reason}")
        pass

    def get_status(self):
        return {
            "emergency_activated": self.emergency_activated,
            "emergency_time": self.emergency_time
        }
