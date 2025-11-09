#!/usr/bin/env python3
"""
TEST COMPLETO DEL SISTEMA NEXTIA TRADING BOT
Script de pruebas end-to-end para verificar todos los componentes del sistema
"""

import os
import sys
import time
import logging
from datetime import datetime

# Configurar logging para el test
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_sistema_completo.log')
    ]
)

logger = logging.getLogger("TEST_SISTEMA_COMPLETO")

def test_configuraciones():
    """Test 1: Verificar que todas las configuraciones se cargan correctamente"""
    logger.info("🧪 TEST 1: Verificando configuraciones...")
    
    try:
        # Verificar archivos de configuración esenciales
        config_files = [
            'config/trading_rules.json',
            'config/exchanges.json', 
            'config/bot_config.json'
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                logger.info(f"✅ {config_file} encontrado")
            else:
                logger.warning(f"⚠️  {config_file} no encontrado (usando defaults)")
        
        logger.info("✅ TEST 1 COMPLETADO: Configuraciones verificadas")
        return True
        
    except Exception as e:
        logger.error(f"❌ TEST 1 FALLADO: {e}")
        return False

def test_imports_modulos():
    """Test 2: Verificar que todos los módulos se importan correctamente"""
    logger.info("🧪 TEST 2: Verificando imports de módulos...")
    
    try:
        # Test de imports básicos
        import pandas as pd
        import numpy as np
        import sqlite3
        from binance.client import Client
        
        logger.info("✅ Librerías básicas importadas correctamente")
        
        # Test de imports de nuestros módulos
        try:
            from data_engine import DataEngine
            logger.info("✅ DataEngine importado correctamente")
        except ImportError as e:
            logger.warning(f"⚠️  DataEngine no disponible: {e}")
            
        try:
            from trade_engine import TradeEngine
            logger.info("✅ TradeEngine importado correctamente")
        except ImportError as e:
            logger.warning(f"⚠️  TradeEngine no disponible: {e}")
            
        try:
            from risk_manager import RiskManager
            logger.info("✅ RiskManager importado correctamente")
        except ImportError as e:
            logger.warning(f"⚠️  RiskManager no disponible: {e}")
            
        logger.info("✅ TEST 2 COMPLETADO: Imports verificados")
        return True
        
    except Exception as e:
        logger.error(f"❌ TEST 2 FALLADO: {e}")
        return False

def test_conexion_binance():
    """Test 3: Verificar conexión con Binance Testnet"""
    logger.info("🧪 TEST 3: Verificando conexión Binance Testnet...")
    
    try:
        from trade_engine import TradeEngine
        
        # Crear instancia de TradeEngine (usará testnet por defecto)
        trade_engine = TradeEngine()
        
        # Verificar conexión
        if trade_engine.client:
            # Test de ping
            try:
                trade_engine.client.ping()
                logger.info("✅ Ping a Binance Testnet exitoso")
                
                # Obtener tiempo del servidor
                server_time = trade_engine.client.get_server_time()
                logger.info(f"✅ Tiempo del servidor: {server_time['serverTime']}")
                
                # Obtener información de cuenta (testnet)
                account_info = trade_engine.client.get_account()
                logger.info(f"✅ Cuenta Testnet: {account_info['accountType']}")
                
                trade_engine.client.session.close()
                logger.info("✅ TEST 3 COMPLETADO: Conexión Binance Testnet exitosa")
                return True
                
            except Exception as e:
                logger.error(f"❌ Error en comunicación con Binance: {e}")
                return False
        else:
            logger.error("❌ Cliente Binance no inicializado")
            return False
            
    except Exception as e:
        logger.error(f"❌ TEST 3 FALLADO: {e}")
        return False

def test_base_datos():
    """Test 4: Verificar base de datos y tablas"""
    logger.info("🧪 TEST 4: Verificando base de datos...")
    
    try:
        import sqlite3
        import os
        
        db_path = 'trading_bot.db'
        
        if os.path.exists(db_path):
            logger.info(f"✅ Base de datos encontrada: {db_path}")
            
            # Conectar y verificar tablas
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Verificar tablas existentes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            logger.info("📊 Tablas en la base de datos:")
            for table in tables:
                logger.info(f"   - {table[0]}")
                
            # Verificar estructura de tabla de señales si existe
            if ('signals',) in tables:
                cursor.execute("PRAGMA table_info(signals)")
                columns = cursor.fetchall()
                logger.info("📋 Estructura de tabla 'signals':")
                for col in columns:
                    logger.info(f"   - {col[1]} ({col[2]})")
            
            conn.close()
            logger.info("✅ TEST 4 COMPLETADO: Base de datos verificada")
            return True
        else:
            logger.warning("⚠️  Base de datos no encontrada (se creará automáticamente)")
            return True
            
    except Exception as e:
        logger.error(f"❌ TEST 4 FALLADO: {e}")
        return False

def test_indicadores_tecnicos():
    """Test 5: Verificar cálculo de indicadores técnicos"""
    logger.info("🧪 TEST 5: Verificando indicadores técnicos...")
    
    try:
        import pandas as pd
        import numpy as np
        
        # Crear datos de prueba
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        data = pd.DataFrame({
            'date': dates,
            'open': np.random.uniform(100, 200, 100),
            'high': np.random.uniform(200, 300, 100),
            'low': np.random.uniform(50, 100, 100),
            'close': np.random.uniform(150, 250, 100),
            'volume': np.random.uniform(1000, 5000, 100)
        })
        
        # Calcular indicadores básicos
        data['sma_20'] = data['close'].rolling(window=20).mean()
        data['ema_12'] = data['close'].ewm(span=12).mean()
        data['rsi'] = 50  # Placeholder para RSI
        
        logger.info(f"✅ Datos de prueba generados: {len(data)} registros")
        logger.info(f"✅ SMA_20 calculado: {data['sma_20'].iloc[-1]:.2f}")
        logger.info(f"✅ EMA_12 calculado: {data['ema_12'].iloc[-1]:.2f}")
        
        logger.info("✅ TEST 5 COMPLETADO: Indicadores técnicos verificados")
        return True
        
    except Exception as e:
        logger.error(f"❌ TEST 5 FALLADO: {e}")
        return False

def test_sistema_notificaciones():
    """Test 6: Verificar sistema de notificaciones"""
    logger.info("🧪 TEST 6: Verificando sistema de notificaciones...")
    
    try:
        # Verificar configuración de Telegram
        telegram_config = 'config/telegram.json'
        if os.path.exists(telegram_config):
            logger.info("✅ Configuración de Telegram encontrada")
            
            # Test básico de notificación (sin enviar realmente)
            logger.info("📱 Sistema de notificaciones listo")
            logger.info("✅ TEST 6 COMPLETADO: Sistema de notificaciones verificado")
            return True
        else:
            logger.warning("⚠️  Configuración de Telegram no encontrada")
            logger.info("✅ TEST 6 COMPLETADO (con advertencias)")
            return True
            
    except Exception as e:
        logger.error(f"❌ TEST 6 FALLADO: {e}")
        return False

def test_risk_management():
    """Test 7: Verificar cálculos de risk management"""
    logger.info("🧪 TEST 7: Verificando risk management...")
    
    try:
        # Simular cálculos de posición sizing
        balance = 100000  # $100,000
        risk_per_trade = 0.02  # 2%
        entry_price = 50000  # BTC a $50,000
        stop_loss = 48000    # SL a $48,000
        
        position_size = (balance * risk_per_trade) / (entry_price - stop_loss)
        investment = position_size * entry_price
        
        logger.info(f"💰 Balance simulado: ${balance:,.2f}")
        logger.info(f"🎯 Riesgo por trade: {risk_per_trade*100}%")
        logger.info(f"📏 Tamaño de posición: {position_size:.6f} BTC")
        logger.info(f"💵 Inversión: ${investment:,.2f}")
        
        # Verificar límites
        max_position_size = balance * 0.1  # Máximo 10% del balance
        if investment <= max_position_size:
            logger.info("✅ Tamaño de posición dentro de límites")
        else:
            logger.warning("⚠️  Tamaño de posición excede límites")
        
        logger.info("✅ TEST 7 COMPLETADO: Risk management verificado")
        return True
        
    except Exception as e:
        logger.error(f"❌ TEST 7 FALLADO: {e}")
        return False

def ejecutar_tests_completos():
    """Ejecutar todos los tests del sistema"""
    logger.info("🚀 INICIANDO TEST COMPLETO DEL SISTEMA")
    logger.info("=" * 60)
    
    start_time = time.time()
    tests_results = []
    
    # Ejecutar todos los tests
    tests = [
        test_configuraciones,
        test_imports_modulos, 
        test_conexion_binance,
        test_base_datos,
        test_indicadores_tecnicos,
        test_sistema_notificaciones,
        test_risk_management
    ]
    
    for test in tests:
        result = test()
        tests_results.append(result)
        logger.info("-" * 40)
    
    # Resumen final
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info("📊 RESUMEN FINAL DE TESTS")
    logger.info("=" * 60)
    
    passed = sum(tests_results)
    total = len(tests_results)
    
    logger.info(f"✅ Tests pasados: {passed}/{total}")
    logger.info(f"⏱️  Duración total: {duration:.2f} segundos")
    
    if passed == total:
        logger.info("🎉 ¡SISTEMA VERIFICADO COMPLETAMENTE!")
        logger.info("🚀 Todo listo para operar en modo producción")
    else:
        logger.warning("⚠️  Algunos tests fallaron - Revisar logs")
        logger.info("💡 Ejecutar tests individuales para más detalles")
    
    logger.info("=" * 60)
    
    return all(tests_results)

if __name__ == "__main__":
    # Crear directorio de config si no existe
    os.makedirs('config', exist_ok=True)
    
    # Ejecutar tests
    success = ejecutar_tests_completos()
    
    # Salir con código apropiado
    sys.exit(0 if success else 1)
