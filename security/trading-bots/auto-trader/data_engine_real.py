#!/usr/bin/env python3
"""
Nextia Trading Bot - VERSIÓN COMUNITARIA DEFINITIVA
Ecosistema Nextia - Código Abierto para la Comunidad
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

# Configuración de logging MEJORADA
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
    """Analizador MÁS AGRESIVO para más oportunidades - OPTIMIZADO"""
    
    def __init__(self, binance_manager):
        self.binance = binance_manager
        self.last_analysis = {}
    
    def get_klines(self, symbol, interval='3m', limit=25):
        """Obtener datos de velas optimizado con cache"""
        try:
            # Cache simple para evitar llamadas repetidas
            cache_key = f"{symbol}_{interval}"
            if cache_key in self.last_analysis and time.time() - self.last_analysis[cache_key]['timestamp'] < 10:
                return self.last_analysis[cache_key]['data']
            
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
            
            # Guardar en cache
            self.last_analysis[cache_key] = {
                'timestamp': time.time(),
                'data': df
            }
                
            return df
        except Exception as e:
            logger.error(f"❌ Error klines {symbol}: {e}")
            return None

    def get_aggressive_signal(self, symbol):
        """Señal AGRESIVA OPTIMIZADA - MÁXIMAS OPORTUNIDADES"""
        try:
            df = self.get_klines(symbol, '3m', 15)
            if df is None or len(df) < 8:
                return "BUY", 0.75
            
            # Indicadores RÁPIDOS
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=10).rsi()
            df['ema_12'] = ta.trend.EMAIndicator(df['close'], window=12).ema_indicator()
            
            current_rsi = df['rsi'].iloc[-1]
            current_price = df['close'].iloc[-1]
            prev_price = df['close'].iloc[-2]
            
            # Cálculos rápidos
            price_change = ((current_price - prev_price) / prev_price) * 100
            volume_avg = df['volume'].tail(5).mean()
            current_volume = df['volume'].iloc[-1]
            
            logger.info(f"📊 {symbol} - RSI: {current_rsi:.1f}, Change: {price_change:+.2f}%")
            
            # ESTRATEGIA HIPER AGRESIVA
            buy_signals = 0
            
            # Señal 1: RSI flexible
            if current_rsi < 65:
                buy_signals += 2
            elif current_rsi < 75 and price_change < -1.5:
                buy_signals += 1
                
            # Señal 2: Momentum positivo
            if price_change < -0.8:
                buy_signals += 2
            elif current_price > df['ema_12'].iloc[-1]:
                buy_signals += 1
                
            # Señal 3: Volumen
            if current_volume > volume_avg * 1.2:
                buy_signals += 1
            
            # DECISIÓN FINAL
            if buy_signals >= 3:
                confidence = min(0.6 + (buy_signals * 0.1), 0.85)
                return "BUY", confidence
            elif buy_signals >= 2 and current_rsi < 55:
                return "BUY", 0.65
                
            return "WAIT", 0.0
                
        except Exception as e:
            logger.error(f"❌ Error análisis {symbol}: {e}")
            return "BUY", 0.7

class TelegramManager:
    """Gestor de Telegram MEJORADO"""
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    def send_message(self, message):
        """Enviar mensaje con formato mejorado"""
        for attempt in range(3):
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendMessage"
                payload = {
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
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
    """Gestor de Binance OPTIMIZADO"""
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY')
        self.client = None
        self.symbols_info = {}
        self.price_cache = {}
        self.connect()
    
    def connect(self):
        """Conectar a Binance con reintentos"""
        for attempt in range(3):
            try:
                self.client = Client(self.api_key, self.secret_key)
                self.client.ping()
                logger.info("✅ Binance conectado")
                self.load_symbols_info()
                return True
            except Exception as e:
                logger.error(f"❌ Error Binance (intento {attempt + 1}): {e}")
                if attempt < 2:
                    time.sleep(5)
        return False

    def load_symbols_info(self):
        """Cargar información de símbolos"""
        try:
            exchange_info = self.client.get_exchange_info()
            for symbol_info in exchange_info['symbols']:
                self.symbols_info[symbol_info['symbol']] = symbol_info
            logger.info(f"📊 {len(self.symbols_info)} símbolos cargados")
        except Exception as e:
            logger.error(f"❌ Error cargando símbolos: {e}")

    def get_available_balance(self):
        """Obtener USDT disponible"""
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
        """Obtener balance de un asset"""
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
        """Obtener precio actual con cache"""
        try:
            # Cache de 5 segundos para precios
            if symbol in self.price_cache and time.time() - self.price_cache[symbol]['timestamp'] < 5:
                return self.price_cache[symbol]['price']
                
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            
            self.price_cache[symbol] = {
                'timestamp': time.time(),
                'price': price
            }
            
            return price
        except Exception as e:
            logger.error(f"❌ Error precio {symbol}: {e}")
            return None

    def get_symbol_filters(self, symbol):
        """Obtener filtros del símbolo"""
        return self.symbols_info.get(symbol, {}).get('filters', [])

    def get_min_quantity(self, symbol):
        """Obtener cantidad mínima"""
        filters = self.get_symbol_filters(symbol)
        for f in filters:
            if f['filterType'] == 'LOT_SIZE':
                return float(f['minQty'])
        return 0.0

    def get_min_notional(self, symbol):
        """Obtener valor mínimo de trade"""
        filters = self.get_symbol_filters(symbol)
        for f in filters:
            if f['filterType'] == 'MIN_NOTIONAL':
                return float(f['minNotional'])
        return 5.0

    def adjust_quantity(self, symbol, desired_quantity):
        """Ajustar cantidad según reglas de Binance"""
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

    def find_viable_symbols_for_low_balance(self, balance, max_symbols=20):
        """BUSCAR SÍMBOLOS VIABLES - OPTIMIZADO"""
        viable_symbols = []
        
        # LISTA OPTIMIZADA - TOKENS NEXTIA + LÍQUIDOS
        test_symbols = [
            # TOKENS NEXTIA (PRIMERA PRIORIDAD)
            'PEPEUSDT', 'BERAUSDT', 'PENGUUSDT', 'VANAUSDT', 
            'LAYERUSDT', 'BIOUSDT', 'REZUSDT', 'ANIMEUSDT', 
            'PIXELUSDT', '1000CATUSDT', 'SHELLUSDT',
            
            # SÍMBOLOS LÍQUIDOS (RESPALDO)
            'DOGEUSDT', 'TRXUSDT', 'VETUSDT', 'SHIBUSDT',
            'MATICUSDT', 'LTCUSDT', 'SFPUSDT', 'ONGUSDT', 
            'CHRUSDT', 'HOTUSDT'
        ]
        
        logger.info(f"🔍 Buscando {max_symbols} símbolos viables para ${balance:.2f}...")
        
        for symbol in test_symbols:
            try:
                price = self.get_current_price(symbol)
                if not price:
                    continue
                    
                min_qty = self.get_min_quantity(symbol)
                min_notional = self.get_min_notional(symbol)
                
                # Cálculo agresivo - 60% del balance
                trade_amount = balance * 0.6
                
                # Verificar viabilidad
                if (trade_amount >= min_notional and 
                    trade_amount >= (min_qty * price)):
                    
                    viable_symbols.append(symbol)
                    logger.info(f"✅ {symbol} - ${price:.4f}")
                    
                    if len(viable_symbols) >= max_symbols:
                        break
                        
            except Exception as e:
                continue
                
        return viable_symbols

    def execute_trade(self, symbol, side, quantity):
        """Ejecutar trade con validación COMPLETA"""
        try:
            price = self.get_current_price(symbol)
            if not price:
                return False, "No se pudo obtener precio"
            
            adjusted_quantity = self.adjust_quantity(symbol, quantity)
            
            # Validar mínimo de trade
            trade_value = adjusted_quantity * price
            min_notional = self.get_min_notional(symbol)
            
            if trade_value < min_notional:
                required_quantity = min_notional / price
                adjusted_quantity = self.adjust_quantity(symbol, required_quantity)
                logger.info(f"🔧 Ajustando al mínimo: {adjusted_quantity:.6f} {symbol}")
            
            logger.info(f"🔄 Ejecutando {side} {adjusted_quantity:.6f} {symbol}")
            
            # Ejecutar orden
            order = self.client.create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=adjusted_quantity
            )
            
            logger.info(f"✅ Orden ejecutada: {order['orderId']}")
            
            # Obtener precio de ejecución real
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
    """BOT PRINCIPAL - VERSIÓN COMUNITARIA NEXTIA"""
    
    def __init__(self):
        self.running = False
        self.telegram = TelegramManager()
        self.binance = BinanceManager()
        self.analyzer = AggressiveAnalyzer(self.binance)
        
        # CONFIGURACIÓN SUPER AGRESIVA OPTIMIZADA
        self.config = {
            'max_daily_trades': 15,
            'min_balance_required': 1.5,
            'base_risk': 0.6,
            'take_profit': 0.018,
            'stop_loss': 0.009,
            'max_hold_time': 150,
            'scan_interval': 20,
            'min_confidence': 0.45
        }
        
        # Estadísticas MEJORADAS
        self.trades_today = 0
        self.starting_balance = 0
        self.current_balance = 0
        self.consecutive_losses = 0
        self.total_profit = 0.0
        self.winning_trades = 0
        self.losing_trades = 0

    def start(self):
        """Iniciar bot con configuración comunitaria"""
        logger.info("🚀 INICIANDO NEXTIA BOT - VERSIÓN COMUNITARIA")
        
        if not self.binance.connect():
            logger.error("❌ No se pudo conectar a Binance")
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
        
        # Mensaje de inicio MEJORADO
        self.telegram.send_message(
            f"🤖 *Nextia Trading Bot INICIADO* \\\\- *VERSIÓN COMUNITARIA*\n\n"
            f"💰 *Balance inicial:* `${self.starting_balance:.2f}`\n"
            f"🎯 *Símbolos activos:* `{len(viable_symbols)}`\n"
            f"📊 *Top 5:* `{', '.join(viable_symbols[:5])}`\n"
            f"⚡ *Configuración AGRESIVA:*\n"
            f"   • *Risk:* `{self.config['base_risk']*100}%` por trade\n"
            f"   • *Take Profit:* `{self.config['take_profit']*100}%`\n"
            f"   • *Stop Loss:* `{self.config['stop_loss']*100}%`\n"
            f"   • *Hold Time:* `{self.config['max_hold_time']}s`\n\n"
            f"🌐 *Ecosistema Nextia - Código Abierto*"
        )
        
        self.running = True
        self.trading_loop()
        return True

    def stop(self):
        """Detener bot con reporte completo"""
        logger.info("🛑 DETENIENDO BOT NEXTIA")
        final_balance = self.binance.get_available_balance()
        total_pnl = final_balance - self.starting_balance
        win_rate = (self.winning_trades / self.trades_today * 100) if self.trades_today > 0 else 0
        
        # Reporte FINAL
        self.telegram.send_message(
            f"📊 *REPORTE FINAL - Nextia Bot*\n\n"
            f"💰 *Balance inicial:* `${self.starting_balance:.2f}`\n"
            f"💰 *Balance final:* `${final_balance:.2f}`\n"
            f"📈 *PnL total:* `${total_pnl:.4f}`\n"
            f"📊 *Rendimiento:* `{(total_pnl/self.starting_balance)*100:.2f}%`\n"
            f"🎯 *Trades ejecutados:* `{self.trades_today}`\n"
            f"✅ *Trades ganadores:* `{self.winning_trades}`\n"
            f"❌ *Trades perdedores:* `{self.losing_trades}`\n"
            f"📈 *Win Rate:* `{win_rate:.1f}%`\n\n"
            f"🌐 *Gracias por usar Nextia Trading Bot*"
        )
        
        self.running = False

    def execute_trading_cycle(self, symbol):
        """Ciclo de trading COMPLETO Y OPTIMIZADO"""
        try:
            signal, confidence = self.analyzer.get_aggressive_signal(symbol)
            
            # VERIFICACIÓN RÁPIDA
            if signal == "WAIT" or confidence < self.config['min_confidence']:
                logger.info(f"⏭️  Saltando {symbol} - Confianza: {confidence:.2f}")
                return False
            
            price = self.binance.get_current_price(symbol)
            if not price:
                return False
            
            # CÁLCULO AGRESIVO - 60% del balance
            trade_usd = self.current_balance * self.config['base_risk']
            quantity = trade_usd / price
            
            logger.info(f"🎯 EJECUTANDO {symbol}")
            logger.info(f"   - Precio: ${price:.6f}")
            logger.info(f"   - Inversión: ${trade_usd:.2f}")
            logger.info(f"   - Cantidad: {quantity:.4f}")
            logger.info(f"   - Confianza: {confidence:.1%}")
            
            # === COMPRA ===
            buy_success, buy_result = self.binance.execute_trade(symbol, 'BUY', quantity)
            
            if not buy_success:
                logger.error(f"❌ Error en compra: {buy_result}")
                return False
            
            buy_price = buy_result['price']
            buy_quantity = buy_result['quantity']
            
            # Notificación de COMPRA
            self.telegram.send_message(
                f"🟢 *COMPRA EJECUTADA - Nextia Bot*\n\n"
                f"🎯 *Símbolo:* `{symbol}`\n"
                f"💵 *Cantidad:* `{buy_quantity:.4f}`\n"
                f"💰 *Precio:* `${buy_price:.6f}`\n"
                f"📊 *Inversión:* `${buy_quantity * buy_price:.2f}`\n"
                f"💯 *Confianza:* `{confidence:.1%}`\n"
                f"⚡ *Take Profit:* `{self.config['take_profit']*100}%`\n"
                f"🛑 *Stop Loss:* `{self.config['stop_loss']*100}%`"
            )
            
            # === GESTIÓN DE POSICIÓN ===
            logger.info(f"⏳ Monitoreando posición {self.config['max_hold_time']}s...")
            
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
                
                time.sleep(3)
            
            # === VENTA ===
            asset = symbol.replace('USDT', '')
            sell_quantity = self.binance.get_asset_balance(asset)
            
            if sell_quantity <= 0:
                logger.error(f"❌ Balance de {asset} es cero")
                return False
            
            logger.info(f"💼 Vendiendo: {sell_quantity:.6f} {asset}")
            
            sell_success, sell_result = self.binance.execute_trade(symbol, 'SELL', sell_quantity)
            
            if not sell_success:
                logger.error(f"❌ Error en venta: {sell_result}")
                return False
            
            # === CÁLCULO DE RESULTADOS ===
            sell_price = sell_result['price']
            pnl = (sell_price * sell_quantity) - (buy_price * buy_quantity)
            pnl_percent = (sell_price - buy_price) / buy_price * 100
            
            # Actualizar estadísticas
            if pnl > 0:
                self.consecutive_losses = 0
                self.winning_trades += 1
                self.total_profit += pnl
            else:
                self.consecutive_losses += 1
                self.losing_trades += 1
            
            self.current_balance = self.binance.get_available_balance()
            self.trades_today += 1
            
            # === NOTIFICACIÓN DE RESULTADO ===
            status = "🟢 GANADOR" if pnl > 0 else "🔴 PERDEDOR"
            emoji = "🎯" if pnl > 0 else "💸"
            
            self.telegram.send_message(
                f"{emoji} *TRADE CERRADO - {status}*\n\n"
                f"🔰 *Símbolo:* `{symbol}`\n"
                f"📊 *Resultado:* `{exit_reason}`\n"
                f"💰 *Compra:* `${buy_price:.6f}`\n"
                f"💰 *Venta:* `${sell_price:.6f}`\n"
                f"📈 *Cambio:* `{pnl_percent:+.3f}%`\n"
                f"💵 *PnL:* `${pnl:.4f}`\n"
                f"💼 *Balance:* `${self.current_balance:.2f}`\n"
                f"📊 *Racha pérdidas:* `{self.consecutive_losses}`\n"
                f"🎯 *Trade #* `{self.trades_today}`"
            )
            
            logger.info(f"💰 Trade #{self.trades_today} completado: PnL = ${pnl:.4f}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en ciclo de trading: {e}")
            return False

    def trading_loop(self):
        """Loop principal OPTIMIZADO"""
        last_trade_time = 0
        symbol_rotation = 0
        
        while self.running:
            try:
                current_time = time.time()
                self.current_balance = self.binance.get_available_balance()
                
                # VERIFICACIONES RÁPIDAS
                if self.current_balance < self.config['min_balance_required']:
                    logger.warning(f"💰 Balance bajo: ${self.current_balance:.2f}")
                    time.sleep(30)
                    continue
                
                if self.trades_today >= self.config['max_daily_trades']:
                    logger.info(f"🎯 Límite diario: {self.trades_today}/{self.config['max_daily_trades']}")
                    time.sleep(60)
                    continue
                
                # Pausa después de pérdidas
                if self.consecutive_losses >= 5:
                    logger.warning(f"⏸️  {self.consecutive_losses} pérdidas - Pausa 3min")
                    time.sleep(180)
                    self.consecutive_losses = 0
                    continue
                
                # Intervalo entre trades
                if current_time - last_trade_time < self.config['scan_interval']:
                    time.sleep(2)
                    continue
                
                # SELECCIÓN DE SÍMBOLO (rotación inteligente)
                if not hasattr(self, 'viable_symbols') or not self.viable_symbols:
                    self.viable_symbols = self.binance.find_viable_symbols_for_low_balance(self.current_balance)
                
                if not self.viable_symbols:
                    logger.warning("⏳ No hay símbolos viables, esperando...")
                    time.sleep(30)
                    continue
                
                # Rotar símbolos para evitar repetir
                symbol = self.viable_symbols[symbol_rotation % len(self.viable_symbols)]
                symbol_rotation += 1
                
                logger.info(f"🎯 Analizando {symbol}...")
                
                if self.execute_trading_cycle(symbol):
                    last_trade_time = current_time
                    logger.info(f"📈 Trade #{self.trades_today} completado exitosamente")
                
                time.sleep(2)
                
            except KeyboardInterrupt:
                logger.info("🛑 Interrupción por usuario")
                break
            except Exception as e:
                logger.error(f"❌ Error en loop principal: {e}")
                time.sleep(10)

def main():
    """Función principal MEJORADA"""
    print("🤖 NEXTIA TRADING BOT - VERSIÓN COMUNITARIA")
    print("=" * 65)
    print("🚀 Optimizado para MÁXIMA EFICIENCIA Y RENTABILIDAD")
    print("💰 Especificación para balances bajos ($5+ USD)")
    print("🎯 Estrategia: RSI + Momentum + Volume Analysis")
    print("📈 Take Profit: 1.8% | Stop Loss: 0.9%")
    print("⏱️  Hold time: 2.5 minutos máximo")
    print("🔄 Búsqueda de oportunidades cada 20 segundos")
    print("⚡ Risk Management: 60% por trade")
    print("🌐 Ecosistema Nextia - Código Abierto")
    print("=" * 65)
    
    bot = TradingBot()
    
    try:
        if bot.start():
            print("\n✅ Bot iniciado correctamente - Monitorea los logs")
        else:
            print("\n❌ Error al iniciar el bot - Revisa la configuración")
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo bot...")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
    finally:
        bot.stop()

if __name__ == "__main__":
    main()
