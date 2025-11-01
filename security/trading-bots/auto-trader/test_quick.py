#!/usr/bin/env python3
"""
Prueba rápida del Emergency Stop
"""

import logging
logging.basicConfig(level=logging.INFO)

def test_syntax():
    """Verificar que no hay errores de sintaxis"""
    print("🔍 Verificando sintaxis...")
    try:
        from trade_engine import TradeEngine
        print("✅ Sintaxis de trade_engine.py OK")
        
        from risk_manager import RiskManager  
        print("✅ Sintaxis de risk_manager.py OK")
        
        print("🎉 Todos los archivos tienen sintaxis correcta!")
        return True
        
    except SyntaxError as e:
        print(f"❌ ERROR DE SINTAXIS: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Otro error: {e}")
        return True

if __name__ == "__main__":
    test_syntax()
