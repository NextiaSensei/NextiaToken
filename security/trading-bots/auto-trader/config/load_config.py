#!/usr/bin/env python3
"""
Módulo seguro para cargar configuraciones desde .env y archivos JSON
"""

import os
import json
from dotenv import load_dotenv

def load_config():
    """Cargar configuración completa del bot"""
    # Cargar variables de entorno
    load_dotenv()
    
    config = {
        'exchanges': load_exchanges_config(),
        'telegram': load_telegram_config(),
        'trading': load_trading_config()
    }
    
    return config

def load_exchanges_config():
    """Cargar configuración de exchanges de forma segura"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'exchanges.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Reemplazar placeholders con valores reales
        if config['binance']['api_key'] == 'BINANCE_TESTNET_API_KEY':
            config['binance']['api_key'] = os.getenv('BINANCE_TESTNET_API_KEY', '')
            
        if config['binance']['api_secret'] == 'BINANCE_TESTNET_SECRET_KEY':
            config['binance']['api_secret'] = os.getenv('BINANCE_TESTNET_SECRET_KEY', '')
            
        return config
    except Exception as e:
        print(f"❌ Error cargando configuración de exchanges: {e}")
        return {}

def load_telegram_config():
    """Cargar configuración de Telegram"""
    return {
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
    }

def load_trading_config():
    """Cargar configuración de trading"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'bot_config.json')
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return {}
