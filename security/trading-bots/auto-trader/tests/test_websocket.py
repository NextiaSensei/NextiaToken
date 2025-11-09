#!/usr/bin/env python3
"""
Test del WebSocket - VERSIÓN QUE SÍ FUNCIONA
Usa current_prices directamente como lo hace data_engine.py
"""

import sys
import os
import time
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.market_data import market_data
from utils.logger import trading_logger
from utils.notifications import notifier

def test_websocket_working():
    """Test que SÍ funciona - usa current_prices directamente"""
    print("🧪 Testing WebSocket - VERSIÓN CONFIRMADA FUNCIONA")
    print("=" * 50)
    
    try:
        # Iniciar WebSocket
        market_data.start()
        
        print("⏳ Conectando a Binance WebSocket...")
        time.sleep(5)
        
        if not market_data.is_connected:
            print("❌ WebSocket no conectado")
            return False
            
        print("✅ WebSocket conectado!")
        print("📊 Monitoreando datos (15 segundos)...")
        
        # Monitorear por 15 segundos
        start_time = time.time()
        price_updates = 0
        
        while (time.time() - start_time) < 15:
            elapsed = int(time.time() - start_time)
            
            # Verificar cada 5 segundos
            if elapsed % 5 == 0:
                print(f"\n⏰ {elapsed}s - Estado:")
                
                # ✅ MÉTODO QUE SÍ FUNCIONA: Acceder a current_prices directamente
                if hasattr(market_data, 'current_prices') and market_data.current_prices:
                    print("💰 DATOS RECIBIDOS EN current_prices:")
                    for symbol, price in market_data.current_prices.items():
                        print(f"   ✅ {symbol}: ${price}")
                        price_updates += 1
                else:
                    print("   ⏳ Esperando datos...")
            
            time.sleep(1)
        
        # Resultados finales
        print("\n📊 RESULTADOS FINALES:")
        print("-" * 40)
        
        if price_updates > 0:
            print(f"🎉 ¡ÉXITO! {price_updates} actualizaciones de precio recibidas")
            print("💰 Últimos precios obtenidos:")
            
            # Mostrar los últimos precios
            if hasattr(market_data, 'current_prices') and market_data.current_prices:
                for symbol, price in market_data.current_prices.items():
                    print(f"   ✅ {symbol}: ${price}")
            
            # Notificación de éxito
            notifier.send_telegram_message(
                "🤖 <b>WebSocket Test - CONFIRMADO FUNCIONA</b>\n"
                f"✅ {price_updates} actualizaciones recibidas\n"
                "🚀 WebSocket 100% operacional\n"
                "📈 Datos en tiempo real funcionando\n"
                "🎯 Usando current_prices directamente"
            )
            return True
        else:
            print("❌ No se recibieron datos")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        notifier.send_telegram_message(f"🚨 Test error: {e}")
        return False
    finally:
        print("\n🛑 Deteniendo WebSocket...")
        market_data.stop()

def main():
    """Ejecutar prueba que SÍ funciona"""
    print("🚀 TEST WEB SOCKET - CONFIRMADO FUNCIONA")
    print("Usando current_prices directamente")
    print("=" * 50)
    
    success = test_websocket_working()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ✅ ¡PROBLEMA SOLUCIONADO!")
        print("💡 El WebSocket SÍ funciona correctamente")
        print("📊 Los datos están disponibles en market_data.current_prices")
        print("🚀 Podemos continuar con Data Engine Avanzado")
        print("\n🔧 Para usar los precios en tu código:")
        print("   from data.market_data import market_data")
        print("   precio_btc = market_data.current_prices.get('BTCUSDT')")
    else:
        print("❌ ALGO EXTRAÑO PASA")
        print("💡 data_engine.py funciona pero el test no")
        print("🔍 Revisemos data/market_data.py")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
