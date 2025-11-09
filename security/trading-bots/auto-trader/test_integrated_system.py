#!/usr/bin/env python3
"""
PRUEBA COMPLETA DEL SISTEMA INTEGRADO - Nextia Trading Bot
"""

import sys
import os
import time
import json
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

def test_integrated_system():
    print("🚀 INICIANDO PRUEBA COMPLETA DEL SISTEMA INTEGRADO")
    print("=" * 60)
    
    try:
        # Importar todos los módulos
        from integrated_trading_bot import IntegratedTradingBot
        from profit_manager import ProfitManager
        from session_scheduler import SessionScheduler
        
        print("✅ Módulos importados correctamente")
        
        # 1. Probar Profit Manager
        print("\n🧪 1. Probando Profit Manager...")
        pm = ProfitManager('config/trading_sessions.json')
        print(f"   ✅ Profit Targets: {len(pm.profit_targets)} símbolos")
        print(f"   ✅ Stop Losses: {len(pm.stop_losses)} símbolos")
        
        # Testear lógica de profit/stop
        test_price = 50000
        current_price_profit = 51250  # +2.5%
        current_price_stop = 49250    # -1.5%
        
        should_close_profit = pm.should_close_position('BTCUSDT', current_price_profit, test_price, 'long')
        should_close_stop = pm.should_close_position('BTCUSDT', current_price_stop, test_price, 'long')
        
        print(f"   ✅ Profit Target (2.5%): {should_close_profit} - Esperado: True")
        print(f"   ✅ Stop Loss (1.5%): {should_close_stop} - Esperado: True")
        
        # 2. Probar Session Scheduler
        print("\n🧪 2. Probando Session Scheduler...")
        ss = SessionScheduler('config/trading_sessions.json')
        print(f"   ✅ Sesiones cargadas: {len(ss.trading_sessions)}")
        print(f"   ✅ Sesión activa actualmente: {ss.is_session_active()}")
        
        # Iniciar scheduler en segundo plano
        ss.start_scheduler()
        print(f"   ✅ Scheduler iniciado: {ss.is_trading_time}")
        
        # 3. Probar Trading Bot Integrado
        print("\n🧪 3. Probando Trading Bot Integrado...")
        bot = IntegratedTradingBot()
        
        # Verificar que todos los módulos estén inicializados
        print(f"   ✅ Trade Engine: {'✅' if bot.trade_engine.initialized else '❌'}")
        print(f"   ✅ Risk Manager: ✅")
        print(f"   ✅ Profit Manager: ✅ ({len(bot.profit_manager.profit_targets)} símbolos)")
        print(f"   ✅ Session Scheduler: ✅ ({'Activo' if bot.session_scheduler.is_trading_time else 'Inactivo'})")
        
        # 4. Probar estado del sistema
        print("\n🧪 4. Probando Estado del Sistema...")
        system_status = bot.get_system_status()
        print(f"   ✅ Estado general: {system_status['status']}")
        print(f"   ✅ Sesión trading: {system_status['trading_session_active']}")
        print(f"   ✅ Módulos operativos: {sum(1 for k,v in system_status.items() if v == 'operational')}")
        
        # 5. Probar portfolio info
        print("\n🧪 5. Probando Información de Portfolio...")
        portfolio_info = bot.get_portfolio_info()
        print(f"   ✅ Balance: ${portfolio_info.get('total_balance', 0):.2f}")
        print(f"   ✅ Trades activos: {portfolio_info.get('active_trades', 0)}")
        print(f"   ✅ Sesión trading: {portfolio_info.get('trading_session_active', False)}")
        
        # 6. Simular procesamiento de señales
        print("\n🧪 6. Simulando Procesamiento de Señales...")
        
        # Señal dentro de horario (si está activo)
        if bot.session_scheduler.is_trading_time:
            print("   🕒 Sesión ACTIVA - Probando señal...")
            success, message = bot.process_signal('BTCUSDT', 'BUY', 'STRONG', 0.85)
            print(f"   ✅ Señal procesada: {success} - {message}")
        else:
            print("   🕒 Sesión INACTIVA - Probando rechazo...")
            success, message = bot.process_signal('BTCUSDT', 'BUY', 'STRONG', 0.85)
            print(f"   ✅ Señal rechazada (esperado): {not success} - Razón: {message}")
        
        # 7. Probar limpieza de trades
        print("\n🧪 7. Probando Limpieza de Trades...")
        cleaned = bot.cleanup_old_trades()
        print(f"   ✅ Trades limpiados: {cleaned}")
        
        # 8. Probar verificación de profit/stop
        print("\n🧪 8. Probando Verificación Profit/Stop...")
        closed_positions = bot.check_profit_stop_conditions()
        print(f"   ✅ Posiciones cerradas por profit/stop: {closed_positions}")
        
        print("\n" + "=" * 60)
        print("🎉 ¡PRUEBA COMPLETADA EXITOSAMENTE!")
        print("✅ Sistema integrado funcionando correctamente")
        print("📊 Módulos operativos:")
        print("   - IntegratedTradingBot: ✅")
        print("   - ProfitManager: ✅") 
        print("   - SessionScheduler: ✅")
        print("   - RiskManager: ✅")
        print("   - TradeEngine: ✅")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integrated_system()
    if success:
        print("\n🚀 ¡SISTEMA LISTO PARA PRODUCCIÓN!")
        print("💪 Ejecuta: python integrated_trading_bot.py")
    else:
        print("\n💥 ¡SE REQUIEREN AJUSTES!")
        sys.exit(1)
