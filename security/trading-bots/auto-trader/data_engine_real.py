#!/usr/bin/env python3
"""
Nextia Trading Bot - VERSIÓN AGGRESSIVE 
Combinación perfecta: Tus tokens + Estrategia más agresiva
"""

import time
import sys
import os
import requests
import logging
import sqlite3
import random
import ta
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [NEXTIA] %(message)s',
    handlers=[
        logging.FileHandler('nextia_trading.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

class AggressiveAnalyzer:
    """Analizador MÁS AGRESIVO para más oportunidades"""
    
    def __init__(self, binance_manager):
        self.binance = binance_manager
    
    def get_klines(self, symbol, interval='3m', limit=30):  # MENOS tiempo
        """Obtener datos de velas optimizado"""
        try:
            klines = self.binance.client.get_klines(
                symbol=symbol, 
                interval=interval, 
                limit=limit
            )
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
                
            return df
        except Exception as e:
            logger.error(f"❌ Error klines {symbol}: {e}")
            return None

    def get_aggressive_signal(self, symbol):
        """Señal AGRESIVA - MÁS oportunidades de trading"""
        try:
            df = self.get_klines(symbol, '3m', 15)  # Menos datos, más rápido
            if df is None or len(df) < 10:
                return "BUY", 0.7  # Más agresivo: si no hay datos, comprar igual
            
            # Indicadores SIMPLIFICADOS
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=10).rsi()  # RSI más rápido
            
            current_rsi = df['rsi'].iloc[-1]
            current_price = df['close'].iloc[-1]
            
            # ESTRATEGIA MÁS AGRESIVA
            # Compra si RSI < 60 (mucho más flexible)
            # O si el precio está en mínimos recientes
            price_change_5m = (current_price - df['close'].iloc[-5]) / df['close'].iloc[-5] * 100
            
            logger.info(f"📊 {symbol} - RSI: {current_rsi:.1f}, Change 5m: {price_change_5m:.2f}%")
            
            # CONDICIONES DE COMPRA MÁS FLEXIBLES
            if current_rsi < 60:  # Más flexible que 45
                if price_change_5m < -1.0:  # Si bajó 1% en 5min
                    confidence = 0.8
                    return "BUY", confidence
                elif current_rsi < 50:  # RSI neutral-bajo
                    confidence = 0.75
                    return "BUY", confidence
                else:
                    confidence = 0.7
                    return "BUY", confidence
            else:
                # Si RSI alto, pero el precio bajó recientemente
                if price_change_5m < -2.0:
                    confidence = 0.7
                    return "BUY", confidence
            
            return "WAIT", 0.0
                
        except Exception as e:
            logger.error(f"❌ Error análisis {symbol}: {e}")
            return "BUY", 0.7  # MUY AGRESIVO: si hay error, comprar igual

class TelegramManager:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    def send_message(self, message):
        for attempt in range(3):
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendMessage"
                payload = {
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    logger.info("✅ Telegram: Mensaje enviado")
                    return True
                time.sleep(2)
            except Exception as e:
                logger.warning(f"⚠️ Telegram falló: {e}")
                time.sleep(2)
        logger.error("❌ No se pudo enviar a Telegram")
        return False

class BinanceManager:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY')
        self.client = None
        self.symbols_info = {}
        self.connect()
    
    def connect(self):
        try:
            self.client = Client(self.api_key, self.secret_key)
            self.client.ping()
            logger.info("✅ Binance conectado")
            self.load_symbols_info()
            return True
        except Exception as e:
            logger.error(f"❌ Error Binance: {e}")
            return False

    def load_symbols_info(self):
        try:
            exchange_info = self.client.get_exchange_info()
            for symbol_info in exchange_info['symbols']:
                self.symbols_info[symbol_info['symbol']] = symbol_info
            logger.info(f"📊 {len(self.symbols_info)} símbolos cargados")
        except Exception as e:
            logger.error(f"❌ Error cargando símbolos: {e}")

    def get_available_balance(self):
        try:
            account = self.client.get_account()
            usdt = next((a for a in account['balances'] if a['asset'] == 'USDT'), None)
            if usdt:
                available = float(usdt['free'])
                logger.info(f"💰 USDT disponible: ${available:.2f}")
                return available
            return 0.0
        except Exception as e:
            logger.error(f"❌ Error obteniendo balance: {e}")
            return 0.0

    def get_asset_balance(self, asset):
        try:
            account = self.client.get_account()
            balance = next((a for a in account['balances'] if a['asset'] == asset), None)
            if balance:
                return float(balance['free'])
            return 0.0
        except Exception as e:
            logger.error(f"❌ Error obteniendo balance de {asset}: {e}")
            return 0.0

    def get_current_price(self, symbol):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            return price
        except Exception as e:
            logger.error(f"❌ Error precio {symbol}: {e}")
            return None

    def get_symbol_filters(self, symbol):
        return self.symbols_info.get(symbol, {}).get('filters', [])

    def get_min_quantity(self, symbol):
        filters = self.get_symbol_filters(symbol)
        for f in filters:
            if f['filterType'] == 'LOT_SIZE':
                return float(f['minQty'])
        return 0.0

    def get_min_notional(self, symbol):
        filters = self.get_symbol_filters(symbol)
        for f in filters:
            if f['filterType'] == 'MIN_NOTIONAL':
                return float(f['minNotional'])
        return 5.0

    def adjust_quantity(self, symbol, desired_quantity):
        try:
            min_qty = self.get_min_quantity(symbol)
            filters = self.get_symbol_filters(symbol)
            
            for f in filters:
                if f['filterType'] == 'LOT_SIZE':
                    step_size = float(f['stepSize'])
                    adjusted = int(desired_quantity / step_size) * step_size
                    adjusted = round(adjusted, 8)
                    
                    if adjusted < min_qty:
                        adjusted = min_qty
                    
                    return adjusted
            return desired_quantity
        except Exception as e:
            logger.error(f"❌ Error ajustando cantidad: {e}")
            return desired_quantity

    def find_viable_symbols_for_low_balance(self, balance, max_symbols=15):
        """BUSCAR SÍMBOLOS - MÁS AGRESIVO"""
        viable_symbols = []
        
        # TUS TOKENS + SÍMBOLOS LÍQUIDOS
        test_symbols = [
            # TUS TOKENS DE EARN
            'PEPEUSDT', 'BERAUSDT', 'PENGUUSDT', 'VANAUSDT', 
            'LAYERUSDT', 'BIOUSDT', 'REZUSDT', 'ANIMEUSDT', 
            'PIXELUSDT', '1000CATUSDT', 'SHELLUSDT',
            
            # SÍMBOLOS LÍQUIDOS PARA BACKUP
            'DOGEUSDT', 'TRXUSDT', 'VETUSDT', 'SHIBUSDT',
            'SFPUSDT', 'ONGUSDT', 'CHRUSDT', 'MATICUSDT', 'LTCUSDT'
        ]
        
        logger.info(f"🔍 Buscando símbolos viables para ${balance:.2f}...")
        
        for symbol in test_symbols:
            try:
                price = self.get_current_price(symbol)
                if not price:
                    continue
                    
                min_qty = self.get_min_quantity(symbol)
                min_notional = self.get_min_notional(symbol)
                
                # Para balance bajo, usar 50% del balance (MÁS AGRESIVO)
                trade_amount = balance * 0.5
                
                # Verificar viabilidad
                if (trade_amount >= min_notional and 
                    trade_amount >= (min_qty * price)):
                    
                    viable_symbols.append(symbol)
                    logger.info(f"✅ {symbol} - Precio: ${price:.4f}")
                    
                    if len(viable_symbols) >= max_symbols:
                        break
                        
            except Exception as e:
                continue
                
        return viable_symbols

    def execute_trade(self, symbol, side, quantity):
        try:
            price = self.get_current_price(symbol)
            if not price:
                return False, "No se pudo obtener precio"
            
            adjusted_quantity = self.adjust_quantity(symbol, quantity)
            
            trade_value = adjusted_quantity * price
            min_notional = self.get_min_notional(symbol)
            
            if trade_value < min_notional:
                required_quantity = min_notional / price
                adjusted_quantity = self.adjust_quantity(symbol, required_quantity)
                logger.info(f"🔧 Ajustando al mínimo: {adjusted_quantity:.6f} {symbol}")
            
            logger.info(f"🔄 Ejecutando {side} {adjusted_quantity:.6f} {symbol}")
            
            order = self.client.create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=adjusted_quantity
            )
            
            logger.info(f"✅ Orden ejecutada: {order['orderId']}")
            
            executed_price = float(order['fills'][0]['price']) if order.get('fills') else price
            
            return True, {
                'symbol': symbol,
                'side': side,
                'quantity': adjusted_quantity,
                'price': executed_price,
                'order_id': order['orderId']
            }
            
        except BinanceAPIException as e:
            error_msg = f"Error Binance: {e}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Error ejecutando trade: {e}"
            logger.error(error_msg)
            return False, error_msg

class TradingBot:
    def __init__(self):
        self.running = False
        self.telegram = TelegramManager()
        self.binance = BinanceManager()
        self.analyzer = AggressiveAnalyzer(self.binance)
        
        # CONFIGURACIÓN SUPER AGRESIVA
        self.config = {
            'max_daily_trades': 12,  # MÁS trades
            'min_balance_required': 2.0,
            'base_risk': 0.5,  # 50% por trade - MÁS AGRESIVO
            'take_profit': 0.015,  # 1.5%
            'stop_loss': 0.008,    # 0.8%
            'max_hold_time': 180,  # 3 minutos (MENOS tiempo)
            'scan_interval': 30,   # 30 segundos entre escaneos (MÁS RÁPIDO)
            'min_confidence': 0.5  # 50% confianza mínima (MENOS)
        }
        
        self.trades_today = 0
        self.starting_balance = 0
        self.current_balance = 0
        self.consecutive_losses = 0

    def start(self):
        logger.info("🚀 INICIANDO NEXTIA BOT - VERSIÓN AGRESIVA")
        
        if not self.binance.connect():
            return False
        
        self.starting_balance = self.binance.get_available_balance()
        self.current_balance = self.starting_balance
        
        if self.starting_balance < self.config['min_balance_required']:
            logger.error(f"❌ Balance insuficiente: ${self.starting_balance:.2f}")
            return False
        
        # BUSCAR SÍMBOLOS VIABLES
        viable_symbols = self.binance.find_viable_symbols_for_low_balance(self.current_balance)
        
        if not viable_symbols:
            logger.error("❌ No se encontraron símbolos viables")
            viable_symbols = ['PEPEUSDT', 'BERAUSDT', 'DOGEUSDT', 'TRXUSDT', 'MATICUSDT']
            logger.info(f"🆘 Usando símbolos de emergencia: {viable_symbols}")
        
        self.viable_symbols = viable_symbols
        
        self.telegram.send_message(
            f"🚀 *Nextia Bot VERSIÓN AGRESIVA INICIADO*\n\n"
            f"💰 *Balance:* ${self.starting_balance:.2f}\n"
            f"🎯 *Símbolos:* {len(viable_symbols)}\n"
            f"📊 *Top 5:* {', '.join(viable_symbols[:5])}\n"
            f"⚡ *Risk:* {self.config['base_risk']*100}%\n"
            f"📈 *Take Profit:* {self.config['take_profit']*100}%\n"
            f"🛑 *Stop Loss:* {self.config['stop_loss']*100}%\n"
            f"⏱️ *Hold Time:* {self.config['max_hold_time']}s"
        )
        
        self.running = True
        self.trading_loop()
        return True

    def stop(self):
        logger.info("🛑 DETENIENDO BOT")
        final_balance = self.binance.get_available_balance()
        total_pnl = final_balance - self.starting_balance
        
        self.telegram.send_message(
            f"🛑 *Bot Detenido*\n\n"
            f"💰 *Balance inicial:* ${self.starting_balance:.2f}\n"
            f"💰 *Balance final:* ${final_balance:.2f}\n"
            f"📈 *PnL total:* ${total_pnl:.4f}\n"
            f"📊 *Rendimiento:* {(total_pnl/self.starting_balance)*100:.2f}%\n"
            f"🎯 *Trades hoy:* {self.trades_today}"
        )
        
        self.running = False

    def execute_trading_cycle(self, symbol):
        """Ciclo de trading AGRESIVO"""
        try:
            signal, confidence = self.analyzer.get_aggressive_signal(symbol)
            
            # MÁS AGRESIVO: Si confianza > 50%, operar
            if signal == "WAIT" or confidence < self.config['min_confidence']:
                logger.info(f"⏭️  Saltando {symbol} - Señal: {signal}, Confianza: {confidence:.2f}")
                return False
            
            price = self.binance.get_current_price(symbol)
            if not price:
                return False
            
            # Calcular cantidad (50% del balance - MÁS AGRESIVO)
            trade_usd = self.current_balance * self.config['base_risk']
            quantity = trade_usd / price
            
            logger.info(f"🎯 Ejecutando {signal} en {symbol}")
            logger.info(f"   - Precio: ${price:.6f}")
            logger.info(f"   - Trade USD: ${trade_usd:.2f}")
            logger.info(f"   - Cantidad: {quantity:.2f}")
            logger.info(f"   - Confianza: {confidence:.2f}")
            
            # COMPRA
            buy_success, buy_result = self.binance.execute_trade(symbol, 'BUY', quantity)
            
            if not buy_success:
                logger.error(f"❌ Error compra: {buy_result}")
                return False
            
            buy_price = buy_result['price']
            buy_quantity = buy_result['quantity']
            
            self.telegram.send_message(
                f"✅ *COMPRA AGRESIVA EJECUTADA*\n\n"
                f"🔼 *Símbolo:* {symbol}\n"
                f"💵 *Cantidad:* {buy_quantity:.2f}\n"
                f"💰 *Precio:* ${buy_price:.6f}\n"
                f"💯 *Confianza:* {confidence:.1%}\n"
                f"📈 *Take Profit:* {self.config['take_profit']*100}%\n"
                f"🛑 *Stop Loss:* {self.config['stop_loss']*100}%"
            )
            
            # GESTIÓN DE LA POSICIÓN (MÁS CORTA)
            logger.info(f"⏳ Monitoreando posición por {self.config['max_hold_time']}s...")
            
            start_time = time.time()
            best_price = buy_price
            exit_reason = "TIME"
            
            while time.time() - start_time < self.config['max_hold_time']:
                current_price = self.binance.get_current_price(symbol)
                if current_price:
                    price_change = (current_price - buy_price) / buy_price
                    
                    # Take Profit
                    if price_change >= self.config['take_profit']:
                        logger.info(f"🎯 Take Profit: +{price_change*100:.2f}%")
                        exit_reason = "PROFIT"
                        break
                    
                    # Stop Loss
                    if price_change <= -self.config['stop_loss']:
                        logger.info(f"🛑 Stop Loss: {price_change*100:.2f}%")
                        exit_reason = "LOSS"
                        break
                    
                    if current_price > best_price:
                        best_price = current_price
                
                time.sleep(5)  # Chequeo más frecuente
            
            # VENTA
            asset = symbol.replace('USDT', '')
            sell_quantity = self.binance.get_asset_balance(asset)
            
            if sell_quantity <= 0:
                logger.error(f"❌ Balance de {asset} es cero")
                return False
            
            logger.info(f"💼 Vendiendo: {sell_quantity:.6f} {asset}")
            
            sell_success, sell_result = self.binance.execute_trade(symbol, 'SELL', sell_quantity)
            
            if not sell_success:
                logger.error(f"❌ Error venta: {sell_result}")
                return False
            
            # Calcular PnL
            sell_price = sell_result['price']
            pnl = (sell_price * sell_quantity) - (buy_price * buy_quantity)
            
            # Actualizar estadísticas
            if pnl > 0:
                self.consecutive_losses = 0
            else:
                self.consecutive_losses += 1
            
            self.current_balance = self.binance.get_available_balance()
            self.trades_today += 1
            
            # Notificación de resultado
            status = "✅ GANADOR" if pnl > 0 else "❌ PERDEDOR"
            
            self.telegram.send_message(
                f"💰 *TRADE CERRADO - {status}*\n\n"
                f"🔽 *Símbolo:* {symbol}\n"
                f"📊 *Razón:* {exit_reason}\n"
                f"💵 *Compra:* ${buy_price:.6f}\n"
                f"💵 *Venta:* ${sell_price:.6f}\n"
                f"📈 *Cambio:* {(sell_price-buy_price)/buy_price*100:+.3f}%\n"
                f"💰 *PnL:* ${pnl:.4f}\n"
                f"💼 *Balance:* ${self.current_balance:.2f}\n"
                f"📊 *Pérdidas consecutivas:* {self.consecutive_losses}"
            )
            
            logger.info(f"💰 Trade completado: PnL = ${pnl:.4f}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en ciclo: {e}")
            return False

    def trading_loop(self):
        """Loop principal SUPER AGRESIVO"""
        last_trade_time = 0
        
        while self.running:
            try:
                current_time = time.time()
                self.current_balance = self.binance.get_available_balance()
                
                # Verificaciones básicas
                if self.current_balance < self.config['min_balance_required']:
                    logger.warning(f"💰 Balance bajo: ${self.current_balance:.2f}")
                    time.sleep(30)
                    continue
                
                if self.trades_today >= self.config['max_daily_trades']:
                    logger.info(f"🎯 Límite diario: {self.trades_today}/{self.config['max_daily_trades']}")
                    time.sleep(60)
                    continue
                
                # Pausa después de pérdidas (MENOS restrictiva)
                if self.consecutive_losses >= 4:  # Más pérdidas permitidas
                    logger.warning(f"⏸️  {self.consecutive_losses} pérdidas - Pausa 5min")
                    time.sleep(300)
                    self.consecutive_losses = 0
                    continue
                
                # Intervalo entre trades (MENOS tiempo)
                if current_time - last_trade_time < self.config['scan_interval']:
                    time.sleep(5)
                    continue
                
                # SELECCIONAR SÍMBOLO ALEATORIO
                if not hasattr(self, 'viable_symbols') or not self.viable_symbols:
                    self.viable_symbols = self.binance.find_viable_symbols_for_low_balance(self.current_balance)
                
                if not self.viable_symbols:
                    logger.warning("⏳ No hay símbolos viables, esperando...")
                    time.sleep(30)
                    continue
                
                symbol = random.choice(self.viable_symbols)
                logger.info(f"🎯 Probando {symbol}...")
                
                if self.execute_trading_cycle(symbol):
                    last_trade_time = current_time
                    logger.info(f"📈 Trade #{self.trades_today} completado")
                
                time.sleep(5)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"❌ Error en loop: {e}")
                time.sleep(10)

def main():
    print("🤖 NEXTIA TRADING BOT - VERSIÓN SUPER AGRESIVA")
    print("=" * 60)
    print("🚀 Optimizado para MÁXIMAS OPORTUNIDADES")
    print("💰 Usa tus tokens + símbolos líquidos")
    print("🎯 Estrategia: RSI flexible + precio momentum")
    print("📈 Take Profit: 1.5% | Stop Loss: 0.8%")
    print("⏱️  Hold time: 3 minutos máximo")
    print("🔄 Busca oportunidades cada 30 segundos")
    print("⚡ Risk: 50% por trade")
    print("=" * 60)
    
    bot = TradingBot()
    
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo bot...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        bot.stop()

if __name__ == "__main__":
    main()
