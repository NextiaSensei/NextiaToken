#!/usr/bin/env python3
"""
Nextia Trading Bot - Trade Engine Mejorado
Motor de ejecución de órdenes de trading en Binance Testnet con mejoras de robustez
"""

import os
import sys
import json
import logging
import time
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TradeEngine:
    """Motor de ejecución de órdenes de trading mejorado con información REAL de Binance"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.initialized = False
        self.symbols_info: Dict[str, Dict] = {}
        self.order_history: List[Dict] = []
        self.performance_metrics = {
            'total_orders': 0,
            'successful_orders': 0,
            'failed_orders': 0,
            'total_volume': 0.0,
            'last_order_time': None,
            'average_execution_time': 0.0,
            'success_rate': 0.0
        }
        self.time_offset = 0  # SOLUCIÓN: Offset de tiempo global
        self.setup_binance_client()
        
    def setup_binance_client(self) -> bool:
        """Configurar cliente de Binance Testnet con manejo robusto de errores - VERSIÓN DEFINITIVA"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                load_dotenv()
                
                api_key = os.getenv('BINANCE_TESTNET_API_KEY')
                api_secret = os.getenv('BINANCE_TESTNET_SECRET_KEY')
                
                if not api_key or not api_secret:
                    logger.error("❌ API Keys no configuradas en .env")
                    return False
                
                # SOLUCIÓN DEFINITIVA: Configurar cliente sin time_offset inicial
                self.client = Client(
                    api_key=api_key,
                    api_secret=api_secret,
                    testnet=True,
                    requests_params={'timeout': 10}
                )
                
                # SOLUCIÓN CRÍTICA: Forzar sincronización de tiempo antes de cualquier operación
                self._force_time_sync()
                
                # Verificar conexión
                self.client.ping()
                logger.info("✅ Trade Engine conectado a Binance Testnet")
                self.initialized = True
                
                # Cargar información de símbolos
                self.load_symbols_info()
                return True
                
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    logger.error(f"❌ Error configurando Trade Engine después de {max_retries} intentos: {e}")
                    self.initialized = False
                    return False

    def _force_time_sync(self) -> bool:
        """
        SOLUCIÓN DEFINITIVA: Sincronización forzada de tiempo con compensación manual
        """
        try:
            # Obtener tiempo del servidor de Binance
            server_time = self.client.get_server_time()
            binance_time = server_time['serverTime']
            local_time = int(time.time() * 1000)
            
            # Calcular diferencia
            time_diff = binance_time - local_time
            logger.info(f"⏰ Diferencia de tiempo detectada: {time_diff}ms ({time_diff/1000:.1f} segundos)")
            
            # SOLUCIÓN MEJORADA: Si la diferencia es grande, usar compensación manual
            if abs(time_diff) > 5000:  # Más de 5 segundos
                logger.warning(f"🚨 Gran diferencia de tiempo: {time_diff}ms. Activando modo de compensación...")
                
                # MÉTODO DEFINITIVO: Usar compensación manual en cada request
                self.time_offset = time_diff
                logger.info(f"🔧 Time offset global configurado: {time_diff}ms")
                
                # Configurar recvWindow extendido
                self.client.recv_window = 60000  # 60 segundos
                logger.info("🔧 RecvWindow extendido a 60 segundos")
                
            else:
                # Diferencia pequeña, usar offset normal
                self.time_offset = time_diff
                logger.info("✅ Tiempo sincronizado correctamente")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en sincronización forzada: {e}")
            logger.info("🔄 Usando configuración básica sin sincronización...")
            # Fallback: usar offset de 0
            self.time_offset = 0
            return True  # Continuar de todos modos

    def _get_adjusted_timestamp(self) -> int:
        """
        SOLUCIÓN CRÍTICA: Obtener timestamp ajustado con el offset
        """
        return int(time.time() * 1000) + self.time_offset

    def load_symbols_info(self) -> bool:
        """Cargar información REAL de símbolos desde Binance con caché"""
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
        """Obtener filtros LOT_SIZE para un símbolo con reintentos"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                if symbol not in self.symbols_info:
                    # Intentar cargar información si no está disponible
                    self.load_symbols_info()
                    
                symbol_info = self.symbols_info.get(symbol)
                if not symbol_info:
                    logger.warning(f"⚠️  No hay información para {symbol}")
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
        """
        Ajusta la cantidad al tamaño de lote permitido por Binance
        USANDO INFORMACIÓN REAL DE LA API con validación mejorada
        """
        try:
            # Obtener filtros reales de Binance
            lot_size_filter = self.get_symbol_filters(symbol)
            
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
    
    def get_balance(self, asset: str = 'USDT') -> float:
        """Obtener balance de un activo con reintentos - VERSIÓN MEJORADA"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self.initialized:
                    return 0.0
                
                # SOLUCIÓN DEFINITIVA: Usar timestamp ajustado manualmente
                params = {
                    'recvWindow': 60000,
                    'timestamp': self._get_adjusted_timestamp()  # TIMESTAMP CORREGIDO
                }
                
                account = self.client.get_account(**params)
                for balance in account['balances']:
                    if balance['asset'] == asset:
                        free_balance = float(balance['free'])
                        logger.debug(f"💰 Balance {asset}: {free_balance}")
                        return free_balance
                return 0.0
                
            except BinanceAPIException as e:
                if "recvWindow" in str(e) or "timestamp" in str(e):
                    logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló por recvWindow/timestamp, intentando sin parámetros...")
                    try:
                        # Intentar sin parámetros
                        account = self.client.get_account()
                        for balance in account['balances']:
                            if balance['asset'] == asset:
                                free_balance = float(balance['free'])
                                return free_balance
                        return 0.0
                    except Exception as e2:
                        logger.warning(f"⚠️  Intento alternativo falló: {e2}")
                
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló obteniendo balance: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error(f"❌ Error obteniendo balance de {asset}: {e}")
                    return 0.0
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló obteniendo balance: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error(f"❌ Error obteniendo balance de {asset}: {e}")
                    return 0.0

    def execute_buy_order(self, symbol: str, quantity: float, order_type: str = 'MARKET') -> bool:
        """Ejecutar orden de compra con manejo robusto de errores"""
        start_time = time.time()
        order_success = False
        executed_price = 0.0
        
        try:
            if not self.initialized:
                logger.error("❌ Trade Engine no inicializado")
                return False
            
            # AJUSTAR CANTIDAD AL LOT SIZE REAL
            adjusted_quantity = self.adjust_quantity_to_lot_size(symbol, quantity)
            
            if adjusted_quantity <= 0:
                logger.error(f"❌ Cantidad ajustada inválida para {symbol}: {adjusted_quantity}")
                return False
            
            # Verificar balance suficiente
            quote_balance = self.get_balance('USDT')
            current_price = self.get_current_price(symbol)
            required_amount = adjusted_quantity * current_price
            
            if quote_balance < required_amount:
                logger.error(f"❌ Balance insuficiente. USDT disponible: {quote_balance}, necesario: {required_amount:.2f}")
                return False
            
            # DEBUG: Mostrar información antes de enviar
            logger.info(f"🔍 [DEBUG TRADE] Enviando COMPRA a Binance: {symbol} {adjusted_quantity}")
            
            # SOLUCIÓN DEFINITIVA: Usar timestamp ajustado manualmente
            order_params = {
                'symbol': symbol,
                'side': Client.SIDE_BUY,
                'type': order_type,
                'quantity': adjusted_quantity,
                'recvWindow': 60000,
                'timestamp': self._get_adjusted_timestamp()  # TIMESTAMP CORREGIDO
            }
            
            try:
                order = self.client.create_order(**order_params)
            except BinanceAPIException as e:
                if "recvWindow" in str(e) or "timestamp" in str(e):
                    logger.warning("⚠️  Error con recvWindow/timestamp, intentando sin parámetros...")
                    # Intentar sin parámetros de tiempo
                    order = self.client.create_order(
                        symbol=symbol,
                        side=Client.SIDE_BUY,
                        type=order_type,
                        quantity=adjusted_quantity
                    )
                else:
                    raise e
            
            # Procesar respuesta de la orden
            order_status = order.get('status', 'UNKNOWN')
            order_id = order.get('orderId', 'UNKNOWN')
            
            if order_status in ['FILLED', 'PARTIALLY_FILLED']:
                # Obtener precio de ejecución
                fills = order.get('fills', [])
                if fills:
                    executed_price = float(fills[0]['price'])
                    executed_qty = sum(float(fill['qty']) for fill in fills)
                    logger.info(f"💰 Precio ejecutado: {executed_price}, Cantidad: {executed_qty}")
                else:
                    executed_price = current_price
                
                order_success = True
                logger.info(f"✅ ORDEN EJECUTADA - COMPRA: {adjusted_quantity} {symbol}")
                logger.info(f"   📋 Order ID: {order_id}, Status: {order_status}")
                
            else:
                logger.warning(f"⚠️  Orden no ejecutada completamente: {order_status}")
                order_success = False
            
        except BinanceAPIException as e:
            logger.error(f"❌ Error de Binance API en orden de compra: {e}")
            order_success = False
        except BinanceOrderException as e:
            logger.error(f"❌ Error de orden en Binance: {e}")
            order_success = False
        except Exception as e:
            logger.error(f"❌ Error ejecutando orden de compra: {e}")
            order_success = False
        finally:
            # Actualizar métricas
            execution_time = time.time() - start_time
            self._update_order_metrics(order_success, adjusted_quantity * (executed_price or current_price), execution_time)
            
            # Registrar en historial
            self._record_order_history({
                'symbol': symbol,
                'side': 'BUY',
                'quantity': adjusted_quantity,
                'price': executed_price,
                'order_type': order_type,
                'success': order_success,
                'execution_time': execution_time,
                'timestamp': time.time()
            })
        
        return order_success

    def execute_sell_order(self, symbol: str, quantity: float, order_type: str = 'MARKET') -> bool:
        """Ejecutar orden de venta con manejo robusto de errores"""
        start_time = time.time()
        order_success = False
        executed_price = 0.0
        
        try:
            if not self.initialized:
                logger.error("❌ Trade Engine no inicializado")
                return False
            
            # AJUSTAR CANTIDAD AL LOT SIZE REAL
            adjusted_quantity = self.adjust_quantity_to_lot_size(symbol, quantity)
            
            if adjusted_quantity <= 0:
                logger.error(f"❌ Cantidad ajustada inválida para {symbol}: {adjusted_quantity}")
                return False
            
            # Verificar que tenemos el activo
            base_asset = symbol.replace('USDT', '')
            base_balance = self.get_balance(base_asset)
            
            if base_balance < adjusted_quantity:
                logger.error(f"❌ Balance insuficiente. {base_asset} disponible: {base_balance}, intentando vender: {adjusted_quantity}")
                return False
            
            # DEBUG: Mostrar información antes de enviar
            logger.info(f"🔍 [DEBUG TRADE] Enviando VENTA a Binance: {symbol} {adjusted_quantity}")
            
            # SOLUCIÓN DEFINITIVA: Usar timestamp ajustado manualmente
            order_params = {
                'symbol': symbol,
                'side': Client.SIDE_SELL,
                'type': order_type,
                'quantity': adjusted_quantity,
                'recvWindow': 60000,
                'timestamp': self._get_adjusted_timestamp()  # TIMESTAMP CORREGIDO
            }
            
            try:
                order = self.client.create_order(**order_params)
            except BinanceAPIException as e:
                if "recvWindow" in str(e) or "timestamp" in str(e):
                    logger.warning("⚠️  Error con recvWindow/timestamp, intentando sin parámetros...")
                    # Intentar sin parámetros de tiempo
                    order = self.client.create_order(
                        symbol=symbol,
                        side=Client.SIDE_SELL,
                        type=order_type,
                        quantity=adjusted_quantity
                    )
                else:
                    raise e
            
            # Procesar respuesta de la orden
            order_status = order.get('status', 'UNKNOWN')
            order_id = order.get('orderId', 'UNKNOWN')
            
            if order_status in ['FILLED', 'PARTIALLY_FILLED']:
                # Obtener precio de ejecución
                fills = order.get('fills', [])
                if fills:
                    executed_price = float(fills[0]['price'])
                    executed_qty = sum(float(fill['qty']) for fill in fills)
                    logger.info(f"💰 Precio ejecutado: {executed_price}, Cantidad: {executed_qty}")
                else:
                    executed_price = self.get_current_price(symbol)
                
                order_success = True
                logger.info(f"✅ ORDEN EJECUTADA - VENTA: {adjusted_quantity} {symbol}")
                logger.info(f"   📋 Order ID: {order_id}, Status: {order_status}")
                
            else:
                logger.warning(f"⚠️  Orden no ejecutada completamente: {order_status}")
                order_success = False
            
        except BinanceAPIException as e:
            logger.error(f"❌ Error de Binance API en orden de venta: {e}")
            order_success = False
        except BinanceOrderException as e:
            logger.error(f"❌ Error de orden en Binance: {e}")
            order_success = False
        except Exception as e:
            logger.error(f"❌ Error ejecutando orden de venta: {e}")
            order_success = False
        finally:
            # Actualizar métricas
            execution_time = time.time() - start_time
            self._update_order_metrics(order_success, adjusted_quantity * (executed_price or self.get_current_price(symbol)), execution_time)
            
            # Registrar en historial
            self._record_order_history({
                'symbol': symbol,
                'side': 'SELL',
                'quantity': adjusted_quantity,
                'price': executed_price,
                'order_type': order_type,
                'success': order_success,
                'execution_time': execution_time,
                'timestamp': time.time()
            })
        
        return order_success

    def _update_order_metrics(self, success: bool, volume: float, execution_time: float):
        """Actualizar métricas de órdenes"""
        self.performance_metrics['total_orders'] += 1
        if success:
            self.performance_metrics['successful_orders'] += 1
            self.performance_metrics['total_volume'] += volume
        else:
            self.performance_metrics['failed_orders'] += 1
            
        self.performance_metrics['last_order_time'] = time.time()
        
        # MEJORA: Calcular tasa de éxito
        if self.performance_metrics['total_orders'] > 0:
            self.performance_metrics['success_rate'] = (
                self.performance_metrics['successful_orders'] / self.performance_metrics['total_orders'] * 100
            )
        
        # Calcular tiempo promedio de ejecución
        if success:
            current_avg = self.performance_metrics['average_execution_time']
            total_success = self.performance_metrics['successful_orders']
            new_avg = (current_avg * (total_success - 1) + execution_time) / total_success
            self.performance_metrics['average_execution_time'] = new_avg

    def _record_order_history(self, order_data: Dict):
        """Registrar orden en historial"""
        self.order_history.append(order_data)
        
        # Limitar historial a últimos 500 órdenes
        if len(self.order_history) > 500:
            self.order_history = self.order_history[-500:]

    def get_current_price(self, symbol: str) -> float:
        """Obtener precio actual de un símbolo con reintentos"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                ticker = self.client.get_symbol_ticker(symbol=symbol)
                price = float(ticker['price'])
                logger.debug(f"📊 Precio actual {symbol}: {price}")
                return price
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló obteniendo precio: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error(f"❌ Error obteniendo precio de {symbol}: {e}")
                    return 0.0

    def get_performance_report(self) -> Dict[str, Any]:
        """Obtener reporte de performance completo"""
        return {
            **self.performance_metrics,
            'order_history_count': len(self.order_history),
            'symbols_loaded': len(self.symbols_info),
            'system_uptime': self._get_system_uptime()
        }

    def _get_system_uptime(self) -> str:
        """MEJORA: Calcular uptime del sistema"""
        if not hasattr(self, '_start_time'):
            self._start_time = time.time()
        
        uptime_seconds = time.time() - self._start_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    def get_system_status(self) -> Dict[str, Any]:
        """Obtener estado del sistema de trading"""
        status = 'operational' if self.initialized else 'error'
        
        # MEJORA: Verificar salud adicional
        if self.initialized:
            try:
                # Verificar conexión
                self.client.ping()
                # Verificar balances
                usdt_balance = self.get_balance('USDT')
                if usdt_balance is None:
                    status = 'degraded'
            except:
                status = 'error'
        
        return {
            'system': 'TradeEngine',
            'status': status,
            'initialized': self.initialized,
            'performance': self.get_performance_report(),
            'symbols_loaded': len(self.symbols_info),
            'last_update': datetime.now().isoformat()
        }

    def get_recent_orders(self, limit: int = 10) -> List[Dict]:
        """Obtener órdenes recientes"""
        return self.order_history[-limit:]

def test_trade_engine():
    """Función de prueba del Trade Engine Mejorado"""
    logger.info("🧪 Probando Trade Engine Mejorado...")
    
    engine = TradeEngine()
    
    if not engine.initialized:
        logger.error("❌ Trade Engine no se pudo inicializar")
        return False
    
    # Mostrar balances
    usdt_balance = engine.get_balance('USDT')
    btc_balance = engine.get_balance('BTC')
    eth_balance = engine.get_balance('ETH')
    ada_balance = engine.get_balance('ADA')
    
    logger.info(f"💰 Balances actuales:")
    logger.info(f"   USDT: {usdt_balance}")
    logger.info(f"   BTC: {btc_balance}")
    logger.info(f"   ETH: {eth_balance}")
    logger.info(f"   ADA: {ada_balance}")
    
    # Obtener precios actuales
    btc_price = engine.get_current_price('BTCUSDT')
    eth_price = engine.get_current_price('ETHUSDT')
    ada_price = engine.get_current_price('ADAUSDT')
    
    logger.info(f"📊 Precios actuales:")
    logger.info(f"   BTC/USDT: ${btc_price}")
    logger.info(f"   ETH/USDT: ${eth_price}")
    logger.info(f"   ADA/USDT: ${ada_price}")
    
    # Probar ajuste de lot sizes
    test_quantities = [
        ('BTCUSDT', 0.01963684068040036),
        ('ETHUSDT', 0.6017123),
        ('ADAUSDT', 3549.123),
    ]
    
    logger.info("🧪 Probando ajuste LOT_SIZE REAL:")
    for symbol, qty in test_quantities:
        adjusted = engine.adjust_quantity_to_lot_size(symbol, qty)
        logger.info(f"   {symbol}: {qty} → {adjusted}")
    
    # Probar reporte de performance
    report = engine.get_performance_report()
    logger.info(f"📊 Reporte de performance: {json.dumps(report, indent=2)}")
    
    # Probar estado del sistema
    status = engine.get_system_status()
    logger.info(f"🔧 Estado del sistema: {status['status']}")
    
    return True

if __name__ == "__main__":
    logger.info("🚀 INICIANDO PRUEBA DE TRADE ENGINE MEJORADO")
    logger.info("=====================================")
    
    if test_trade_engine():
        logger.info("=====================================")
        logger.info("🎉 TRADE ENGINE MEJORADO CONFIGURADO CORRECTAMENTE")
        logger.info("💪 Listo para ejecutar órdenes reales en Testnet!")
    else:
        logger.info("=====================================")
        logger.error("💥 ERROR EN TRADE ENGINE - Revisa la configuración")
