#!/usr/bin/env python3
"""
Test de Análisis Técnico y Base de Datos
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.market_data import market_data
from data.technical_analysis import technical_analyzer
from data.database import trading_db
from utils.logger import trading_logger

def test_technical_analysis():
    """Probar sistema de análisis técnico"""
    print("🧪 Testing Análisis Técnico y Base de Datos...")
    print("=" * 50)
    
    try:
        # Simular datos de prueba
        test_prices = [100, 102, 101, 105, 107, 110, 108, 112, 115, 113,
                      116, 118, 120, 119, 121, 123, 125, 124, 126, 128,
                      127, 129, 130, 132, 131, 133, 135, 134, 136, 138]
        
        # Probar indicadores
        sma_20 = technical_analyzer.calculate_sma(test_prices, 20)
        rsi = technical_analyzer.calculate_rsi(test_prices)
        macd, signal, hist = technical_analyzer.calculate_macd(test_prices)
        
        print("📊 INDICADORES CALCULADOS:")
        print(f"   ✅ SMA 20: {sma_20:.2f}")
        print(f"   ✅ RSI: {rsi:.2f}")
        print(f"   ✅ MACD: {macd:.4f}")
        print(f"   ✅ Señal: {signal:.4f}")
        
        # Probar generación de señales
        signals, indicators = technical_analyzer.generate_signals(
            "TESTUSDT", test_prices[-1], test_prices
        )
        
        print(f"📨 Señales generadas: {len(signals)}")
        for signal in signals:
            print(f"   🎯 {signal['type']} - {signal['message']}")
        
        # Probar base de datos
        print("\n💾 Probando base de datos...")
        trading_db.save_price_data("TESTUSDT", 1500.50, 100000)
        recent = trading_db.get_recent_prices("TESTUSDT", 1)
        print(f"   ✅ Datos guardados y recuperados: {len(recent)} registros")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

if __name__ == "__main__":
    success = test_technical_analysis()
    print("\n" + "=" * 50)
    if success:
        print("🎉 ✅ ANÁLISIS TÉCNICO FUNCIONANDO!")
    else:
        print("❌ TEST FALLÓ")
    exit(0 if success else 1)
