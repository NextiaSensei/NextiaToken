PROTECTION_CONFIG = {
    "daily_loss_limit": 2.0,  # 2% máximo de pérdida diaria
    "max_drawdown": 5.0,      # 5% drawdown máximo desde peak
    "volatility_threshold": 3.0,  # 3% volatilidad para circuit breaker
    "max_price_change": 5.0,   # 5% cambio máximo en 1 minuto
    "emergency_contacts": ["@tu_usuario_telegram"],
    "auto_recovery": True,     # Recuperación automática después de volatility
    "recovery_delay": 300,     # 5 minutos antes de reanudar
}
