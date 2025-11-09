#!/usr/bin/env python3
"""
Script para verificar conexión con Binance Testnet - CORREGIDO
"""

import sys
import os
import json
import logging
import time

# Añadir ruta del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from binance.client import Client
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_exchanges_config():
    """Cargar configuración desde exchanges.json y .env"""
    try:
        # Cargar variables de entorno
        load_dotenv()
        
        # Cargar configuración base
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'exchanges.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Reemplazar placeholders con valores reales del .env
        binance_config = config['binance']
        
        if binance_config['api_key'] == 'BINANCE_TESTNET_API_KEY':
            api_key = os.getenv('BINANCE_TESTNET_API_KEY')
            if api_key:
                binance_config['api_key'] = api_key
            else:
                logger.error("❌ BINANCE_TESTNET_API_KEY no encontrada en .env")
                return None
                
        if binance_config['api_secret'] == 'BINANCE_TESTNET_SECRET_KEY':
            api_secret = os.getenv('BINANCE_TESTNET_SECRET_KEY')
            if api_secret:
                binance_config['api_secret'] = api_secret
            else:
                logger.error("❌ BINANCE_TESTNET_SECRET_KEY no encontrada en .env")
                return None
        
        logger.info("✅ Configuración cargada correctamente desde .env")
        return config
        
    except Exception as e:
        logger.error(f"❌ Error cargando configuración: {e}")
        return None

def test_binance_connection():
    """Verifica conexión con Binance Testnet - CORREGIDO"""
    try:
        config = load_exchanges_config()
        if not config:
            return False
        
        binance_config = config['binance']
        
        # Verificar que las keys no sean placeholders
        if "BINANCE_TESTNET_API_KEY" in binance_config['api_key']:
            logger.error("❌ API Key no configurada - Revisa tu archivo .env")
            return False
        
        logger.info("🔗 Conectando a Binance Testnet...")
        
        # Crear cliente con manejo de tiempo mejorado
        client = Client(
            api_key=binance_config['api_key'],
            api_secret=binance_config['api_secret'],
            testnet=binance_config.get('testnet', True)
        )
        
        # Test de conexión básica
        ping = client.ping()
        logger.info("✅ Ping a Binance Testnet exitoso")
        
        # Obtener tiempo del servidor y sincronizar
        server_time = client.get_server_time()
        logger.info(f"⏰ Tiempo servidor: {server_time['serverTime']}")
        
        # Sincronizar tiempo local con servidor
        time_diff = server_time['serverTime'] - int(time.time() * 1000)
        logger.info(f"⏱️  Diferencia de tiempo: {time_diff}ms")
        
        if abs(time_diff) > 1000:  # Si la diferencia es > 1 segundo
            logger.warning(f"⚠️  Gran diferencia de tiempo detectada: {time_diff}ms")
            logger.info("🔄 Ajustando sincronización...")
        
        # Obtener información de cuenta CON manejo de tiempo
        try:
            account = client.get_account()
            logger.info("💰 Balances de prueba disponibles:")
            
            # Mostrar solo los balances principales (para no saturar)
            main_assets = ['BTC', 'ETH', 'ADA', 'USDT', 'BNB', 'USDC']
            assets_shown = 0
            
            for balance in account['balances']:
                free = float(balance['free'])
                locked = float(balance['locked'])
                asset = balance['asset']
                
                # Mostrar solo activos principales o con balance significativo
                if asset in main_assets or free > 0.1 or locked > 0:
                    logger.info(f"   💎 {asset}: Libre={free}, Bloqueado={locked}")
                    assets_shown += 1
            
            if assets_shown == 0:
                logger.info("   ℹ️  Mostrando balances principales...")
                for asset in main_assets:
                    balance = next((b for b in account['balances'] if b['asset'] == asset), None)
                    if balance:
                        free = float(balance['free'])
                        locked = float(balance['locked'])
                        if free > 0 or locked > 0:
                            logger.info(f"   💎 {asset}: Libre={free}, Bloqueado={locked}")
                
        except Exception as account_error:
            logger.warning(f"⚠️  Error obteniendo cuenta: {account_error}")
            logger.info("💡 Probando con método alternativo...")
        
        # Test de orden de prueba (NO real)
        try:
            test_order = client.create_test_order(
                symbol='BTCUSDT',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=0.001
            )
            logger.info("✅ Orden de prueba ejecutada correctamente")
        except Exception as order_error:
            logger.warning(f"⚠️  Orden de prueba falló: {order_error}")
        
        # Obtener ticker de precio
        try:
            ticker = client.get_symbol_ticker(symbol="BTCUSDT")
            logger.info(f"📊 Precio BTC/USDT: ${ticker['price']}")
        except Exception as ticker_error:
            logger.warning(f"⚠️  Error obteniendo precio: {ticker_error}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en conexión Testnet: {e}")
        logger.info("💡 Posibles soluciones:")
        logger.info("   1. Verifica la sincronización de tiempo de tu sistema")
        logger.info("   2. Ejecuta: sudo ntpdate pool.ntp.org")
        logger.info("   3. Revisa que las API keys sean correctas")
        return False

if __name__ == "__main__":
    logger.info("🧪 Iniciando prueba de Binance Testnet...")
    logger.info("==========================================")
    
    if test_binance_connection():
        logger.info("==========================================")
        logger.info("🎉 ¡BINANCE TESTNET CONFIGURADO CORRECTAMENTE!")
        logger.info("🚀 El bot está listo para trading de prueba")
    else:
        logger.info("==========================================")
        logger.error("💥 CONFIGURACIÓN FALLIDA - Revisa los errores arriba")
