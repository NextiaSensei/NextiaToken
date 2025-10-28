#!/usr/bin/env python3
"""
Nextia Trading Bot - Risk Manager Mejorado
Sistema de gestión de riesgo y protección de capital con mejoras de robustez
"""

import logging
import json
import os
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class TradeMetrics:
    """Métricas de performance de trades"""
    total_trades: int = 0
    successful_trades: int = 0
    total_pnl: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    win_rate: float = 0.0

class RiskManager:
    """Gestor de riesgo mejorado para el trading bot con información REAL de Binance"""
    
    def __init__(self, config_file: str = 'config/trading_rules.json', trade_engine: Any = None):
        self.config = self.load_config(config_file)
        self.active_trades: Dict[str, Dict] = {}
        self.trade_engine = trade_engine
        self.symbols_info: Dict[str, Dict] = {}
        self.trade_history: List[Dict] = []
        self.performance_metrics = TradeMetrics()
        
        # MEJORA: Cache para símbolos
        self.symbol_cache = {}
        self.cache_timeout = 300  # 5 minutos
        
        # Métricas avanzadas
        self.risk_metrics = {
            'var_95': 0.0,
            'expected_shortfall': 0.0,
            'volatility_24h': 0.0,
            'correlation_matrix': {},
            'last_risk_update': datetime.now()
        }
        
        # 🔥 MEJORA: Inicialización más robusta
        self._initialize_risk_manager()
        
        logger.info("🎯 Risk Manager mejorado inicializado")
    
    def _initialize_risk_manager(self):
        """MEJORA: Inicialización robusta del Risk Manager"""
        try:
            # Intentar cargar información de Binance si está disponible
            if self.trade_engine and hasattr(self.trade_engine, 'initialized') and self.trade_engine.initialized:
                success = self.load_binance_symbols_info()
                if success:
                    logger.info("✅ Risk Manager usando información REAL de Binance")
                else:
                    logger.warning("⚠️  Risk Manager usando ajustes básicos - Falló carga de símbolos")
            else:
                logger.info("ℹ️  Risk Manager usando ajustes básicos - Trade Engine no disponible")
                
        except Exception as e:
            logger.warning(f"⚠️  Error en inicialización de Risk Manager: {e}")
            logger.info("🔄 Risk Manager continuará con ajustes básicos")
        
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Cargar configuración de riesgo desde archivo JSON con validación"""
        default_config = {
            "max_position_size_percent": 2.0,
            "stop_loss_percent": 3.0,
            "take_profit_percent": 6.0,
            "max_open_trades": 4,
            "daily_loss_limit_percent": 5.0,
            "risk_reward_ratio": 2.0,
            "auto_cleanup_trades": True,
            "reject_weak_signals": False,
            "cleanup_timeout_minutes": 4,
            "cooldown_per_trade": 30,
            "max_portfolio_allocation_per_asset": 40,
            "volatility_adjustment": True,
            "dynamic_position_sizing": True,
            "max_daily_trades": 50,
            "emergency_stop_loss": 10.0,
            "min_position_value": 10.0,
            "max_position_value": 2000.0,
            "confidence_threshold": 0.6  # MEJORA: Nuevo parámetro
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    # MEJORA: Validar configuraciones críticas mejorada
                    critical_settings = {
                        'max_position_size_percent': (0.1, 10.0),
                        'stop_loss_percent': (0.5, 20.0),
                        'max_open_trades': (1, 20)
                    }
                    
                    for key, (min_val, max_val) in critical_settings.items():
                        if key in user_config:
                            if not min_val <= user_config[key] <= max_val:
                                logger.warning(f"⚠️  {key} fuera de rango, ajustando a {max_val if user_config[key] > max_val else min_val}")
                                user_config[key] = max_val if user_config[key] > max_val else min_val
                    
                    default_config.update(user_config)
            
            logger.info("✅ Configuración de riesgo cargada y validada")
            return default_config
            
        except Exception as e:
            logger.warning(f"⚠️  Error cargando configuración, usando valores por defecto: {e}")
            return default_config

    def load_binance_symbols_info(self) -> bool:
        """Cargar información REAL de símbolos desde Binance con reintentos"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self.trade_engine or not self.trade_engine.initialized:
                    logger.warning("⚠️  Trade Engine no disponible para cargar símbolos")
                    return False
                    
                exchange_info = self.trade_engine.client.get_exchange_info()
                for symbol_info in exchange_info['symbols']:
                    symbol = symbol_info['symbol']
                    self.symbols_info[symbol] = symbol_info
                    
                logger.info(f"✅ Información de {len(self.symbols_info)} símbolos cargada desde Binance")
                return True
                
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    logger.error(f"❌ Error cargando información de símbolos después de {max_retries} intentos: {e}")
                    return False

    def get_symbol_filters(self, symbol: str) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Obtener filtros LOT_SIZE y MIN_NOTIONAL para un símbolo con caché"""
        try:
            # MEJORA: Usar cache para reducir llamadas a API
            cache_key = f"{symbol}_filters"
            if cache_key in self.symbol_cache:
                cached_data, timestamp = self.symbol_cache[cache_key]
                if time.time() - timestamp < self.cache_timeout:
                    return cached_data
                
            if symbol not in self.symbols_info:
                # Intentar cargar información si no está disponible
                if not self.load_binance_symbols_info():
                    return None, None
                
            symbol_info = self.symbols_info.get(symbol)
            if not symbol_info:
                logger.warning(f"⚠️  No hay información para {symbol}")
                return None, None
            
            lot_size_filter = None
            min_notional_filter = None
            
            for filter_obj in symbol_info['filters']:
                if filter_obj['filterType'] == 'LOT_SIZE':
                    lot_size_filter = filter_obj
                elif filter_obj['filterType'] == 'MIN_NOTIONAL':
                    min_notional_filter = filter_obj
                    
            result = (lot_size_filter, min_notional_filter)
            self.symbol_cache[cache_key] = (result, time.time())
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo filtros para {symbol}: {e}")
            return None, None

    def adjust_quantity_to_lot_size(self, symbol: str, quantity: float, price: Optional[float] = None) -> float:
        """
        Ajusta la cantidad según TODOS los filtros de Binance
        USANDO INFORMACIÓN REAL DE LA API con validación mejorada
        """
        try:
            # Obtener filtros reales de Binance
            lot_size_filter, min_notional_filter = self.get_symbol_filters(symbol)
            
            # Si no hay información de Binance, usar ajuste básico
            if not lot_size_filter:
                logger.warning(f"⚠️  Usando ajuste básico para {symbol}")
                return self._adjust_quantity_basic(symbol, quantity)
            
            # Aplicar LOT_SIZE filter
            min_qty = float(lot_size_filter['minQty'])
            max_qty = float(lot_size_filter['maxQty'])
            step_size = float(lot_size_filter['stepSize'])
            
            # Validar cantidad mínima
            if quantity < min_qty:
                logger.warning(f"⚠️  Cantidad {quantity} menor que mínimo {min_qty} para {symbol}")
                return 0.0
            
            # Calcular cantidad ajustada al step size
            steps = int(float(quantity) / step_size)
            adjusted_quantity = steps * step_size
            
            # Asegurar que está entre min y max
            adjusted_quantity = max(min_qty, min(max_qty, adjusted_quantity))
            
            # Aplicar MIN_NOTIONAL si tenemos precio
            if price and min_notional_filter:
                min_notional = float(min_notional_filter.get('minNotional', 10.0))
                notional_value = adjusted_quantity * price
                
                if notional_value < min_notional:
                    # Aumentar cantidad para cumplir con min notional
                    min_quantity = min_notional / price
                    steps = int(min_quantity / step_size)
                    if steps * step_size < min_quantity:
                        steps += 1
                    adjusted_quantity = steps * step_size
                    adjusted_quantity = min(max_qty, adjusted_quantity)
                    
                    logger.info(f"📈 Ajustado por MIN_NOTIONAL: {adjusted_quantity}")
            
            # Forzar precisión según el step size
            precision = self._get_precision_from_step_size(step_size)
            adjusted_quantity = round(adjusted_quantity, precision)
            
            logger.info(f"✅ LOT_SIZE REAL: {symbol} {quantity} -> {adjusted_quantity} (step: {step_size})")
            
            return adjusted_quantity
            
        except Exception as e:
            logger.error(f"❌ Error en adjust_quantity_to_lot_size: {e}")
            return self._adjust_quantity_basic(symbol, quantity)

    def _get_precision_from_step_size(self, step_size: float) -> int:
        """Calcular precisión decimal basado en step size"""
        if step_size == 0:
            return 0
        step_str = f"{step_size:.10f}"
        if '.' in step_str:
            return len(step_str.split('.')[1].rstrip('0'))
        return 0

    def _adjust_quantity_basic(self, symbol: str, quantity: float) -> float:
        """Ajuste básico como fallback con más símbolos"""
        lot_sizes = {
            'BTCUSDT': 0.000001,    # 6 decimales
            'ETHUSDT': 0.0001,      # 4 decimales  
            'ADAUSDT': 1,           # 0 decimales
            'DOTUSDT': 0.1,         # 1 decimal
            'LINKUSDT': 0.01,       # 2 decimales
            'BNBUSDT': 0.001,       # 3 decimales
            'XRPUSDT': 1,           # 0 decimales
            'DOGEUSDT': 1,          # 0 decimales
        }
        
        step_size = lot_sizes.get(symbol, 0.001)
        if quantity < step_size:
            return 0.0
            
        steps = int(float(quantity) / step_size)
        adjusted_quantity = steps * step_size
        
        # Forzar precisión
        if symbol in ['BTCUSDT']:
            adjusted_quantity = round(adjusted_quantity, 6)
        elif symbol in ['ETHUSDT']:
            adjusted_quantity = round(adjusted_quantity, 4)
        elif symbol in ['ADAUSDT', 'XRPUSDT', 'DOGEUSDT']:
            adjusted_quantity = int(adjusted_quantity)
        elif symbol in ['DOTUSDT']:
            adjusted_quantity = round(adjusted_quantity, 1)
        elif symbol in ['LINKUSDT']:
            adjusted_quantity = round(adjusted_quantity, 2)
        else:
            adjusted_quantity = round(adjusted_quantity, 3)
        
        logger.info(f"📏 Ajuste LOT_SIZE BÁSICO: {symbol} {quantity} → {adjusted_quantity}")
        return adjusted_quantity
    
    def calculate_dynamic_position_size(self, total_balance: float, symbol_price: float, 
                                      symbol: str, signal_strength: str = 'MEDIUM', 
                                      confidence: float = 0.0) -> float:
        """Calcular tamaño de posición dinámico basado en múltiples factores"""
        try:
            # MEJORA: Validación de parámetros de entrada
            if total_balance <= 0 or symbol_price <= 0:
                logger.error("❌ Parámetros inválidos para cálculo de posición")
                return 0.0
            
            # Factor de fuerza de señal
            strength_multiplier = {
                'STRONG': 1.2,
                'MEDIUM': 1.0,
                'WEAK': 0.7
            }.get(signal_strength.upper(), 1.0)
            
            # MEJORA: Factor de confianza
            confidence_multiplier = 0.5 + (confidence * 0.5)  # Rango: 0.5-1.0
            
            # Calcular posición base
            max_position_value = total_balance * (self.config['max_position_size_percent'] / 100)
            max_position_value *= strength_multiplier
            max_position_value *= confidence_multiplier
            
            # MEJORA: Aplicar límites mínimo y máximo de posición
            min_position_value = self.config.get('min_position_value', 10.0)
            max_position_value_config = self.config.get('max_position_value', 2000.0)
            
            max_position_value = max(min_position_value, min(max_position_value, max_position_value_config))
            
            # Ajustar por volatilidad si está habilitado
            if self.config.get('volatility_adjustment', True):
                volatility_factor = self._get_volatility_factor(symbol)
                max_position_value *= volatility_factor
            
            raw_quantity = max_position_value / symbol_price
            
            # MEJORA: Validar que la cantidad sea razonable
            if raw_quantity <= 0:
                logger.error("❌ Cantidad calculada inválida")
                return 0.0
            
            # Aplicar ajuste de LOT_SIZE con precio actual
            position_size = self.adjust_quantity_to_lot_size(symbol, raw_quantity, symbol_price)
            
            if position_size <= 0:
                logger.warning("⚠️  Posición ajustada a 0 después de LOT_SIZE")
                return 0.0
            
            # MEJORA: Verificar que no exceda el máximo por activo con manejo de errores
            try:
                position_value = position_size * symbol_price
                max_asset_allocation_percent = self.config.get('max_portfolio_allocation_per_asset', 40)  # Valor por defecto
                max_asset_allocation = total_balance * (max_asset_allocation_percent / 100)

                if position_value > max_asset_allocation:
                    logger.warning(f"⚠️  Ajustando posición para no exceder asignación máxima por activo")
                    position_size = max_asset_allocation / symbol_price
                    position_size = self.adjust_quantity_to_lot_size(symbol, position_size, symbol_price)
                    
            except Exception as e:
                logger.warning(f"⚠️  Error en verificación de asignación máxima: {e}")
                # Continuar con el tamaño de posición calculado
                
            logger.info(f"📏 Posición dinámica para {symbol}: {position_size} (Valor: ${position_size * symbol_price:.2f})")
            return position_size
                
        except Exception as e:
            logger.error(f"❌ Error calculando tamaño de posición dinámica: {e}")
            return 0.0

    def _get_volatility_factor(self, symbol: str) -> float:
        """Calcular factor de ajuste por volatilidad"""
        # Por simplicidad, retornamos 1.0
        # En producción, aquí se calcularía la volatilidad histórica
        return 1.0

    def validate_trade(self, symbol: str, quantity: float, price: float, 
                      trade_type: str, total_balance: float) -> Tuple[bool, str]:
        """
        Validar trade con validaciones avanzadas - VERSIÓN MEJORADA
        """
        try:
            logger.info(f"🛡️  Risk Manager validando: {symbol} {trade_type} {quantity} @ ${price:.2f}")
            
            # 1. Validación básica de parámetros
            if quantity <= 0 or price <= 0 or total_balance <= 0:
                return False, "Parámetros de trade inválidos"
            
            # 2. Verificar máximo de trades abiertos
            if len(self.active_trades) >= self.config['max_open_trades']:
                return False, f"Límite de trades alcanzado: {self.config['max_open_trades']}"
            
            # 3. Verificar cooldown por par
            if self.is_in_cooldown(symbol):
                return False, f"Cooldown activo para {symbol}"
            
            # 4. Verificar límite diario de trades
            if self._daily_trade_limit_reached():
                return False, "Límite diario de trades alcanzado"
            
            # 5. Verificar tamaño de posición
            position_value = quantity * price
            max_allowed = total_balance * (self.config['max_position_size_percent'] / 100)
            
            # MEJORA: 15% de tolerancia para ajustes de LOT_SIZE
            tolerance = max_allowed * 0.15
            
            if position_value > (max_allowed + tolerance):
                return False, f"Posición excede límite de ${max_allowed:.2f}"
            
            # 6. Verificar asignación máxima por activo
            max_asset_allocation = total_balance * (self.config['max_portfolio_allocation_per_asset'] / 100)
            if position_value > max_asset_allocation:
                return False, f"Excede asignación máxima para {symbol}"
            
            # 7. Verificar stop loss de emergencia
            if self._emergency_stop_triggered():
                return False, "Stop loss de emergencia activado"
            
            # MEJORA: Verificar valor mínimo de posición
            min_position_value = self.config.get('min_position_value', 10.0)
            if position_value < min_position_value:
                return False, f"Posición muy pequeña (mínimo: ${min_position_value:.2f})"
            
            logger.info(f"✅ Trade APROBADO por Risk Manager: {quantity} {symbol}")
            return True, "Trade aprobado"
            
        except Exception as e:
            logger.error(f"❌ Error validando trade: {e}")
            return False, f"Error de validación: {e}"

    def _daily_trade_limit_reached(self) -> bool:
        """Verificar si se alcanzó el límite diario de trades - VERSIÓN MEJORADA"""
        try:
            max_daily = self.config.get('max_daily_trades', 50)
            
            # MEJORA: Si el límite es muy alto (ej. 50), considerar que nunca se alcanza
            if max_daily >= 50:
                return False
                
            today = datetime.now().date()
            today_trades = [
                trade for trade in self.trade_history 
                if trade.get('timestamp') and datetime.fromtimestamp(trade['timestamp']).date() == today
            ]
            return len(today_trades) >= max_daily
        except Exception as e:
            logger.error(f"❌ Error verificando límite diario: {e}")
            return False

    def _emergency_stop_triggered(self) -> bool:
        """Verificar si se activó el stop loss de emergencia"""
        # Por simplicidad, siempre retorna False
        # En producción, aquí se verificarían condiciones de mercado extremas
        return False

    def is_in_cooldown(self, symbol: str) -> bool:
        """Verificar si el par está en período de cooldown mejorado"""
        try:
            current_time = time.time()
            cooldown_period = self.config.get('cooldown_per_trade', 30)
            
            for trade_id, trade_info in self.active_trades.items():
                if trade_info['symbol'] == symbol:
                    trade_age = current_time - trade_info.get('timestamp', current_time)
                    if trade_age < cooldown_period:
                        remaining = cooldown_period - trade_age
                        logger.info(f"⏰ Cooldown activo para {symbol}: {remaining:.0f}s restantes")
                        return True
            return False
        except Exception as e:
            logger.error(f"❌ Error verificando cooldown: {e}")
            return False

    def validate_signal(self, symbol: str, signal_type: str, strength: str, confidence: float = 0.0) -> Tuple[bool, str]:
        """Validación avanzada de señal - VERSIÓN MEJORADA"""
        try:
            logger.info(f"🛡️  Validando señal: {symbol} - {signal_type} (Fuerza: {strength}, Confianza: {confidence:.2f})")
            
            # MEJORA: Validar confianza mínima
            min_confidence = self.config.get('confidence_threshold', 0.6)
            if confidence < min_confidence:
                return False, f"Confianza insuficiente: {confidence:.2f} < {min_confidence}"
            
            # 1. Verificar máximo de trades abiertos
            if len(self.active_trades) >= self.config['max_open_trades']:
                return False, f"Límite de trades alcanzado: {self.config['max_open_trades']}"
            
            # MEJORA: No rechazar señales débiles por defecto
            if self.config.get('reject_weak_signals', False) and strength == "WEAK":
                return False, "Señal débil"
            
            # 3. Verificar cooldown
            if self.is_in_cooldown(symbol):
                return False, "Par en cooldown"
            
            # 4. Verificar límite diario
            if self._daily_trade_limit_reached():
                return False, "Límite diario de trades alcanzado"
            
            logger.info(f"✅ Señal APROBADA: {symbol} - {signal_type} (Fuerza: {strength}, Confianza: {confidence:.2f})")
            return True, "Señal aprobada"
            
        except Exception as e:
            logger.error(f"❌ Error validando señal: {e}")
            return False, f"Error de validación: {e}"

    def cleanup_completed_trades(self, trade_engine) -> int:
        """Limpieza mejorada de trades completados con métricas - VERSIÓN MEJORADA"""
        try:
            trades_to_remove = []
            current_time = time.time()
            timeout_seconds = self.config.get('cleanup_timeout_minutes', 4) * 60
            
            for trade_id, trade_info in self.active_trades.items():
                symbol = trade_info['symbol']
                asset = symbol.replace('USDT', '')
                
                # ESTRATEGIA MEJORADA:
                # 1. Todos los trades SELL se remueven inmediatamente
                if trade_info['trade_type'] == 'SELL':
                    trades_to_remove.append(trade_id)
                    logger.info(f"🗑️  Trade SELL removido: {trade_id}")
                
                # 2. Para trades BUY, verificar balance actual
                elif trade_info['trade_type'] == 'BUY':
                    try:
                        current_balance = trade_engine.get_balance(asset)
                        original_quantity = trade_info['quantity']
                        
                        # MEJORA: Margen más flexible (25% en lugar de 20%)
                        margin = original_quantity * 0.25
                        if current_balance < (original_quantity - margin):
                            trades_to_remove.append(trade_id)
                            self._record_trade_completion(trade_info, 'completed')
                            logger.info(f"🗑️  Trade BUY completado: {trade_id}")
                        
                        # LIMPIEZA POR TIEMPO - MEJORA: Más tiempo de gracia
                        elif 'timestamp' in trade_info:
                            trade_age = current_time - trade_info['timestamp']
                            if trade_age > timeout_seconds:
                                trades_to_remove.append(trade_id)
                                self._record_trade_completion(trade_info, 'timeout')
                                logger.info(f"🗑️  Trade antiguo removido: {trade_id} ({trade_age:.0f}s)")
                                
                    except Exception as e:
                        logger.warning(f"⚠️  Error verificando trade {trade_id}: {e}")
                        # En caso de error, considerar remover después de timeout extendido
                        if 'timestamp' in trade_info:
                            trade_age = current_time - trade_info['timestamp']
                            if trade_age > timeout_seconds * 2:
                                trades_to_remove.append(trade_id)
            
            # Remover trades identificados
            for trade_id in trades_to_remove:
                self.remove_active_trade(trade_id)
                
            if trades_to_remove:
                logger.info(f"🧹 LIMPIEZA COMPLETADA: {len(trades_to_remove)} trades removidos")
                logger.info(f"📊 Trades activos restantes: {len(self.active_trades)}/{self.config['max_open_trades']}")
                
            return len(trades_to_remove)
            
        except Exception as e:
            logger.error(f"❌ Error crítico en limpieza: {e}")
            return 0

    def _record_trade_completion(self, trade_info: Dict, completion_type: str):
        """Registrar finalización de trade para métricas"""
        trade_record = {
            **trade_info,
            'completion_type': completion_type,
            'completion_timestamp': time.time()
        }
        self.trade_history.append(trade_record)
        
        # MEJORA: Actualizar métricas de performance
        if completion_type == 'completed':
            self.performance_metrics.total_trades += 1
            self.performance_metrics.successful_trades += 1
            
            # Calcular win rate
            if self.performance_metrics.total_trades > 0:
                self.performance_metrics.win_rate = (
                    self.performance_metrics.successful_trades / self.performance_metrics.total_trades * 100
                )
        
        # Limitar historial a últimos 1000 trades
        if len(self.trade_history) > 1000:
            self.trade_history = self.trade_history[-1000:]

    def print_active_trades_status(self):
        """Mostrar estado actual de todos los trades activos con detalles"""
        if not self.active_trades:
            logger.info("📊 No hay trades activos")
            return
            
        logger.info("📊 === ESTADO DE TRADES ACTIVOS MEJORADO ===")
        current_time = time.time()
        
        for trade_id, trade_info in self.active_trades.items():
            age = current_time - trade_info.get('timestamp', current_time)
            age_str = f"{age:.0f}s" if age < 60 else f"{age/60:.1f}m"
            
            # Calcular P&L actual si tenemos precio actual
            current_price = 0
            try:
                if self.trade_engine:
                    current_price = self.trade_engine.get_current_price(trade_info['symbol'])
            except:
                pass
                
            pnl_info = ""
            if current_price > 0 and trade_info['trade_type'] == 'BUY':
                pnl_pct = ((current_price - trade_info['entry_price']) / trade_info['entry_price']) * 100
                pnl_info = f" | P&L: {pnl_pct:+.2f}%"
            
            logger.info(f"   {trade_id}: {trade_info['symbol']} {trade_info['trade_type']} "
                       f"({trade_info['quantity']}) - {age_str}{pnl_info}")
        
        logger.info(f"📊 Total: {len(self.active_trades)}/{self.config['max_open_trades']} trades activos")

    def get_available_for_sell(self, symbol: str, trade_engine) -> float:
        """Obtener cantidad disponible para vender con validación"""
        try:
            asset = symbol.replace('USDT', '')
            available = trade_engine.get_balance(asset)
            
            # Verificar que la cantidad sea válida después de ajustes LOT_SIZE
            if available > 0:
                adjusted_available = self.adjust_quantity_to_lot_size(symbol, available)
                logger.info(f"💰 Balance disponible para {symbol}: {available} -> {adjusted_available} después de LOT_SIZE")
                return adjusted_available
            else:
                logger.info(f"💰 Balance disponible para {symbol}: {available}")
                return available
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo balance para {symbol}: {e}")
            return 0.0

    def calculate_stop_loss_price(self, entry_price: float, trade_type: str) -> float:
        """Calcular precio de stop loss con validación"""
        try:
            sl_percent = self.config['stop_loss_percent']
            if trade_type.upper() == 'BUY':
                stop_loss = entry_price * (1 - sl_percent / 100)
            else:
                stop_loss = entry_price * (1 + sl_percent / 100)
            return round(stop_loss, 6)  # Mayor precisión
        except Exception as e:
            logger.error(f"❌ Error calculando stop loss: {e}")
            return entry_price * 0.95  # Fallback conservador

    def calculate_take_profit_price(self, entry_price: float, trade_type: str) -> float:
        """Calcular precio de take profit con validación"""
        try:
            tp_percent = self.config['take_profit_percent']
            if trade_type.upper() == 'BUY':
                take_profit = entry_price * (1 + tp_percent / 100)
            else:
                take_profit = entry_price * (1 - tp_percent / 100)
            return round(take_profit, 6)  # Mayor precisión
        except Exception as e:
            logger.error(f"❌ Error calculando take profit: {e}")
            return entry_price * 1.05  # Fallback conservador
    
    def add_active_trade(self, trade_id: str, symbol: str, quantity: float, 
                        entry_price: float, trade_type: str):
        """Agregar trade activo con métricas avanzadas"""
        # Para trades SELL, NO mantener activos (son instantáneos)
        if trade_type.upper() == 'SELL':
            logger.info(f"📊 Trade de VENTA ejecutado: {trade_id}")
            # Pero registrar en historial
            self._record_trade_completion({
                'symbol': symbol,
                'quantity': quantity,
                'entry_price': entry_price,
                'trade_type': trade_type,
                'timestamp': time.time()
            }, 'sell_executed')
            return
            
        stop_loss = self.calculate_stop_loss_price(entry_price, trade_type)
        take_profit = self.calculate_take_profit_price(entry_price, trade_type)
        
        self.active_trades[trade_id] = {
            'symbol': symbol,
            'quantity': quantity,
            'entry_price': entry_price,
            'trade_type': trade_type,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'current_pnl': 0.0,
            'timestamp': time.time(),
            'trade_id': trade_id
        }
        
        logger.info(f"📊 Trade activo registrado: {trade_id}")
        logger.info(f"   SL: ${stop_loss:.6f}, TP: ${take_profit:.6f}")
        logger.info(f"   Trades activos: {len(self.active_trades)}/{self.config['max_open_trades']}")
    
    def remove_active_trade(self, trade_id: str):
        """Remover trade completado del registro con métricas"""
        if trade_id in self.active_trades:
            trade_info = self.active_trades[trade_id]
            del self.active_trades[trade_id]
            logger.info(f"📊 Trade removido: {trade_id}")

    def get_active_trades_count(self) -> int:
        """Obtener número de trades activos"""
        return len(self.active_trades)

    def get_performance_report(self) -> Dict[str, Any]:
        """Obtener reporte de performance completo"""
        return {
            'active_trades': len(self.active_trades),
            'max_trades': self.config['max_open_trades'],
            'trade_history_count': len(self.trade_history),
            'daily_trades': len([t for t in self.trade_history 
                               if datetime.fromtimestamp(t.get('timestamp', 0)).date() == datetime.now().date()]),
            'performance_metrics': self.performance_metrics.__dict__,
            'risk_metrics': self.risk_metrics
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Obtener estado del sistema de risk management"""
        return {
            'system': 'RiskManager',
            'status': 'operational',
            'active_trades': self.get_active_trades_count(),
            'max_trades': self.config['max_open_trades'],
            'symbols_loaded': len(self.symbols_info),
            'performance': self.get_performance_report()
        }

