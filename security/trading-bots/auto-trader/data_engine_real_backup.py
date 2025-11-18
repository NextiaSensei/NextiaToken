#!/usr/bin/env python3
"""
Nextia Data Engine - VERSIÓN REAL CON BINANCE
Bot mejorado con risk manager y configuración optimizada
"""

import time
import sys
import os
import requests
import logging
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - DATA ENGINE REAL - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramSimple:
    """Telegram simple SIN asyncio"""
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    def send_message(self, message):
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Mensaje enviado a Telegram")
                return True
            else:
                logger.error(f"❌ Error Telegram: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Error enviando a Telegram: {e}")
            return False

class RealBinanceTrader:
    """Clase REAL para trading con Binance - MEJORADA"""
    
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY')
        self.client = None
        self.initial_balance = 0
        self.current_balance = 0
        self.total_trades = 0
        self.symbols_info = {}  # Cache para info de símbolos
        
        self.connect_to_binance()
        self.load_symbols_info()
    
    def connect_to_binance(self):
        """Conectar a Binance REAL"""
        try:
            self.client = Client(self.api_key, self.secret_key)
            
            # Obtener balance REAL
            account = self.client.get_account()
            usdt = next((a for a in account['balances'] if a['asset'] == 'USDT'), None)
            if usdt:
                self.initial_balance = float(usdt['free']) + float(usdt['locked'])
                self.current_balance = self.initial_balance
                
            logger.info(f"✅ Conectado a Binance REAL - Balance: ${self.initial_balance:.2f}")
            
            # Verificar trades existentes
            self.check_existing_trades()
            return True
            
        except Exception as e:
            logger.error(f"❌ Error conectando a Binance: {e}")
            return False

    def load_symbols_info(self):
        """Cargar información de símbolos para precisiones"""
        try:
            exchange_info = self.client.get_exchange_info()
            for symbol_info in exchange_info['symbols']:
                self.symbols_info[symbol_info['symbol']] = symbol_info
            logger.info(f"✅ Información de {len(self.symbols_info)} símbolos cargada")
        except Exception as e:
            logger.error(f"❌ Error cargando info de símbolos: {e}")

    def get_symbol_precision(self, symbol):
        """Obtener precisiones de cantidad y precio para un símbolo"""
        try:
            symbol_info = self.symbols_info.get(symbol)
            if symbol_info:
                # Encontrar el filtro LOT_SIZE
                for f in symbol_info['filters']:
                    if f['filterType'] == 'LOT_SIZE':
                        step_size = float(f['stepSize'])
                        # Calcular decimales basado en step_size
                        if step_size == 1.0:
                            return 0
                        elif step_size == 0.1:
                            return 1
                        elif step_size == 0.01:
                            return 2
                        elif step_size == 0.001:
                            return 3
                        elif step_size == 0.0001:
                            return 4
                        else:
                            return 8  # Por defecto
            return 2  # Por defecto
        except Exception as e:
            logger.error(f"❌ Error obteniendo precision: {e}")
            return 2

    def check_existing_trades(self):
        """Verificar trades reales existentes"""
        try:
            symbols_to_check = ['ADAUSDT', 'DOTUSDT', 'LINKUSDT', 'DOGEUSDT', 'SOLUSDT']
            total_trades = 0
            
            for symbol in symbols_to_check:
                try:
                    trades = self.client.get_my_trades(symbol=symbol, limit=10)
                    total_trades += len(trades)
                    if trades:
                        logger.info(f"📊 {symbol}: {len(trades)} trades reales")
                        for trade in trades[-2:]:
                            logger.info(f"   {trade['id']} {trade['side']} {trade['qty']} @ {trade['price']}")
                except:
                    continue
                    
            self.total_trades = total_trades
            logger.info(f"📈 Total de trades reales: {total_trades}")
            
        except Exception as e:
            logger.error(f"❌ Error verificando trades existentes: {e}")
    
    def get_real_price(self, symbol):
        """Obtener precio REAL de Binance"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            logger.error(f"❌ Error obteniendo precio de {symbol}: {e}")
            return None

    def adjust_quantity(self, symbol, quantity):
        """Ajustar cantidad según las reglas de Binance"""
        try:
            precision = self.get_symbol_precision(symbol)
            adjusted = round(quantity, precision)
            
            # Asegurar que cumple mínimo notional (normalmente $10)
            price = self.get_real_price(symbol)
            if price and adjusted * price < 10:
                min_quantity = 10 / price
                adjusted = round(min_quantity, precision)
                logger.info(f"🔧 Ajustada cantidad mínima: {adjusted}")
            
            return adjusted
        except Exception as e:
            logger.error(f"❌ Error ajustando cantidad: {e}")
            return quantity

    def execute_real_trade(self, symbol, side, quantity):
        """Ejecutar trade REAL en Binance - MEJORADO"""
        try:
            # Obtener precio actual
            price = self.get_real_price(symbol)
            if not price:
                return False, "Error obteniendo precio"
            
            # Calcular cantidad en base al balance (máximo 25% para risk management)
            max_trade_amount = self.current_balance * 0.25
            trade_amount = min(quantity * price, max_trade_amount)
            raw_quantity = trade_amount / price
            
            # Ajustar cantidad según reglas de Binance
            adjusted_quantity = self.adjust_quantity(symbol, raw_quantity)
            
            if adjusted_quantity <= 0:
                return False, "Cantidad muy pequeña después de ajustes"
            
            logger.info(f"🔄 Ejecutando orden REAL: {side} {adjusted_quantity:.6f} {symbol} @ ${price:.6f}")
            
            # Crear orden REAL en Binance
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=adjusted_quantity
            )
            
            # Actualizar balance y contador
            self.update_balance()
            self.total_trades += 1
            
            logger.info(f"✅ Orden REAL ejecutada: {order['orderId']}")
            return True, f"Orden {order['orderId']} ejecutada - {adjusted_quantity:.4f} {symbol}"
            
        except BinanceAPIException as e:
            logger.error(f"❌ Error Binance: {e}")
            return False, f"Error Binance: {e}"
        except Exception as e:
            logger.error(f"❌ Error ejecutando trade: {e}")
            return False, f"Error: {e}"
    
    def update_balance(self):
        """Actualizar balance REAL"""
        try:
            account = self.client.get_account()
            usdt = next((a for a in account['balances'] if a['asset'] == 'USDT'), None)
            if usdt:
                self.current_balance = float(usdt['free']) + float(usdt['locked'])
        except Exception as e:
            logger.error(f"❌ Error actualizando balance: {e}")

class DataEngineReal:
    def __init__(self):
        self.running = False
        self.telegram = TelegramSimple()
        self.binance_trader = RealBinanceTrader()
        self.trades_today = 0
        self.max_daily_trades = 3
        
    def start(self):
        """Iniciar el motor de datos REAL"""
        logger.info("🚀 INICIANDO NEXTIA DATA ENGINE - MODO REAL MEJORADO...")
        
        # Mensaje de inicio mejorado
        self.telegram.send_message(
            "🚀 *Nextia Trading Bot REINICIADO - MODO REAL*\n"
            f"💰 Balance actual: ${self.binance_trader.current_balance:.2f}\n"
            f"📊 Trades históricos: {self.binance_trader.total_trades}\n"
            f"🎯 Límite diario: {self.max_daily_trades} trades\n"
            "✅ Sistema mejorado con risk management"
        )
        
        self.running = True
        self.main_loop()
        
    def stop(self):
        """Detener el motor de datos"""
        logger.info("🛑 DETENIENDO Nextia Data Engine...")
        self.telegram.send_message(
            "🛑 *Nextia Trading Bot DETENIDO*\n"
            f"💰 Balance final: ${self.binance_trader.current_balance:.2f}\n"
            f"📈 Trades hoy: {self.trades_today}"
        )
        self.running = False
        
    def main_loop(self):
        """Bucle principal REAL MEJORADO"""
        logger.info("📊 Motor de datos REAL ejecutándose...")
        
        last_trade_time = 0
        trade_interval = 600  # 10 minutos entre trades (más conservador)
        
        try:
            while self.running:
                current_time = time.time()
                
                # Verificar si podemos hacer más trades hoy
                if (self.trades_today >= self.max_daily_trades):
                    logger.info(f"🎯 Límite diario alcanzado: {self.trades_today}/{self.max_daily_trades}")
                    time.sleep(60)
                    continue
                
                # Ejecutar trades REALES periódicamente
                if current_time - last_trade_time >= trade_interval and self.binance_trader.client:
                    if self.execute_real_trading_strategy():
                        last_trade_time = current_time
                        self.trades_today += 1
                
                time.sleep(10)  # Check cada 10 segundos
                
        except KeyboardInterrupt:
            logger.info("🛑 Señal de interrupción recibida")
        except Exception as e:
            logger.error(f"❌ Error en motor de datos: {e}")
            self.telegram.send_message(f"🚨 *Error en Data Engine:* {e}")
        finally:
            self.stop()
            
    def execute_real_trading_strategy(self):
        """Estrategia de trading REAL mejorada"""
        symbols = ['ADAUSDT', 'DOTUSDT', 'LINKUSDT', 'DOGEUSDT']  # Símbolos probados
        
        for symbol in symbols:
            try:
                # Verificar balance mínimo
                if self.binance_trader.current_balance < 5:
                    logger.warning("💰 Balance muy bajo para trading")
                    return False
                
                # Obtener precio REAL
                current_price = self.binance_trader.get_real_price(symbol)
                if not current_price:
                    continue
                
                # Estrategia conservadora: Solo operar si tenemos suficiente balance
                trade_amount = self.binance_trader.current_balance * 0.15  # 15% del balance
                quantity = trade_amount / current_price
                
                if quantity * current_price < 5:  # Mínimo $5 por trade
                    logger.info(f"⚖️  Trade muy pequeño para {symbol}, saltando...")
                    continue
                
                # EJECUTAR ORDEN REAL DE COMPRA
                success, message = self.binance_trader.execute_real_trade(
                    symbol=symbol, 
                    side='BUY', 
                    quantity=quantity
                )
                
                if success:
                    # Notificar en Telegram
                    self.telegram.send_message(
                        f"✅ *TRADE REAL EJECUTADO*\n"
                        f"🔼 {symbol} COMPRA\n"
                        f"💵 Cantidad: {quantity:.2f}\n"
                        f"📈 Precio: ${current_price:.4f}\n"
                        f"💰 Costo: ${quantity * current_price:.2f}\n"
                        f"💼 Balance: ${self.binance_trader.current_balance:.2f}\n"
                        f"📊 Trade #{self.trades_today + 1} de {self.max_daily_trades}"
                    )
                    
                    # Esperar 2 minutos y vender (estrategia simple)
                    logger.info("⏳ Esperando 2 minutos para venta...")
                    time.sleep(120)
                    
                    # Obtener nuevo precio para venta
                    new_price = self.binance_trader.get_real_price(symbol)
                    
                    # EJECUTAR ORDEN REAL DE VENTA
                    sell_success, sell_message = self.binance_trader.execute_real_trade(
                        symbol=symbol, 
                        side='SELL', 
                        quantity=quantity * 0.995  # Vender 99.5% para comisiones
                    )
                    
                    if sell_success:
                        profit = self.binance_trader.current_balance - self.binance_trader.initial_balance
                        self.telegram.send_message(
                            f"💰 *TRADE CERRADO*\n"
                            f"🔽 {symbol} VENTA\n"
                            f"📈 Precio venta: ${new_price:.4f}\n"
                            f"📊 Profit acumulado: ${profit:.2f}\n"
                            f"💼 Balance actual: ${self.binance_trader.current_balance:.2f}\n"
                            f"🎯 Trades hoy: {self.trades_today + 1}/{self.max_daily_trades}"
                        )
                        return True
                    
                break  # Solo un trade a la vez
                    
            except Exception as e:
                logger.error(f"❌ Error en estrategia para {symbol}: {e}")
                continue
        
        return False

def main():
    """Función principal REAL MEJORADA"""
    print("🤖 NEXTIA TRADING BOT - DATA ENGINE REAL MEJORADO")
    print("=" * 50)
    print("🚀 MODO REAL CON BINANCE ACTIVADO")
    print("💰 Trading con dinero REAL")
    print("🎯 Risk Management: 25% máximo por trade")
    print("📊 Límite: 3 trades por día")
    print("💡 Presiona Ctrl+C para detener")
    print("=" * 50)
    
    engine = DataEngineReal()
    
    try:
        engine.start()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo motor de datos...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        engine.stop()

if __name__ == "__main__":
    main()
