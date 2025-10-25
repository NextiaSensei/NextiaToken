import websocket
import json
import threading
import time
import pandas as pd
from datetime import datetime
from utils.logger import trading_logger
from utils.config_loader import config
from utils.notifications import notifier

class RealTimeMarketData:
    def __init__(self):
        self.ws = None
        self.is_connected = False
        self.symbols = config.get('bot', 'symbols')
        self.timeframe = config.get('bot', 'timeframe')
        self.current_prices = {}
        self.price_history = {}
        self.volume_data = {}
        self.setup_websocket()
        
        # Inicializar datos históricos
        for symbol in self.symbols:
            self.price_history[symbol] = []
            self.volume_data[symbol] = []

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
        
        # Log cada minuto para no saturar
        current_time = int(time.time())
        if current_time % 60 == 0:  # Log cada minuto
            trading_logger.info(f"📊 {symbol}: ${price:.2f} ({change_percent:+.2f}%) - Vol: {volume:.0f}")

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
        return self.current_prices.get(symbol)

    def get_price_history(self, symbol, limit=50):
        """Obtener histórico de precios"""
        if symbol in self.price_history:
            return self.price_history[symbol][-limit:]
        return []

    def get_all_prices(self):
        """Obtener todos los precios actuales"""
        return self.current_prices

# Instancia global del mercado
market_data = RealTimeMarketData()
