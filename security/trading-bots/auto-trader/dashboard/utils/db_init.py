import sqlite3
import json
from datetime import datetime, timedelta
import random

def init_sample_data():
    """Inicializar datos de muestra para el dashboard"""
    conn = sqlite3.connect('trading_data.db')
    cursor = conn.cursor()
    
    # Crear tablas si no existen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            balance REAL NOT NULL,
            timestamp DATETIME NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            type TEXT NOT NULL,
            price REAL NOT NULL,
            quantity REAL NOT NULL,
            pnl REAL,
            timestamp DATETIME NOT NULL
        )
    ''')
    
    # Generar datos de performance de muestra
    base_balance = 116200.0
    current_time = datetime.now()
    
    for i in range(100):
        balance = base_balance + random.uniform(-500, 800)
        time_offset = timedelta(minutes=10 * i)
        timestamp = current_time - time_offset
        
        cursor.execute(
            'INSERT INTO performance (balance, timestamp) VALUES (?, ?)',
            (balance, timestamp.isoformat())
        )
    
    # Generar trades de muestra
    symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT']
    
    for i in range(20):
        symbol = random.choice(symbols)
        trade_type = random.choice(['BUY', 'SELL'])
        price = random.uniform(10, 50000)
        quantity = random.uniform(0.001, 1.0)
        pnl = random.uniform(-50, 100)
        time_offset = timedelta(hours=random.randint(1, 24))
        timestamp = current_time - time_offset
        
        cursor.execute(
            'INSERT INTO trades (symbol, type, price, quantity, pnl, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
            (symbol, trade_type, price, quantity, pnl, timestamp.isoformat())
        )
    
    conn.commit()
    conn.close()
    print("✅ Datos de muestra inicializados")

if __name__ == '__main__':
    init_sample_data()
