import websocket
import json
import threading
import time
import pandas as pd
from datetime import datetime
from utils.logger import trading_logger
from utils.config_loader import config
from utils.notifications import notifier
from data.database import trading_db
from data.technical_analysis import technical_analyzer

class RealTimeMarketData:
    def __init__(self):
        self.ws = None
        self.is_connected = False
        self.symbols = config.get('bot', 'symbols')
        self.timeframe = config.get('bot', 'timeframe')
        self.current_prices = {}
        self.price_history = {}
        self.volume_data = {}
        self.last_signal_time = {}  # 🔥 NUEVO: Control de tiempo entre señales
        self.setup_websocket()
        
        # Inicializar datos históricos
        for symbol in self.symbols:
            self.price_history[symbol] = []
            self.volume_data[symbol] = []
            self.last_signal_time[symbol] = 0

    def setup_websocket(self):
        """Configurar conexión WebSocket a Binance"""
        trading_logger.info("🔄 Inicializando WebSocket para datos en tiempo real...")
        
        self.ws = websocket.WebSocketApp(
            "wss://stream.binance.com:9443/ws",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

    def on_message(self, ws, message):
        """Procesar mensajes entrantes del WebSocket"""
        try:
            data = json.loads(message)
            
            # Procesar datos de ticker (precios en tiempo real)
            if 'e' in data and data['e'] == '24hrTicker':
                self.process_ticker_data(data)
            
            # Procesar datos de kline (velas)
            elif 'e' in data and data['e'] == 'kline':
                self.process_kline_data(data)
                
        except Exception as e:
            trading_logger.error(f"❌ Error procesando mensaje WebSocket: {e}")

    def process_ticker_data(self, data):
        """Procesar datos de ticker en tiempo real"""
        symbol = data['s']
        price = float(data['c'])
        price_change = float(data['p'])
        change_percent = float(data['P'])
        volume = float(data['v'])
        
        # Actualizar precio actual
        self.current_prices[symbol] = price
        
        # Guardar histórico (mantener últimos 100 precios)
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        self.price_history[symbol].append({
            'timestamp': datetime.now(),
            'price': price,
            'change_percent': change_percent,
            'volume': volume
        })
        
        # Mantener solo últimos 100 registros
        if len(self.price_history[symbol]) > 100:
            self.price_history[symbol] = self.price_history[symbol][-100:]
        
        # 🔥 NUEVO: GUARDAR EN BASE DE DATOS
        trading_db.save_price_data(symbol, price, volume)
        
        # 🔥 NUEVO: ANÁLISIS TÉCNICO Y SEÑALES
        self.generate_trading_signals(symbol, price, volume)
        
        # Log cada minuto para no saturar
        current_time = int(time.time())
        if current_time % 60 == 0:  # Log cada minuto
            trading_logger.info(f"📊 {symbol}: ${price:.2f} ({change_percent:+.2f}%) - Vol: {volume:.0f}")

    def generate_trading_signals(self, symbol, price, volume):
        """Generar señales de trading usando análisis técnico"""
        try:
            # 🔥 MEJORA: Evitar señales repetidas muy seguidas
            current_time = time.time()
            last_signal = self.last_signal_time.get(symbol, 0)
            
            # Solo procesar señales cada 10 minutos para el mismo símbolo
            if current_time - last_signal < 600:  # 10 minutos entre señales
                return
            
            # Obtener datos históricos de la base de datos (últimas 24 horas)
            historical_prices = trading_db.get_recent_prices(symbol, hours=24)
            
            # Necesitamos suficientes datos para análisis
            if len(historical_prices) >= 50:
                # Generar señales e indicadores
                signals, indicators = technical_analyzer.generate_signals(
                    symbol, price, historical_prices
                )
                
                # 🔥 GUARDAR INDICADORES EN BASE DE DATOS
                trading_db.save_technical_indicators(symbol, indicators)
                
                # 🔥 PROCESAR SEÑALES FUERTES
                strong_signals = [s for s in signals if s['strength'] > 0.6]
                
                if strong_signals:
                    # 🔥 MEJORA: Actualizar tiempo de última señal
                    self.last_signal_time[symbol] = current_time
                    
                    # Tomar la señal más fuerte
                    strongest_signal = max(strong_signals, key=lambda x: x['strength'])
                    
                    trading_logger.info(f"🎯 SEÑAL FUERTE: {symbol} - {strongest_signal['message']}")
                    
                    # 🔥 NOTIFICACIÓN DE SEÑAL FUERTE
                    notifier.send_telegram_message(
                        f"🚨 <b>SEÑAL DE TRADING DETECTADA</b>\n"
                        f"💎 <b>{symbol}</b>\n"
                        f"📊 {strongest_signal['message']}\n"
                        f"💰 Precio actual: ${price:.2f}\n"
                        f"📈 Volumen: {volume:,.0f}\n"
                        f"💪 Fuerza de señal: {strongest_signal['strength']*100:.0f}%\n"
                        f"🕒 {datetime.now().strftime('%H:%M:%S')}"
                    )
                    
                    # 🔥 GUARDAR SEÑAL EN BASE DE DATOS
                    try:
                        trading_db.save_trading_signal(
                            symbol, 
                            strongest_signal['type'], 
                            strongest_signal['strength'], 
                            price
                        )
                    except Exception as db_error:
                        trading_logger.error(f"❌ Error guardando señal en DB: {db_error}")
                        # Continuar aunque falle el guardado en DB
            
            # Log de indicadores cada 5 minutos
            current_time = int(time.time())
            if current_time % 300 == 0 and len(historical_prices) >= 50:  # Cada 5 minutos
                trading_logger.info(
                    f"📈 {symbol} - SMA20: {indicators.get('sma_20', 0):.2f}, "
                    f"SMA50: {indicators.get('sma_50', 0):.2f}, "
                    f"RSI: {indicators.get('rsi', 0):.2f}"
                )
                
        except Exception as e:
            trading_logger.error(f"❌ Error generando señales para {symbol}: {e}")

    def process_kline_data(self, data):
        """Procesar datos de velas (kline)"""
        kline = data['k']
        symbol = kline['s']
        is_closed = kline['x']  # Si la vela está cerrada
        
        if is_closed:
            candle_data = {
                'timestamp': datetime.fromtimestamp(kline['t'] / 1000),
                'open': float(kline['o']),
                'high': float(kline['h']),
                'low': float(kline['l']),
                'close': float(kline['c']),
                'volume': float(kline['v']),
                'symbol': symbol
            }
            
            trading_logger.info(f"🕯️ Vela cerrada {symbol}: O:{candle_data['open']:.2f} H:{candle_data['high']:.2f} L:{candle_data['low']:.2f} C:{candle_data['close']:.2f}")

    def on_error(self, ws, error):
        """Manejar errores del WebSocket"""
        trading_logger.error(f"❌ WebSocket error: {error}")
        notifier.send_error_alert(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Manejar cierre del WebSocket"""
        self.is_connected = False
        trading_logger.warning("🔌 WebSocket connection closed")
        
        # Intentar reconectar después de 5 segundos
        threading.Timer(5.0, self.reconnect).start()

    def on_open(self, ws):
        """Manejar apertura exitosa del WebSocket"""
        self.is_connected = True
        trading_logger.success("✅ WebSocket CONECTADO a Binance")
        notifier.send_telegram_message("🔌 <b>WebSocket Conectado</b>\n✅ Recibiendo datos en tiempo real de Binance")
        
        # Suscribirse a los streams de cada símbolo
        for symbol in self.symbols:
            stream_name = symbol.lower().replace('/', '')
            
            # Stream de ticker para precios en tiempo real
            ticker_stream = f"{stream_name}@ticker"
            
            # Stream de kline para velas
            kline_stream = f"{stream_name}@kline_{self.timeframe}"
            
            subscription_msg = json.dumps({
                "method": "SUBSCRIBE",
                "params": [ticker_stream, kline_stream],
                "id": 1
            })
            
            ws.send(subscription_msg)
            trading_logger.info(f"📡 Suscrito a {symbol}")

    def reconnect(self):
        """Reconectar WebSocket automáticamente"""
        trading_logger.info("🔄 Intentando reconexión WebSocket...")
        self.setup_websocket()
        self.start()

    def start(self):
        """Iniciar la conexión WebSocket"""
        def run_ws():
            self.ws.run_forever()
        
        ws_thread = threading.Thread(target=run_ws)
        ws_thread.daemon = True
        ws_thread.start()
        trading_logger.info("🚀 WebSocket thread iniciado")

    def stop(self):
        """Detener la conexión WebSocket"""
        if self.ws:
            self.ws.close()
        self.is_connected = False
        trading_logger.info("🛑 WebSocket detenido")

    def get_current_price(self, symbol):
        """Obtener precio actual de un símbolo"""
        # Intentar diferentes formatos de símbolo
        formats_to_try = [
            symbol,
            symbol.replace("/", ""),
            symbol.replace("/", "").upper(),
            symbol.upper(),
            symbol.replace("/", "-"),
        ]
        
        for symbol_format in formats_to_try:
            if symbol_format in self.current_prices:
                return self.current_prices[symbol_format]
        
        return None

    def get_price_history(self, symbol, limit=50):
        """Obtener histórico de precios"""
        if symbol in self.price_history:
            return self.price_history[symbol][-limit:]
        return []

    def get_all_prices(self):
        """Obtener todos los precios actuales"""
        return self.current_prices

    def get_technical_indicators(self, symbol):
        """🔥 NUEVO: Obtener indicadores técnicos actuales"""
        try:
            # Obtener datos históricos
            historical_prices = trading_db.get_recent_prices(symbol, hours=24)
            current_price = self.get_current_price(symbol)
            
            if historical_prices and current_price and len(historical_prices) >= 50:
                signals, indicators = technical_analyzer.generate_signals(
                    symbol, current_price, historical_prices
                )
                return indicators, signals
            else:
                return {}, []
                
        except Exception as e:
            trading_logger.error(f"❌ Error obteniendo indicadores para {symbol}: {e}")
            return {}, []

# Instancia global del mercado
market_data = RealTimeMarketData()
