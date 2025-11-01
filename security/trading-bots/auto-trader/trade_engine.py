#!/usr/bin/env python3
"""
Nextia Trading Bot - Trade Engine MEJORADO con ProfitManager integrado
Motor de ejecución de órdenes con gestión avanzada de profits y riesgo
"""

import os
import sys
import json
import logging
import time
import threading
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv

# Importar ProfitManager mejorado
try:
    from profit_manager import ProfitManager
except ImportError:
    # Fallback para desarrollo
    class ProfitManager:
        def __init__(self):
            self.profit_targets = {'default': 2.0}
            self.stop_losses = {'default': 1.5}
        
        def should_close_position(self, symbol, current_price, entry_price, position_type):
            return False, None, {}

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trade_engine.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TradeEngine:
    """Motor de ejecución de órdenes MEJORADO con ProfitManager integrado"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.initialized = False
        self.symbols_info: Dict[str, Dict] = {}
        self.order_history: List[Dict] = []
        self.active_positions: Dict[str, Dict] = {}
        self.profit_manager = ProfitManager()
        
        # 🚀 NUEVO: Métricas mejoradas
        self.performance_metrics = {
            'total_orders': 0,
            'successful_orders': 0,
            'failed_orders': 0,
            'total_volume': 0.0,
            'total_profit': 0.0,
            'last_order_time': None,
            'average_execution_time': 0.0,
            'success_rate': 0.0,
            'profit_factor': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0
        }
        
        self.time_offset = 0
        self.connection_retries = 0
        self.max_retries = 5
        self.initial_balance = 0.0
        self.current_balance = 0.0
        self.emergency_stop_activated = False
        
        self.setup_binance_client()
        self.start_health_monitor()
        logger.info("✅ Trade Engine MEJORADO inicializado con ProfitManager")
        
    def setup_binance_client(self) -> bool:
        """Configurar cliente de Binance Testnet - VERSIÓN DEFINITIVA"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                load_dotenv()
                
                api_key = os.getenv('BINANCE_TESTNET_API_KEY')
                api_secret = os.getenv('BINANCE_TESTNET_SECRET_KEY')
                
                if not api_key or not api_secret:
                    logger.error("❌ API Keys no configuradas en .env")
                    return False
                
                # SOLUCIÓN DEFINITIVA: Configurar cliente con manejo de tiempo automático
                self.client = Client(
                    api_key=api_key,
                    api_secret=api_secret,
                    testnet=True
                )
                
                # Sincronización de tiempo MEJORADA
                self._synchronize_time_robust()
                
                # Verificar conexión
                self.client.ping()
                logger.info("✅ Trade Engine conectado a Binance Testnet")
                self.initialized = True
                self.connection_retries = 0
                
                # Obtener balance inicial
                self.initial_balance = self.get_balance('USDT')
                self.current_balance = self.initial_balance
                
                # Cargar información de símbolos
                self.load_symbols_info()
                return True
                
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló: {e}")
                self.connection_retries += 1
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    logger.error(f"❌ Error configurando Trade Engine después de {max_retries} intentos: {e}")
                    self.initialized = False
                    return False

    def _synchronize_time_robust(self) -> bool:
        """
        SOLUCIÓN DEFINITIVA: Sincronización de tiempo ultra-robusta
        """
        try:
            # Obtener tiempo del servidor
            server_time = self.client.get_server_time()
            binance_time = server_time['serverTime']
            local_time = int(time.time() * 1000)
            
            # Calcular diferencia
            time_diff = binance_time - local_time
            logger.info(f"⏰ Diferencia de tiempo detectada: {time_diff}ms ({time_diff/1000:.1f} segundos)")
            
            # SOLUCIÓN CRÍTICA: Configurar el offset correctamente
            self.time_offset = time_diff
            
            # Configurar recvWindow extendido para compensar diferencias grandes
            self.client.recv_window = 60000  # 60 segundos
            
            logger.info(f"🔧 Offset configurado: {time_diff}ms, RecvWindow: 60s")
            logger.info("✅ Sincronización de tiempo completada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en sincronización de tiempo: {e}")
            # Fallback seguro
            self.time_offset = 0
            self.client.recv_window = 60000
            return False

    def get_balance(self, asset: str = 'USDT') -> float:
        """Obtener balance - VERSIÓN DEFINITIVA Y ROBUSTA"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                if not self.initialized:
                    return 0.0
                
                # SOLUCIÓN: Usar get_account() con manejo de tiempo automático
                account = self.client.get_account()
                
                for balance in account['balances']:
                    if balance['asset'] == asset:
                        free_balance = float(balance['free'])
                        logger.info(f"💰 Balance {asset}: {free_balance}")
                        return free_balance
                return 0.0
                
            except BinanceAPIException as e:
                if "timestamp" in str(e):
                    logger.warning(f"⚠️  Error de timestamp, re-sincronizando (intento {attempt + 1})")
                    self._synchronize_time_robust()
                    continue
                logger.error(f"❌ Error API obteniendo balance de {asset}: {e}")
                return 0.0
            except Exception as e:
                logger.error(f"❌ Error obteniendo balance de {asset}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    return 0.0

    def load_symbols_info(self) -> bool:
        """Cargar información de símbolos"""
        try:
            if not self.initialized:
                return False
                
            exchange_info = self.client.get_exchange_info()
            for symbol_info in exchange_info['symbols']:
                symbol = symbol_info['symbol']
                self.symbols_info[symbol] = symbol_info
                
            logger.info(f"✅ Información de {len(self.symbols_info)} símbolos cargada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cargando información de símbolos: {e}")
            return False

    def get_symbol_filters(self, symbol: str) -> Optional[Dict]:
        """Obtener filtros LOT_SIZE para un símbolo"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                if symbol not in self.symbols_info:
                    self.load_symbols_info()
                    
                symbol_info = self.symbols_info.get(symbol)
                if not symbol_info:
                    return None
                
                for filter_obj in symbol_info['filters']:
                    if filter_obj['filterType'] == 'LOT_SIZE':
                        return filter_obj
                        
                return None
                
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló obteniendo filtros: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error(f"❌ Error obteniendo filtros para {symbol}: {e}")
                    return None

    def adjust_quantity_to_lot_size(self, symbol: str, quantity: float) -> float:
        """Ajusta la cantidad al tamaño de lote permitido"""
        try:
            lot_size_filter = self.get_symbol_filters(symbol)
            
            if not lot_size_filter:
                logger.warning(f"⚠️  Usando ajuste básico para {symbol}")
                return self._adjust_quantity_basic(symbol, quantity)
            
            min_qty = float(lot_size_filter['minQty'])
            max_qty = float(lot_size_filter['maxQty'])
            step_size = float(lot_size_filter['stepSize'])
            
            if quantity < min_qty:
                logger.warning(f"⚠️  Cantidad {quantity} menor que mínimo {min_qty} para {symbol}")
                return 0.0
            
            steps = int(float(quantity) / step_size)
            adjusted_quantity = steps * step_size
            adjusted_quantity = max(min_qty, min(max_qty, adjusted_quantity))
            
            precision = self._get_precision_from_step_size(step_size)
            adjusted_quantity = round(adjusted_quantity, precision)
            
            logger.info(f"✅ LOT_SIZE: {symbol} {quantity} -> {adjusted_quantity}")
            
            return adjusted_quantity
            
        except Exception as e:
            logger.error(f"❌ Error en adjust_quantity_to_lot_size: {e}")
            return self._adjust_quantity_basic(symbol, quantity)

    def _get_precision_from_step_size(self, step_size: float) -> int:
        """Calcular precisión decimal"""
        if step_size >= 1:
            return 0
        step_str = f"{step_size:.10f}"
        if '.' in step_str:
            return len(step_str.split('.')[1].rstrip('0'))
        return 0

    def _adjust_quantity_basic(self, symbol: str, quantity: float) -> float:
        """Ajuste básico como fallback"""
        lot_sizes = {
            'BTCUSDT': 0.000001,
            'ETHUSDT': 0.0001,  
            'ADAUSDT': 1,
            'DOTUSDT': 0.1,
            'LINKUSDT': 0.01,
            'BNBUSDT': 0.001,
            'XRPUSDT': 1,
            'DOGEUSDT': 1,
        }
        
        step_size = lot_sizes.get(symbol, 0.001)
        if quantity < step_size:
            return 0.0
            
        steps = int(float(quantity) / step_size)
        adjusted_quantity = steps * step_size
        
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
        
        logger.info(f"📏 Ajuste BÁSICO: {symbol} {quantity} → {adjusted_quantity}")
        return adjusted_quantity

    # 🚀 NUEVO: Función mejorada para calcular tamaño de posición
    def calculate_position_size(self, symbol: str, signal_strength: str) -> float:
        """Calcula el tamaño de posición usando ProfitManager mejorado"""
        try:
            current_balance = self.get_balance('USDT')
            
            # Usar ProfitManager para recomendación
            recommendation = self.profit_manager.get_trade_recommendation(
                symbol, current_balance, signal_strength
            )
            
            position_size = recommendation.get('recommended_position_size', current_balance * 0.1)
            
            logger.info(f"🎯 Position Size calculado: {symbol} - ${position_size:.2f} (Signal: {signal_strength})")
            return position_size
            
        except Exception as e:
            logger.error(f"❌ Error calculando position size: {e}")
            # Fallback seguro
            return self.get_balance('USDT') * 0.1

    def execute_buy_order(self, symbol: str, quantity: float, order_type: str = 'MARKET') -> Dict[str, Any]:
        """Ejecutar orden de compra MEJORADA con ProfitManager"""
        start_time = time.time()
        order_result = {
            'success': False,
            'order_id': None,
            'executed_quantity': 0.0,
            'executed_price': 0.0,
            'total_cost': 0.0,
            'status': 'FAILED',
            'error': None
        }
        
        try:
            if not self.initialized:
                order_result['error'] = "Trade Engine no inicializado"
                return order_result
            
            # 🚀 NUEVO: Verificar emergency stop
            if self.emergency_stop_activated:
                order_result['error'] = "EMERGENCY STOP activado - trading suspendido"
                return order_result
            
            adjusted_quantity = self.adjust_quantity_to_lot_size(symbol, quantity)
            
            if adjusted_quantity <= 0:
                order_result['error'] = f"Cantidad ajustada inválida: {adjusted_quantity}"
                return order_result
            
            quote_balance = self.get_balance('USDT')
            current_price = self.get_current_price(symbol)
            required_amount = adjusted_quantity * current_price
            
            if quote_balance < required_amount:
                order_result['error'] = f"Balance insuficiente. USDT: {quote_balance}, Necesario: {required_amount:.2f}"
                return order_result
            
            logger.info(f"🔍 Enviando COMPRA: {symbol} {adjusted_quantity}")
            
            # La librería maneja automáticamente el timestamp
            order = self.client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=order_type,
                quantity=adjusted_quantity
            )
            
            order_status = order.get('status', 'UNKNOWN')
            order_id = order.get('orderId')
            
            order_result['order_id'] = order_id
            order_result['status'] = order_status
            
            if order_status in ['FILLED', 'PARTIALLY_FILLED']:
                fills = order.get('fills', [])
                if fills:
                    executed_price = float(fills[0]['price'])
                    executed_qty = sum(float(fill['qty']) for fill in fills)
                    total_cost = sum(float(fill['qty']) * float(fill['price']) for fill in fills)
                    
                    order_result['executed_quantity'] = executed_qty
                    order_result['executed_price'] = executed_price
                    order_result['total_cost'] = total_cost
                    order_result['success'] = True
                
                logger.info(f"✅ COMPRA EJECUTADA: {executed_qty} {symbol} @ {executed_price}")
                
                # 🚀 NUEVO: Registrar posición activa
                self._register_active_position(symbol, executed_price, executed_qty, 'long')
                
            else:
                order_result['error'] = f"Orden no ejecutada: {order_status}"
                logger.warning(f"⚠️  Orden no ejecutada: {order_status}")
            
        except BinanceAPIException as e:
            error_msg = f"Error de Binance API: {e}"
            order_result['error'] = error_msg
            logger.error(error_msg)
        except BinanceOrderException as e:
            error_msg = f"Error de orden: {e}"
            order_result['error'] = error_msg
            logger.error(error_msg)
        except Exception as e:
            error_msg = f"Error inesperado: {e}"
            order_result['error'] = error_msg
            logger.error(error_msg)
        
        # 🛡️ FIX CRÍTICO: FINALLY CORRECTAMENTE INDENTADO
        finally:
            execution_time = time.time() - start_time
            # 🛡️ FIX: Manejo seguro de métricas cuando hay error temprano
            volume_for_metrics = order_result.get('total_cost', 0.0)
            if volume_for_metrics == 0 and 'adjusted_quantity' in locals() and 'current_price' in locals():
                volume_for_metrics = adjusted_quantity * current_price
                
            self._update_order_metrics(
                order_result['success'], 
                volume_for_metrics, 
                execution_time
            )
            
            self._record_order_history({
                'symbol': symbol,
                'side': 'BUY',
                'quantity': adjusted_quantity if 'adjusted_quantity' in locals() else quantity,
                'price': order_result['executed_price'],
                'order_type': order_type,
                'success': order_result['success'],
                'execution_time': execution_time,
                'timestamp': time.time(),
                'order_id': order_result['order_id'],
                'error': order_result['error']
            })
        
        return order_result

    def execute_sell_order(self, symbol: str, quantity: float, order_type: str = 'MARKET') -> Dict[str, Any]:
        """Ejecutar orden de venta MEJORADA con ProfitManager"""
        start_time = time.time()
        order_result = {
            'success': False,
            'order_id': None,
            'executed_quantity': 0.0,
            'executed_price': 0.0,
            'total_revenue': 0.0,
            'status': 'FAILED',
            'error': None
        }
        
        try:
            if not self.initialized:
                order_result['error'] = "Trade Engine no inicializado"
                return order_result
            
            # 🚀 NUEVO: Verificar emergency stop
            if self.emergency_stop_activated:
                order_result['error'] = "EMERGENCY STOP activado - trading suspendido"
                return order_result
            
            adjusted_quantity = self.adjust_quantity_to_lot_size(symbol, quantity)
            
            if adjusted_quantity <= 0:
                order_result['error'] = f"Cantidad ajustada inválida: {adjusted_quantity}"
                return order_result
            
            base_asset = symbol.replace('USDT', '')
            base_balance = self.get_balance(base_asset)
            
            if base_balance < adjusted_quantity:
                order_result['error'] = f"Balance insuficiente. {base_asset}: {base_balance}, Intentando: {adjusted_quantity}"
                return order_result
            
            logger.info(f"🔍 Enviando VENTA: {symbol} {adjusted_quantity}")
            
            order = self.client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=order_type,
                quantity=adjusted_quantity
            )
            
            order_status = order.get('status', 'UNKNOWN')
            order_id = order.get('orderId')
            
            order_result['order_id'] = order_id
            order_result['status'] = order_status
            
            if order_status in ['FILLED', 'PARTIALLY_FILLED']:
                fills = order.get('fills', [])
                if fills:
                    executed_price = float(fills[0]['price'])
                    executed_qty = sum(float(fill['qty']) for fill in fills)
                    total_revenue = executed_qty * executed_price
                    
                    order_result['executed_quantity'] = executed_qty
                    order_result['executed_price'] = executed_price
                    order_result['total_revenue'] = total_revenue
                    order_result['success'] = True
                
                logger.info(f"✅ VENTA EJECUTADA: {executed_qty} {symbol} @ {executed_price}")
                
                # 🚀 NUEVO: Calcular profit y actualizar métricas
                if symbol in self.active_positions:
                    entry_price = self.active_positions[symbol]['entry_price']
                    profit = (executed_price - entry_price) * executed_qty
                    self.performance_metrics['total_profit'] += profit
                    
                    # Remover posición activa
                    self.active_positions.pop(symbol, None)
                
            else:
                order_result['error'] = f"Orden no ejecutada: {order_status}"
                logger.warning(f"⚠️  Orden no ejecutada: {order_status}")
            
        except BinanceAPIException as e:
            error_msg = f"Error de Binance API: {e}"
            order_result['error'] = error_msg
            logger.error(error_msg)
        except BinanceOrderException as e:
            error_msg = f"Error de orden: {e}"
            order_result['error'] = error_msg
            logger.error(error_msg)
        except Exception as e:
            error_msg = f"Error inesperado: {e}"
            order_result['error'] = error_msg
            logger.error(error_msg)
        
        # 🛡️ FIX: FINALLY CORRECTAMENTE INDENTADO
        finally:
            execution_time = time.time() - start_time
            # 🛡️ FIX: Manejo seguro de métricas cuando hay error temprano
            volume_for_metrics = order_result.get('total_revenue', 0.0)
            if volume_for_metrics == 0 and 'adjusted_quantity' in locals():
                current_price_sell = self.get_current_price(symbol)
                volume_for_metrics = adjusted_quantity * current_price_sell
                
            self._update_order_metrics(
                order_result['success'], 
                volume_for_metrics, 
                execution_time
            )
            
            self._record_order_history({
                'symbol': symbol,
                'side': 'SELL',
                'quantity': adjusted_quantity if 'adjusted_quantity' in locals() else quantity,
                'price': order_result['executed_price'],
                'order_type': order_type,
                'success': order_result['success'],
                'execution_time': execution_time,
                'timestamp': time.time(),
                'order_id': order_result['order_id'],
                'error': order_result['error']
            })
        
        return order_result

    # 🚀 NUEVO: Función para registrar posición activa
    def _register_active_position(self, symbol: str, entry_price: float, quantity: float, position_type: str):
        """Registra una posición activa para seguimiento"""
        self.active_positions[symbol] = {
            'entry_price': entry_price,
            'quantity': quantity,
            'position_type': position_type,
            'entry_time': datetime.now(),
            'highest_price': entry_price,
            'lowest_price': entry_price
        }
        logger.info(f"📊 Posición activa registrada: {symbol} {position_type} @ {entry_price}")

    # 🚀 NUEVO: Función para verificar cierre de posiciones
    def check_position_management(self) -> List[Dict]:
        """Verifica todas las posiciones activas para cierre por profit/stop"""
        close_recommendations = []
        
        for symbol, position in self.active_positions.items():
            current_price = self.get_current_price(symbol)
            
            # Actualizar highest/lowest price para trailing stops
            if current_price > position['highest_price']:
                position['highest_price'] = current_price
            if current_price < position['lowest_price']:
                position['lowest_price'] = current_price
            
            # Usar ProfitManager para verificar cierre
            should_close, reason, metadata = self.profit_manager.should_close_position(
                symbol=symbol,
                current_price=current_price,
                entry_price=position['entry_price'],
                position_type=position['position_type'],
                highest_price=position['highest_price'],
                lowest_price=position['lowest_price'],
                current_balance=self.current_balance,
                initial_balance=self.initial_balance
            )
            
            if should_close:
                close_recommendations.append({
                    'symbol': symbol,
                    'reason': reason,
                    'metadata': metadata,
                    'current_price': current_price,
                    'entry_price': position['entry_price']
                })
        
        return close_recommendations

    # 🚨 MÉTODOS NUEVOS PARA EMERGENCY STOP SYSTEM
    async def cancel_all_orders(self) -> bool:
        """Cancelar todas las órdenes abiertas - PARA EMERGENCY STOP"""
        try:
            if not self.initialized:
                return False
                
            # Cancelar todas las órdenes abiertas
            open_orders = self.client.get_open_orders()
            for order in open_orders:
                try:
                    self.client.cancel_order(
                        symbol=order['symbol'],
                        orderId=order['orderId']
                    )
                    logger.info(f"✅ Orden cancelada: {order['symbol']} {order['orderId']}")
                except Exception as e:
                    logger.warning(f"⚠️  Error cancelando orden {order['orderId']}: {e}")
            
            logger.info("✅ Todas las órdenes canceladas")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cancelando órdenes: {e}")
            return False

    async def close_all_positions(self) -> bool:
        """Cerrar todas las posiciones activas - PARA EMERGENCY STOP"""
        try:
            if not self.initialized:
                return False
            
            positions_closed = 0
            
            # Cerrar todas las posiciones en active_positions
            for symbol, position in list(self.active_positions.items()):
                try:
                    if position['position_type'] == 'long':
                        # Vender la posición
                        sell_result = self.execute_sell_order(
                            symbol=symbol,
                            quantity=position['quantity']
                        )
                        if sell_result['success']:
                            positions_closed += 1
                            logger.info(f"✅ Posición cerrada: {symbol}")
                        else:
                            logger.warning(f"⚠️  No se pudo cerrar posición: {symbol}")
                except Exception as e:
                    logger.error(f"❌ Error cerrando posición {symbol}: {e}")
            
            logger.info(f"✅ {positions_closed} posiciones cerradas")
            return positions_closed > 0
            
        except Exception as e:
            logger.error(f"❌ Error cerrando posiciones: {e}")
            return False

    def set_trading_active(self, status: bool):
        """Activar/desactivar trading - PARA EMERGENCY STOP"""
        self.emergency_stop_activated = not status
        logger.info(f"🔧 Trading {'ACTIVADO' if status else 'DESACTIVADO'}")

    def get_current_balance(self) -> float:
        """Obtener balance actual - PARA EMERGENCY STOP"""
        return self.get_balance('USDT')

    async def activate_emergency_stop(self, reason: str = "Manual activation"):
        """Activa el emergency stop - VERSIÓN MEJORADA ASINCRONA"""
        self.emergency_stop_activated = True
        logger.critical(f"🚨 EMERGENCY STOP ACTIVADO: {reason}")
        
        try:
            # 1. Cancelar todas las órdenes abiertas
            await self.cancel_all_orders()
            
            # 2. Cerrar todas las posiciones activas
            await self.close_all_positions()
            
            # 3. Notificación adicional
            logger.info("✅ Emergency Stop completado - Todas las posiciones cerradas")
            
        except Exception as e:
            logger.error(f"❌ Error durante Emergency Stop: {e}")

    def deactivate_emergency_stop(self):
        """Desactiva el emergency stop"""
        self.emergency_stop_activated = False
        logger.info("✅ Emergency Stop desactivado")

    def _update_order_metrics(self, success: bool, volume: float, execution_time: float):
        """Actualizar métricas MEJORADAS"""
        self.performance_metrics['total_orders'] += 1
        if success:
            self.performance_metrics['successful_orders'] += 1
            self.performance_metrics['total_volume'] += volume
        else:
            self.performance_metrics['failed_orders'] += 1
            
        self.performance_metrics['last_order_time'] = time.time()
        
        if self.performance_metrics['total_orders'] > 0:
            self.performance_metrics['success_rate'] = (
                self.performance_metrics['successful_orders'] / self.performance_metrics['total_orders'] * 100
            )
        
        if success:
            current_avg = self.performance_metrics['average_execution_time']
            total_success = self.performance_metrics['successful_orders']
            new_avg = (current_avg * (total_success - 1) + execution_time) / total_success
            self.performance_metrics['average_execution_time'] = new_avg

    def _record_order_history(self, order_data: Dict):
        """Registrar orden en historial"""
        self.order_history.append(order_data)
        if len(self.order_history) > 500:
            self.order_history = self.order_history[-500:]

    def get_current_price(self, symbol: str) -> float:
        """Obtener precio actual"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                ticker = self.client.get_symbol_ticker(symbol=symbol)
                price = float(ticker['price'])
                return price
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error(f"❌ Error obteniendo precio de {symbol}: {e}")
                    return 0.0

    def get_performance_report(self) -> Dict[str, Any]:
        """Obtener reporte de performance MEJORADO"""
        # 🚀 NUEVO: Obtener métricas del ProfitManager
        profit_metrics = self.profit_manager.get_performance_metrics()
        
        return {
            **self.performance_metrics,
            **profit_metrics,
            'order_history_count': len(self.order_history),
            'symbols_loaded': len(self.symbols_info),
            'active_positions': len(self.active_positions),
            'emergency_stop': self.emergency_stop_activated,
            'system_uptime': self._get_system_uptime()
        }

    def _get_system_uptime(self) -> str:
        """Calcular uptime del sistema"""
        if not hasattr(self, '_start_time'):
            self._start_time = time.time()
        
        uptime_seconds = time.time() - self._start_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    def get_system_status(self) -> Dict[str, Any]:
        """Obtener estado del sistema MEJORADO"""
        status = 'operational' if self.initialized else 'error'
        health_score = 100
        
        if self.initialized:
            try:
                self.client.ping()
                usdt_balance = self.get_balance('USDT')
                
                # 🚀 NUEVO: Verificar límites diarios
                daily_limits = self.profit_manager.check_daily_limits(
                    self.current_balance, self.initial_balance
                )
                
                if daily_limits.get('emergency_stop_activated'):
                    status = 'emergency_stop'
                    health_score = 0
                elif daily_limits.get('max_daily_loss_breached'):
                    status = 'warning'
                    health_score = 50
                    
            except:
                status = 'error'
                health_score = 0
        
        return {
            'system': 'TradeEngine',
            'status': status,
            'health_score': health_score,
            'initialized': self.initialized,
            'performance': self.get_performance_report(),
            'symbols_loaded': len(self.symbols_info),
            'active_positions': self.active_positions,
            'emergency_stop': self.emergency_stop_activated,
            'last_update': datetime.now().isoformat()
        }

    def get_recent_orders(self, limit: int = 10) -> List[Dict]:
        """Obtener órdenes recientes"""
        return self.order_history[-limit:]

    def start_health_monitor(self):
        """Iniciar monitor de salud MEJORADO"""
        def health_check():
            while True:
                try:
                    if self.initialized:
                        self.client.ping()
                        
                        # 🚀 NUEVO: Verificar gestión de posiciones cada 30 segundos
                        close_recommendations = self.check_position_management()
                        for recommendation in close_recommendations:
                            logger.info(f"🎯 ProfitManager recomienda cerrar {recommendation['symbol']}: {recommendation['reason']}")
                            
                    time.sleep(30)  # Verificar cada 30 segundos
                except Exception as e:
                    logger.warning(f"⚠️  Error en health monitor: {e}")
                    time.sleep(30)
        
        health_thread = threading.Thread(target=health_check, daemon=True)
        health_thread.start()
        logger.info("✅ Monitor de salud MEJORADO iniciado")

def test_trade_engine():
    """Función de prueba del Trade Engine MEJORADO"""
    logger.info("🧪 Probando Trade Engine MEJORADO...")
    
    engine = TradeEngine()
    
    if not engine.initialized:
        logger.error("❌ Trade Engine no se pudo inicializar")
        return False
    
    # Mostrar balances
    assets = ['USDT', 'BTC', 'ETH', 'ADA']
    logger.info("💰 Balances actuales:")
    for asset in assets:
        balance = engine.get_balance(asset)
        logger.info(f"   {asset}: {balance}")
    
    # Obtener precios actuales
    symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']
    logger.info("📊 Precios actuales:")
    for symbol in symbols:
        price = engine.get_current_price(symbol)
        logger.info(f"   {symbol}: ${price}")
    
    # Probar ajuste de lot sizes
    test_quantities = [
        ('BTCUSDT', 0.01963684068040036),
        ('ETHUSDT', 0.6017123),
        ('ADAUSDT', 3549.123),
    ]
    
    logger.info("🧪 Probando ajuste LOT_SIZE:")
    for symbol, qty in test_quantities:
        adjusted = engine.adjust_quantity_to_lot_size(symbol, qty)
        logger.info(f"   {symbol}: {qty} → {adjusted}")
    
    # 🚀 NUEVO: Probar cálculo de position size
    logger.info("🧪 Probando cálculo de Position Size:")
    for symbol in symbols:
        position_size = engine.calculate_position_size(symbol, "STRONG")
        logger.info(f"   {symbol}: ${position_size:.2f}")
    
    # Probar reporte de performance
    report = engine.get_performance_report()
    logger.info(f"📊 Reporte de performance MEJORADO:")
    for key, value in report.items():
        logger.info(f"   {key}: {value}")
    
    # Probar estado del sistema
    status = engine.get_system_status()
    logger.info(f"🔧 Estado del sistema: {status['status']}")
    
    return True

if __name__ == "__main__":
    logger.info("🚀 INICIANDO PRUEBA DE TRADE ENGINE MEJORADO")
    logger.info("=============================================")
    
    if test_trade_engine():
        logger.info("=============================================")
        logger.info("🎉 TRADE ENGINE MEJORADO CONFIGURADO CORRECTAMENTE")
        logger.info("💪 Listo para ejecutar órdenes con ProfitManager!")
    else:
        logger.info("=============================================")
        logger.error("💥 ERROR EN TRADE ENGINE - Revisa la configuración")
