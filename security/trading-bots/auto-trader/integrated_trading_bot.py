#!/usr/bin/env python3
"""
Nextia Trading Bot - Sistema Integrado Mejorado
Combina Data Engine, Trade Engine y Risk Manager para trading automático
"""

import logging
import time
import sys
import os
import asyncio
import json
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta

# Añadir ruta para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trade_engine import TradeEngine
from risk_manager import RiskManager
from profit_manager import ProfitManager
from session_scheduler import SessionScheduler

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class IntegratedTradingBot:
    """Bot de trading integrado completo - Versión Mejorada"""
    
    def __init__(self, config_path: str = "config/trading_rules.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.trade_engine = TradeEngine()
        self.risk_manager = RiskManager(trade_engine=self.trade_engine)
        
        # NUEVO: Inicializar módulos de profit y sesiones
        self.profit_manager = ProfitManager('config/trading_sessions.json')
        self.session_scheduler = SessionScheduler('config/trading_sessions.json')
        self.session_scheduler.start_scheduler()
        
        self.total_balance = 0.0
        self.performance_metrics = {
            'total_trades': 0,
            'successful_trades': 0,
            'total_pnl': 0.0,
            'daily_pnl': 0.0,
            'win_rate': 0.0,
            'last_update': datetime.now(),
            'daily_trades': 0,
            'daily_start_balance': 0.0
        }
        self.daily_reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # MEJORA: Estadísticas en tiempo real
        self.session_stats = {
            'start_time': datetime.now(),
            'signals_processed': 0,
            'trades_executed': 0,
            'errors_count': 0,
            'signals_outside_session': 0,
            'positions_closed_by_profit': 0,
            'positions_closed_by_stop': 0
        }
        
        # MEJORA: Cache para precios
        self.price_cache = {}
        self.cache_timeout = 5  # segundos
        
        self._initialize_systems()
        
    def _load_config(self) -> Dict:
        """Cargar configuración desde archivo JSON con manejo de errores robusto"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"✅ Configuración cargada desde {self.config_path}")
            
            # MEJORA: Validar configuración mínima requerida
            required_keys = ['max_position_size_percent', 'stop_loss_percent', 'max_open_trades']
            for key in required_keys:
                if key not in config:
                    raise KeyError(f"Clave de configuración requerida faltante: {key}")
                    
            return config
        except FileNotFoundError:
            logger.error(f"❌ Archivo de configuración no encontrado: {self.config_path}")
            # Configuración por defecto de emergencia
            default_config = {
                "max_position_size_percent": 2.0,
                "stop_loss_percent": 3.0,
                "take_profit_percent": 6.0,
                "max_open_trades": 4,
                "daily_loss_limit_percent": 10.0,
                "risk_reward_ratio": 2.0
            }
            logger.info("🔄 Usando configuración por defecto")
            return default_config
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error decodificando configuración: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error cargando configuración: {e}")
            raise
        
    def _initialize_systems(self):
        """Inicialización robusta de todos los sistemas - VERSIÓN MEJORADA"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self.trade_engine.initialized:
                    logger.error(f"❌ Trade Engine no inicializado (intento {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        raise Exception("Trade Engine no disponible después de múltiples intentos")
                
                # MEJORA: Configurar Risk Manager con parámetros actualizados
                self.risk_manager.config = self.config
                
                success = self.update_balance()
                if not success:
                    logger.warning("⚠️  Balance inicial no disponible, continuando...")
                
                # MEJORA: Establecer balance diario inicial
                self.performance_metrics['daily_start_balance'] = self.total_balance
                
                logger.info("✅ Sistemas inicializados correctamente")
                logger.info(f"📅 Scheduler de sesiones: {'✅ Activo' if self.session_scheduler.is_trading_time else '⏸️ Inactivo'}")
                return
                
            except Exception as e:
                logger.error(f"❌ Error en inicialización (intento {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                else:
                    logger.error("💥 Error crítico en inicialización del sistema")
                    raise
    
    def _reset_daily_metrics(self):
        """MEJORA: Reiniciar métricas diarias a medianoche"""
        now = datetime.now()
        if now.date() > self.daily_reset_time.date():
            self.performance_metrics['daily_pnl'] = 0.0
            self.performance_metrics['daily_trades'] = 0
            self.performance_metrics['daily_start_balance'] = self.total_balance
            self.daily_reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
            logger.info("🔄 Métricas diarias reiniciadas")
            
    def update_balance(self) -> bool:
        """Actualizar balance total del portfolio de forma robusta - VERSIÓN MEJORADA"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                usdt_balance = self.trade_engine.get_balance('USDT')
                btc_balance = self.trade_engine.get_balance('BTC')
                btc_price = self._get_cached_price('BTCUSDT')
                
                # MEJORA: Validación más robusta de datos
                if usdt_balance is None or btc_balance is None or btc_price <= 0:
                    logger.warning(f"⚠️  Datos de balance incompletos (intento {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    else:
                        # Usar valores por defecto como fallback
                        usdt_balance = usdt_balance or 0.0
                        btc_balance = btc_balance or 0.0
                        btc_price = btc_price if btc_price > 0 else 1.0
                        logger.warning("🔄 Usando valores de balance por defecto")
                
                new_balance = usdt_balance + (btc_balance * btc_price)
                
                # MEJORA: Calcular P&L diario
                if self.performance_metrics['daily_start_balance'] > 0:
                    daily_pnl = new_balance - self.performance_metrics['daily_start_balance']
                    self.performance_metrics['daily_pnl'] = daily_pnl
                
                self.total_balance = new_balance
                logger.info(f"💰 Balance total del portfolio: ${self.total_balance:.2f}")
                return True
                
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló obteniendo balance: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error(f"❌ Error actualizando balance después de {max_retries} intentos: {e}")
                    if self.total_balance <= 0:
                        self.total_balance = 1000.0
                        logger.info(f"🔄 Usando balance fallback: ${self.total_balance:.2f}")
                    return False
    
    def _get_cached_price(self, symbol: str) -> float:
        """MEJORA: Obtener precio con cache para reducir llamadas a API"""
        now = time.time()
        if symbol in self.price_cache:
            price, timestamp = self.price_cache[symbol]
            if now - timestamp < self.cache_timeout:
                return price
        
        # Obtener nuevo precio
        price = self.trade_engine.get_current_price(symbol)
        if price > 0:
            self.price_cache[symbol] = (price, now)
        return price
    
    def cleanup_old_trades(self) -> int:
        """Limpiar trades antiguos antes de procesar nueva señal - VERSIÓN MEJORADA"""
        try:
            cleaned_count = self.risk_manager.cleanup_completed_trades(self.trade_engine)
            if cleaned_count > 0:
                logger.info(f"🧹 Se limpiaron {cleaned_count} trades completados")
                # MEJORA: Actualizar balance después de limpieza
                self.update_balance()
            return cleaned_count
        except Exception as e:
            logger.error(f"❌ Error limpiando trades: {e}")
            return 0

    def check_profit_stop_conditions(self):
        """NUEVO: Verificar condiciones de profit/stop para posiciones activas"""
        try:
            active_trades = self.risk_manager.active_trades.copy()
            closed_count = 0
            
            for trade_id, trade_info in active_trades.items():
                symbol = trade_info['symbol']
                current_price = self._get_cached_price(symbol)
                
                if current_price <= 0:
                    continue
                
                # Verificar si debería cerrar por profit/stop
                should_close = self.profit_manager.should_close_position(
                    symbol, current_price, trade_info['entry_price'], trade_info['trade_type'].lower()
                )
                
                if should_close:
                    # Cerrar posición
                    position_size = self.risk_manager.get_available_for_sell(symbol, self.trade_engine)
                    if position_size > 0:
                        success = self.trade_engine.execute_sell_order(symbol, position_size)
                        if success:
                            self.risk_manager.remove_active_trade(trade_id)
                            closed_count += 1
                            
                            # Determinar si fue por profit o stop
                            profit_percent = ((current_price - trade_info['entry_price']) / trade_info['entry_price']) * 100
                            if profit_percent >= 0:
                                self.session_stats['positions_closed_by_profit'] += 1
                                logger.info(f"🎯 POSICIÓN CERRADA POR PROFIT: {symbol} (+{profit_percent:.2f}%)")
                            else:
                                self.session_stats['positions_closed_by_stop'] += 1
                                logger.info(f"🛑 POSICIÓN CERRADA POR STOP: {symbol} ({profit_percent:.2f}%)")
            
            if closed_count > 0:
                logger.info(f"📊 Cierre automático: {closed_count} posiciones por profit/stop")
                self.update_balance()
                
            return closed_count
            
        except Exception as e:
            logger.error(f"❌ Error verificando profit/stop: {e}")
            return 0
    
    def process_signal(self, symbol: str, signal_type: str, strength: str, confidence: float = 0.0) -> Tuple[bool, str]:
        """Procesar señal de trading y ejecutar orden si es válida - VERSIÓN MEJORADA"""
        try:
            # MEJORA: Resetear métricas diarias si es necesario
            self._reset_daily_metrics()
            
            # NUEVO: Verificar horario de trading
            if not self.session_scheduler.is_trading_time:
                self.session_stats['signals_outside_session'] += 1
                logger.warning(f"⏰ Fuera del horario de trading - Señal rechazada: {symbol}")
                return False, "Fuera del horario de trading"
            
            # NUEVO: Verificar condiciones de profit/stop antes de nueva señal
            self.check_profit_stop_conditions()
            
            self.session_stats['signals_processed'] += 1
            logger.info(f"🎯 Procesando señal: {symbol} - {signal_type} (Fuerza: {strength}, Confianza: {confidence:.2f})")
            
            # MEJORA: Validación inicial de parámetros
            if not symbol or not signal_type:
                return False, "Parámetros de señal inválidos"
            
            # MEJORA: Validar confianza mínima
            if confidence < 0.6:  # 60% de confianza mínima
                logger.warning(f"⚠️  Señal con baja confianza ({confidence:.2f}), omitiendo...")
                return False, f"Confianza demasiado baja: {confidence:.2f}"
            
            # Paso 1: Limpiar trades completados
            self.cleanup_old_trades()
            
            # Paso 2: Obtener precio actual con cache
            current_price = self._get_cached_price(symbol)
            if current_price <= 0:
                error_msg = f"Error obteniendo precio para {symbol}"
                logger.error(f"❌ {error_msg}")
                return False, error_msg
            
            # MEJORA: Verificar que el balance esté actualizado
            if self.total_balance <= 0:
                self.update_balance()
                if self.total_balance <= 0:
                    error_msg = "Balance del portfolio no disponible"
                    logger.error(f"❌ {error_msg}")
                    return False, error_msg
            
            # Paso 3: Calcular tamaño de posición dinámico considerando confianza
            position_size = self.risk_manager.calculate_dynamic_position_size(
                self.total_balance, current_price, symbol, strength, confidence
            )
            
            if position_size <= 0:
                error_msg = f"Tamaño de posición inválido para {symbol}"
                logger.error(f"❌ {error_msg}")
                return False, error_msg
            
            # Paso 4: Validar trade con Risk Manager
            is_valid, message = self.risk_manager.validate_trade(
                symbol, position_size, current_price, signal_type, self.total_balance
            )
            
            if not is_valid:
                logger.warning(f"⚠️  Trade rechazado por Risk Manager: {message}")
                return False, f"Risk Manager: {message}"
            
            # Paso 5: Ejecutar orden
            success = False
            trade_id = f"{symbol}_{int(time.time())}"
            
            if signal_type.upper() == 'BUY':
                success = self.trade_engine.execute_buy_order(symbol, position_size)
                if success:
                    self.risk_manager.add_active_trade(
                        trade_id, symbol, position_size, current_price, 'BUY'
                    )
                    self._update_performance_metrics(True)
                    self.session_stats['trades_executed'] += 1
                    self.performance_metrics['daily_trades'] += 1
                    logger.info(f"✅ Orden de COMPRA ejecutada: {position_size:.6f} {symbol} a ${current_price:.2f}")
                    
            elif signal_type.upper() == 'SELL':
                success = self.trade_engine.execute_sell_order(symbol, position_size)
                if success:
                    self._update_performance_metrics(True)
                    self.session_stats['trades_executed'] += 1
                    self.performance_metrics['daily_trades'] += 1
                    logger.info(f"✅ Orden de VENTA ejecutada: {position_size:.6f} {symbol} a ${current_price:.2f}")
            
            else:
                error_msg = f"Tipo de señal no reconocido: {signal_type}"
                logger.warning(f"⚠️ {error_msg}")
                return False, error_msg
            
            # Paso 6: Actualizar balance después de la operación
            if success:
                time.sleep(2)
                self.update_balance()
                logger.info(f"📈 Balance actualizado: ${self.total_balance:.2f}")
                
            return success, "Operación ejecutada exitosamente" if success else "Error en ejecución"
                
        except Exception as e:
            error_msg = f"Error procesando señal: {e}"
            logger.error(f"❌ {error_msg}")
            self.session_stats['errors_count'] += 1
            return False, error_msg

    def _get_current_price_with_retry(self, symbol: str, max_retries: int = 2) -> float:
        """MEJORA: Obtener precio actual con reintentos"""
        for attempt in range(max_retries):
            try:
                price = self._get_cached_price(symbol)
                if price > 0:
                    return price
                else:
                    logger.warning(f"⚠️  Precio inválido para {symbol} (intento {attempt + 1}/{max_retries})")
            except Exception as e:
                logger.warning(f"⚠️  Error obteniendo precio (intento {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                time.sleep(1)
        
        logger.error(f"❌ No se pudo obtener precio para {symbol} después de {max_retries} intentos")
        return 0.0
    
    def _update_performance_metrics(self, success: bool):
        """Actualizar métricas de performance"""
        self.performance_metrics['total_trades'] += 1
        if success:
            self.performance_metrics['successful_trades'] += 1
        
        # MEJORA: Calcular win rate en tiempo real
        if self.performance_metrics['total_trades'] > 0:
            self.performance_metrics['win_rate'] = (
                self.performance_metrics['successful_trades'] / self.performance_metrics['total_trades'] * 100
            )
        
        self.performance_metrics['last_update'] = datetime.now()
    
    def get_portfolio_info(self) -> Dict:
        """Obtener información completa del portfolio - VERSIÓN MEJORADA"""
        try:
            self.update_balance()
            active_trades = self.risk_manager.get_active_trades_count()
            
            info = {
                'total_balance': self.total_balance,
                'active_trades': active_trades,
                'max_trades': self.config['max_open_trades'],
                'performance': self.performance_metrics,
                'session_stats': self.session_stats,
                'trading_session_active': self.session_scheduler.is_trading_time,
                'profit_manager_configured': len(self.profit_manager.profit_targets) > 0,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"📊 Portfolio - Balance: ${self.total_balance:.2f}, "
                       f"Trades activos: {active_trades}/{self.config['max_open_trades']}, "
                       f"Win Rate: {self.performance_metrics['win_rate']:.1f}%, "
                       f"Sesión: {'✅ Activa' if self.session_scheduler.is_trading_time else '⏸️ Inactiva'}")
            return info
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo info del portfolio: {e}")
            return {
                'total_balance': self.total_balance or 0,
                'active_trades': 0,
                'max_trades': 0,
                'performance': self.performance_metrics,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_system_status(self) -> Dict:
        """Obtener estado completo del sistema - VERSIÓN MEJORADA"""
        try:
            portfolio_info = self.get_portfolio_info()
            
            # MEJORA: Calcular uptime de la sesión
            session_duration = datetime.now() - self.session_stats['start_time']
            
            status = {
                'system': 'IntegratedTradingBot',
                'status': 'operational',
                'portfolio': portfolio_info,
                'trade_engine': 'operational' if self.trade_engine.initialized else 'error',
                'risk_manager': 'operational',
                'profit_manager': 'operational',
                'session_scheduler': 'operational',
                'trading_session_active': self.session_scheduler.is_trading_time,
                'total_balance': self.total_balance,
                'session_duration_hours': round(session_duration.total_seconds() / 3600, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            if not self.trade_engine.initialized:
                status['status'] = 'degraded'
                status['trade_engine'] = 'error'
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estado del sistema: {e}")
            return {
                'system': 'IntegratedTradingBot',
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

def main():
    """Función principal del bot integrado - Versión Mejorada"""
    logger.info("🚀 INICIANDO NEXTIA TRADING BOT INTEGRADO - VERSIÓN MEJORADA")
    logger.info("==========================================")
    
    try:
        # Crear bot integrado
        bot = IntegratedTradingBot()
        
        if not bot.trade_engine.initialized:
            logger.error("❌ No se pudo inicializar el Trade Engine")
            return
        
        logger.info("✅ Todos los sistemas inicializados correctamente")
        logger.info("   - Trade Engine: ✅")
        logger.info("   - Risk Manager: ✅")
        logger.info("   - Profit Manager: ✅")
        logger.info("   - Session Scheduler: ✅")
        logger.info("   - Balance Tracking: ✅")
        logger.info("   - Dynamic Position Sizing: ✅")
        logger.info("   - Price Caching: ✅")
        logger.info("   - Daily Metrics: ✅")
        logger.info(f"   - Sesión Trading: {'✅ Activa' if bot.session_scheduler.is_trading_time else '⏸️ Inactiva'}")
        
        # Mostrar configuración cargada
        logger.info(f"⚙️  Configuración cargada:")
        for key, value in bot.config.items():
            logger.info(f"     {key}: {value}")
        
        # Mostrar profit targets configurados
        logger.info(f"🎯 Profit Targets configurados: {len(bot.profit_manager.profit_targets)} símbolos")
        
        # Mostrar info del portfolio
        portfolio_info = bot.get_portfolio_info()
        logger.info(f"💰 Balance inicial: ${portfolio_info['total_balance']:.2f}")
        
        # Mostrar estado del sistema
        system_status = bot.get_system_status()
        logger.info(f"🔧 Estado del sistema: {system_status['status']}")
        
        logger.info("==========================================")
        logger.info("🎉 SISTEMA INTEGRADO MEJORADO FUNCIONANDO CORRECTAMENTE")
        logger.info("💪 Bot listo para recibir señales del Data Engine!")
        
    except Exception as e:
        logger.error(f"❌ Error crítico en inicialización: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
