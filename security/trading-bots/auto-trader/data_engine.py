#!/usr/bin/env python3
"""
MOTOR PRINCIPAL DE DATOS - Nextia Trading Bot
Sistema central que maneja datos en tiempo real
"""

import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.market_data import market_data
from utils.logger import trading_logger
from utils.notifications import notifier

class DataEngine:
    def __init__(self):
        self.running = False
        self.market_data = market_data
        
    def start(self):
        """Iniciar el motor de datos"""
        trading_logger.info("🚀 INICIANDO NEXTIA DATA ENGINE...")
        notifier.send_telegram_message(
            "🚀 <b>Nextia Data Engine INICIADO</b>\n"
            "📊 Monitoreando mercados en tiempo real\n"
            "🔧 Listo para estrategias de trading"
        )
        
        self.running = True
        self.market_data.start()
        
        # Iniciar bucle principal
        self.main_loop()
        
    def stop(self):
        """Detener el motor de datos"""
        trading_logger.info("🛑 DETENIENDO Nextia Data Engine...")
        self.running = False
        self.market_data.stop()
        notifier.send_telegram_message("🛑 <b>Nextia Data Engine DETENIDO</b>")
        
    def main_loop(self):
        """Bucle principal del motor de datos"""
        trading_logger.info("📊 Motor de datos ejecutándose...")
        
        last_status_time = 0
        status_interval = 300  # 5 minutos
        
        try:
            while self.running:
                current_time = time.time()
                
                # Reporte de estado cada 5 minutos
                if current_time - last_status_time >= status_interval:
                    self.send_status_report()
                    last_status_time = current_time
                
                # Aquí procesaremos estrategias después
                # Por ahora solo monitoreamos conexión
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            trading_logger.info("🛑 Señal de interrupción recibida")
        except Exception as e:
            trading_logger.error(f"❌ Error en motor de datos: {e}")
            notifier.send_error_alert(f"Error en motor de datos: {e}")
        finally:
            self.stop()
            
    def send_status_report(self):
        """Enviar reporte de estado por Telegram"""
        active_symbols = []
        for symbol in self.market_data.symbols:
            price = self.market_data.get_current_price(symbol)
            if price:
                active_symbols.append(f"{symbol}: ${price:.2f}")
        
        if active_symbols:
            status_message = (
                "📊 <b>Reporte de Estado - Data Engine</b>\n"
                f"🔗 Conectado: {'✅' if self.market_data.is_connected else '❌'}\n"
                f"📈 Símbolos activos: {len(active_symbols)}\n"
                f"⏰ Tiempo: {time.strftime('%H:%M:%S')}\n\n"
                "<b>Precios Actuales:</b>\n" +
                "\n".join([f"   • {symbol}" for symbol in active_symbols[:5]]) +  # Mostrar solo primeros 5
                ("\n   ..." if len(active_symbols) > 5 else "")
            )
            
            notifier.send_telegram_message(status_message)
            
    def get_market_data(self):
        """Obtener datos de mercado para estrategias"""
        return {
            'prices': self.market_data.get_all_prices(),
            'is_connected': self.market_data.is_connected,
            'symbols': self.market_data.symbols
        }

def main():
    """Función principal"""
    print("🤖 NEXTIA TRADING BOT - DATA ENGINE")
    print("=" * 50)
    print("📡 Conectando a Binance WebSocket...")
    print("💡 Presiona Ctrl+C para detener")
    print("=" * 50)
    
    engine = DataEngine()
    
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
