#!/usr/bin/env python3
"""
Nextia Data Engine - VERSIÓN TESTING
Genera señales de prueba
"""

import logging
import time
import random
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='📡 %(asctime)s - DATA ENGINE TEST - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class TestingDataEngine:
    def __init__(self):
        self.symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT']
        self.signals_generated = 0

    def generate_test_signal(self):
        symbol = random.choice(self.symbols)
        signal_type = random.choice(['BUY', 'SELL'])
        strength = random.choice(['LOW', 'MEDIUM', 'HIGH', 'STRONG'])
        confidence = round(random.uniform(0.6, 0.95), 2)
        
        self.signals_generated += 1
        
        logger.info(f"🎯 SEÑAL TEST: {symbol} {signal_type} (Fuerza: {strength}, Conf: {confidence})")
        
        return {
            'symbol': symbol, 'signal_type': signal_type, 
            'strength': strength, 'confidence': confidence
        }

    def start_testing(self):
        logger.info("🚀 DATA ENGINE TEST INICIADO")
        logger.info("📡 Generando señales cada 1-3 minutos")
        
        while True:
            try:
                wait_time = random.randint(60, 180)
                time.sleep(wait_time)
                
                signal = self.generate_test_signal()
                logger.info(f"📊 Total señales: {self.signals_generated}")
                
            except KeyboardInterrupt:
                logger.info("🛑 Data Engine Test detenido")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")
                time.sleep(30)

def main():
    engine = TestingDataEngine()
    engine.start_testing()

if __name__ == "__main__":
    main()
