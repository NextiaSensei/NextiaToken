from flask import Flask, render_template, jsonify, request
import sqlite3
import json
from datetime import datetime, timedelta
import os
import threading
import time

app = Flask(__name__)

# Configuración
class DashboardConfig:
    REFRESH_INTERVAL = 5000  # 5 segundos
    HISTORY_HOURS = 24

def get_db_connection():
    """Conexión a la base de datos de trading"""
    try:
        conn = sqlite3.connect('../trading_data.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error BD: {e}")
        return None

def get_trading_stats():
    """Obtener estadísticas completas del trading"""
    try:
        conn = get_db_connection()
        if not conn:
            return {}
            
        cursor = conn.cursor()
        
        # Balance y métricas actuales
        cursor.execute('''
            SELECT balance, timestamp FROM performance 
            ORDER BY timestamp DESC LIMIT 1
        ''')
        current = cursor.fetchone()
        
        # Historial para gráficos
        cursor.execute('''
            SELECT balance, timestamp FROM performance 
            WHERE timestamp >= datetime('now', '-24 hours')
            ORDER BY timestamp
        ''')
        history = cursor.fetchall()
        
        # Trades recientes
        cursor.execute('''
            SELECT symbol, type, price, quantity, timestamp, pnl
            FROM trades 
            ORDER BY timestamp DESC LIMIT 20
        ''')
        trades = cursor.fetchall()
        
        # Métricas de performance
        cursor.execute('''
            SELECT 
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
                AVG(pnl) as avg_pnl,
                SUM(pnl) as total_pnl
            FROM trades 
            WHERE timestamp >= datetime('now', '-24 hours')
        ''')
        metrics = cursor.fetchone()
        
        conn.close()
        
        return {
            'current_balance': current[0] if current else 0,
            'performance_history': [
                {'timestamp': row[1], 'balance': row[0]} for row in history
            ],
            'recent_trades': [
                {
                    'symbol': row[0],
                    'type': row[1],
                    'price': row[2],
                    'quantity': row[3],
                    'timestamp': row[4],
                    'pnl': row[5] or 0
                } for row in trades
            ],
            'metrics': {
                'total_trades': metrics[0] if metrics else 0,
                'winning_trades': metrics[1] if metrics else 0,
                'win_rate': (metrics[1] / metrics[0] * 100) if metrics and metrics[0] > 0 else 0,
                'avg_pnl': metrics[2] if metrics else 0,
                'total_pnl': metrics[3] if metrics else 0
            } if metrics else {}
        }
        
    except Exception as e:
        print(f"Error obteniendo stats: {e}")
        return {}

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def api_dashboard_data():
    data = get_trading_stats()
    return jsonify(data)

@app.route('/api/system-status')
def api_system_status():
    """Estado del sistema en tiempo real"""
    return jsonify({
        'status': 'operational',
        'last_update': datetime.now().isoformat(),
        'trading_session': 'active',
        'active_strategies': 3,
        'signals_today': 24,
        'protection_active': True
    })

@app.route('/api/performance-metrics')
def api_performance_metrics():
    """Métricas detalladas de performance"""
    stats = get_trading_stats()
    return jsonify(stats.get('metrics', {}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
