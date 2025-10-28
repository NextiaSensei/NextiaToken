#!/usr/bin/env python3
"""
Sistema de Base de Datos para Datos Históricos
Almacena precios, volumen e indicadores técnicos
"""

import sqlite3
import json
import time
from datetime import datetime, timedelta
from utils.logger import trading_logger

class TradingDatabase:
    def __init__(self, db_path="trading_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar base de datos y tablas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla de precios en tiempo real
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    price REAL NOT NULL,
                    volume REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, timestamp)
                )
            ''')
            
            # Tabla de indicadores técnicos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS technical_indicators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    sma_20 REAL,
                    sma_50 REAL,
                    rsi REAL,
                    macd REAL,
                    signal_line REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de señales de trading
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trading_signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    signal_type TEXT NOT NULL,
                    strength REAL,
                    price REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            trading_logger.info("✅ Base de datos inicializada correctamente")
            
        except Exception as e:
            trading_logger.error(f"❌ Error inicializando base de datos: {e}")
    
    def save_price_data(self, symbol, price, volume):
        """Guardar datos de precio y volumen"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO price_history 
                (symbol, price, volume, timestamp)
                VALUES (?, ?, ?, datetime('now'))
            ''', (symbol, price, volume))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            trading_logger.error(f"❌ Error guardando datos: {e}")
            return False
    
    def get_recent_prices(self, symbol, hours=24):
        """Obtener precios recientes de las últimas N horas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT price, timestamp FROM price_history 
                WHERE symbol = ? AND timestamp >= datetime('now', ?)
                ORDER BY timestamp ASC
            ''', (symbol, f'-{hours} hours'))
            
            data = cursor.fetchall()
            conn.close()
            return [row[0] for row in data]
            
        except Exception as e:
            trading_logger.error(f"❌ Error obteniendo precios: {e}")
            return []
    
    def save_technical_indicators(self, symbol, indicators):
        """Guardar indicadores técnicos calculados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO technical_indicators 
                (symbol, sma_20, sma_50, rsi, macd, signal_line)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                symbol, 
                indicators.get('sma_20'),
                indicators.get('sma_50'), 
                indicators.get('rsi'),
                indicators.get('macd'),
                indicators.get('signal_line')
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            trading_logger.error(f"❌ Error guardando indicadores: {e}")
            return False

    def save_trading_signal(self, symbol, signal_type, strength, price):
        """Guardar señal de trading en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trading_signals 
                (symbol, signal_type, strength, price)
                VALUES (?, ?, ?, ?)
            ''', (symbol, signal_type, strength, price))
            
            conn.commit()
            conn.close()
            trading_logger.info(f"✅ Señal guardada en DB: {symbol} - {signal_type}")
            return True
            
        except Exception as e:
            trading_logger.error(f"❌ Error guardando señal en DB: {e}")
            return False

# Instancia global de la base de datos
trading_db = TradingDatabase()