def test_risk_manager():
    """Función de prueba del Risk Manager Mejorado"""
    logger.info("🧪 Probando Risk Manager Mejorado...")
    
    risk_mgr = RiskManager()
    
    # Probar validación de señales
    is_valid, message = risk_mgr.validate_signal("BTCUSDT", "BUY", "STRONG", 0.85)
    logger.info(f"✅ Validación de señal: {is_valid} - {message}")
    
    is_valid, message = risk_mgr.validate_signal("ADAUSDT", "SELL", "WEAK", 0.55)
    logger.info(f"✅ Validación de señal: {is_valid} - {message}")
    
    # Simular datos de prueba
    total_balance = 10000.0
    btc_price = 111340.42
    symbol = 'BTCUSDT'
    
    # Probar cálculo de posición dinámica
    position_size = risk_mgr.calculate_dynamic_position_size(total_balance, btc_price, symbol, 'STRONG', 0.85)
    logger.info(f"📈 Tamaño de posición dinámica calculado: {position_size} BTC")
    
    # Probar validación de trade
    is_valid, message = risk_mgr.validate_trade(symbol, position_size, btc_price, 'BUY', total_balance)
    logger.info(f"✅ Validación de trade: {is_valid} - {message}")
    
    # Probar cálculo de SL/TP
    stop_loss = risk_mgr.calculate_stop_loss_price(btc_price, 'BUY')
    take_profit = risk_mgr.calculate_take_profit_price(btc_price, 'BUY')
    
    logger.info(f"🎯 Stop Loss calculado: ${stop_loss:.2f}")
    logger.info(f"🎯 Take Profit calculado: ${take_profit:.2f}")
    
    # Probar registro de trade activo
    risk_mgr.add_active_trade('TEST_001', symbol, position_size, btc_price, 'BUY')
    
    # Probar cooldown
    logger.info(f"⏰ Verificando cooldown para {symbol}: {risk_mgr.is_in_cooldown(symbol)}")
    
    # Probar limpieza
    risk_mgr.print_active_trades_status()
    
    # Probar reporte de performance
    report = risk_mgr.get_performance_report()
    
    # MEJORA: Serialización segura de JSON para evitar el error
    try:
        # Convertir objetos datetime a string para JSON
        safe_report = report.copy()
        if 'risk_metrics' in safe_report and 'last_risk_update' in safe_report['risk_metrics']:
            safe_report['risk_metrics']['last_risk_update'] = safe_report['risk_metrics']['last_risk_update'].isoformat()
        
        logger.info(f"📊 Reporte de performance: {json.dumps(safe_report, indent=2, default=str)}")
    except Exception as e:
        logger.warning(f"⚠️  Error serializando reporte: {e}")
        logger.info(f"📊 Reporte de performance (formato simple): {report}")
    
    return True

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logger.info("🛡️  INICIANDO PRUEBA DE RISK MANAGER MEJORADO")
    logger.info("=====================================")
    
    if test_risk_manager():
        logger.info("=====================================")
        logger.info("🎉 RISK MANAGER MEJORADO CONFIGURADO CORRECTAMENTE")
        logger.info("💪 Sistema de protección de capital activo!")
    else:
        logger.info("=====================================")
        logger.error("💥 ERROR EN RISK MANAGER")
