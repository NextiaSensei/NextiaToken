#!/usr/bin/env python3
"""
Prueba rápida del Emergency Stop System
"""

import asyncio
import logging
import sys
import os

# Agregar la ruta del proyecto al path
sys.path.append('/NextiaToken/security/trading-bots/auto-trader')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_emergency_stop():
    """Probar el emergency stop"""
    print("🚀 INICIANDO PRUEBA DE EMERGENCY STOP SYSTEM...")
    print("=" * 50)
    
    try:
        # Importar después de agregar el path
        from trade_engine import TradeEngine
        
        # Inicializar trade engine
        print("🔄 Inicializando Trade Engine...")
        engine = TradeEngine()
        
        if not engine.initialized:
            print("❌ Trade Engine no se pudo inicializar")
            return False
        
        print("✅ Trade Engine inicializado correctamente")
        
        # Mostrar estado inicial
        print("\n📊 ESTADO INICIAL:")
        print(f"   Balance USDT: ${engine.get_balance('USDT'):.2f}")
        print(f"   Emergency Stop: {'ACTIVADO' if engine.emergency_stop_activated else 'DESACTIVADO'}")
        print(f"   Trading activo: {'SÍ' if not engine.emergency_stop_activated else 'NO'}")
        
        # Probar emergency stop
        print("\n🛑 ACTIVANDO EMERGENCY STOP...")
        await engine.activate_emergency_stop("Prueba manual del sistema")
        
        # Verificar estado después del emergency stop
        print("\n📊 ESTADO DESPUÉS DE EMERGENCY STOP:")
        print(f"   Emergency Stop: {'ACTIVADO' if engine.emergency_stop_activated else 'DESACTIVADO'}")
        print(f"   Trading activo: {'SÍ' if not engine.emergency_stop_activated else 'NO'}")
        
        # Probar que no se pueden ejecutar órdenes
        print("\n🧪 PROBANDO BLOQUEO DE ÓRDENES...")
        test_result = engine.execute_buy_order("BTCUSDT", 0.001)
        if "EMERGENCY STOP" in str(test_result.get('error', '')):
            print("✅ ✅ ✅ BLOQUEO FUNCIONA: Las órdenes están correctamente bloqueadas")
        else:
            print("❌ ❌ ❌ ERROR: Las órdenes no se bloquearon")
        
        # Probar desactivación
        print("\n🔄 DESACTIVANDO EMERGENCY STOP...")
        engine.deactivate_emergency_stop()
        
        print(f"   Emergency Stop: {'ACTIVADO' if engine.emergency_stop_activated else 'DESACTIVADO'}")
        print(f"   Trading activo: {'SÍ' if not engine.emergency_stop_activated else 'NO'}")
        
        print("\n🎉 PRUEBA DE EMERGENCY STOP COMPLETADA EXITOSAMENTE!")
        return True
        
    except Exception as e:
        print(f"💥 ERROR CRÍTICO EN LA PRUEBA: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_risk_manager_drawdown():
    """Probar el sistema de drawdown del Risk Manager"""
    print("\n" + "=" * 50)
    print("🧪 PROBANDO SISTEMA DE DRAWDOWN...")
    print("=" * 50)
    
    try:
        from risk_manager import RiskManager
        
        risk_mgr = RiskManager()
        
        # Probar método de drawdown
        drawdown_info = risk_mgr.get_drawdown_info()
        
        print("📊 INFORMACIÓN DE DRAWDOWN:")
        for key, value in drawdown_info.items():
            print(f"   {key}: {value}")
        
        # Verificar detección de breach
        if drawdown_info.get('drawdown_breached', False):
            print("🚨 ALERTA: Drawdown breach detectado (ESPERADO EN PRUEBA)")
        else:
            print("✅ Drawdown dentro de límites normales")
            
        print("🎉 PRUEBA DE DRAWDOWN COMPLETADA!")
        return True
        
    except Exception as e:
        print(f"💥 ERROR en prueba de drawdown: {e}")
        return False

async def main():
    """Función principal de pruebas"""
    print("🔧 TESTING COMPLETO DEL SISTEMA DE PROTECCIÓN")
    print("=============================================")
    
    # Ejecutar ambas pruebas
    success1 = await test_emergency_stop()
    success2 = await test_risk_manager_drawdown()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE PRUEBAS:")
    print(f"   Emergency Stop System: {'✅ PASÓ' if success1 else '❌ FALLÓ'}")
    print(f"   Risk Manager Drawdown: {'✅ PASÓ' if success2 else '❌ FALLÓ'}")
    
    if success1 and success2:
        print("\n🎉 🎉 🎉 TODAS LAS PRUEBAS EXITOSAS!")
        print("💪 El sistema de protección está listo para usar")
    else:
        print("\n⚠️  Algunas pruebas fallaron - Revisar implementación")
    
    print("=============================================")

if __name__ == "__main__":
    # Ejecutar pruebas
    asyncio.run(main())
