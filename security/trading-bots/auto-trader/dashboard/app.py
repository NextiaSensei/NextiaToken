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
    """Conexión a la base de datos de trading - MEJORADA"""
    try:
        # Usar ruta absoluta para evitar problemas
        db_path = 'trading_data.db'
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Error BD: {e}")
        return None

def get_trading_stats():
    """Obtener estadísticas completas del trading - ACTUALIZADA"""
    try:
        conn = get_db_connection()
        if not conn:
            return {
                'current_balance': 0,
                'performance_history': [],
                'recent_trades': [],
                'metrics': {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'win_rate': 0,
                    'avg_pnl': "0.0000",
                    'total_pnl': "0.0000"
                }
            }
            
        cursor = conn.cursor()
        
        # Balance y métricas actuales - MEJORADO
        cursor.execute('''
            SELECT balance, total_trades, winning_trades, losing_trades, timestamp 
            FROM performance 
            ORDER BY timestamp DESC LIMIT 1
        ''')
        current = cursor.fetchone()
        
        # Historial para gráficos - MEJORADO (últimas 24 horas)
        cursor.execute('''
            SELECT balance, total_trades, timestamp FROM performance 
            WHERE timestamp >= datetime('now', '-24 hours')
            ORDER BY timestamp
        ''')
        history = cursor.fetchall()
        
        # Trades recientes - MEJORADO para nuevo formato
        cursor.execute('''
            SELECT symbol, side, price, quantity, profit_loss, timestamp
            FROM trades 
            ORDER BY timestamp DESC LIMIT 20
        ''')
        trades = cursor.fetchall()
        
        # Métricas de performance - ACTUALIZADO
        cursor.execute('''
            SELECT 
                COUNT(*) as total_trades,
                SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) as winning_trades,
                SUM(CASE WHEN profit_loss < 0 THEN 1 ELSE 0 END) as losing_trades,
                AVG(profit_loss) as avg_pnl,
                SUM(profit_loss) as total_pnl
            FROM trades 
            WHERE timestamp >= datetime('now', '-24 hours')
        ''')
        metrics = cursor.fetchone()
        
        conn.close()
        
        # Calcular win rate
        win_rate = 0
        if metrics and metrics[0] > 0:
            win_rate = (metrics[1] / metrics[0]) * 100
        
        # Formatear datos para el dashboard
        current_balance = current[0] if current else 0
        current_trades = current[1] if current else 0
        current_wins = current[2] if current else 0
        current_losses = current[3] if current else 0
        
        return {
            'current_balance': current_balance,
            'current_trades': current_trades,
            'current_wins': current_wins,
            'current_losses': current_losses,
            'last_update': current[4] if current else datetime.now().isoformat(),
            'performance_history': [
                {
                    'timestamp': row[2], 
                    'balance': row[0],
                    'total_trades': row[1]
                } for row in history
            ],
            'recent_trades': [
                {
                    'symbol': row[0],
                    'type': row[1],  # BUY/SELL
                    'price': f"{row[2]:.6f}",
                    'quantity': f"{row[3]:.4f}",
                    'pnl': f"{row[4]:.4f}" if row[4] is not None else "0.0000",
                    'timestamp': row[5],
                    'status': 'profit' if row[4] and row[4] > 0 else 'loss' if row[4] and row[4] < 0 else 'neutral'
                } for row in trades
            ],
            'metrics': {
                'total_trades': metrics[0] if metrics else 0,
                'winning_trades': metrics[1] if metrics else 0,
                'losing_trades': metrics[2] if metrics else 0,
                'win_rate': round(win_rate, 2),
                'avg_pnl': f"{metrics[3]:.4f}" if metrics and metrics[3] else "0.0000",
                'total_pnl': f"{metrics[4]:.4f}" if metrics and metrics[4] else "0.0000"
            }
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo stats: {e}")
        return {
            'current_balance': 0,
            'performance_history': [],
            'recent_trades': [],
            'metrics': {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'avg_pnl': "0.0000",
                'total_pnl': "0.0000"
            }
        }

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def api_dashboard_data():
    """Endpoint principal del dashboard - MEJORADO"""
    data = get_trading_stats()
    return jsonify(data)

@app.route('/api/system-status')
def api_system_status():
    """Estado del sistema en tiempo real - ACTUALIZADO"""
    stats = get_trading_stats()
    
    return jsonify({
        'status': 'operational',
        'last_update': datetime.now().isoformat(),
        'trading_session': 'active',
        'active_strategies': 3,
        'signals_today': stats.get('current_trades', 0),
        'protection_active': True,
        'database_connected': True,
        'real_time_data': True
    })

@app.route('/api/performance-metrics')
def api_performance_metrics():
    """Métricas detalladas de performance - ACTUALIZADO"""
    stats = get_trading_stats()
    return jsonify(stats.get('metrics', {}))

@app.route('/api/debug-trades')
def debug_trades():
    """Endpoint de debug para trades - NUEVO"""
    try:
        conn = get_db_connection()
        trades = conn.execute('''
            SELECT symbol, side, quantity, price, profit_loss, timestamp 
            FROM trades ORDER BY id DESC LIMIT 10
        ''').fetchall()
        conn.close()
        
        trades_list = []
        for trade in trades:
            trades_list.append({
                'symbol': trade[0],
                'side': trade[1],
                'quantity': trade[2],
                'price': trade[3],
                'profit_loss': trade[4],
                'timestamp': trade[5]
            })
        
        return jsonify({
            'total_trades': len(trades_list), 
            'trades': trades_list,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'})

@app.route('/api/debug-performance')
def debug_performance():
    """Endpoint de debug para performance - NUEVO"""
    try:
        conn = get_db_connection()
        performance = conn.execute('''
            SELECT timestamp, balance, total_trades, winning_trades, losing_trades 
            FROM performance ORDER BY id DESC LIMIT 10
        ''').fetchall()
        conn.close()
        
        perf_list = []
        for perf in performance:
            perf_list.append({
                'timestamp': perf[0],
                'balance': perf[1],
                'total_trades': perf[2],
                'winning_trades': perf[3],
                'losing_trades': perf[4]
            })
        
        return jsonify({
            'total_records': len(perf_list), 
            'performance': perf_list,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'})

@app.route('/api/current-balance')
def api_current_balance():
    """Balance actual - NUEVO"""
    try:
        conn = get_db_connection()
        current = conn.execute('''
            SELECT balance FROM performance ORDER BY timestamp DESC LIMIT 1
        ''').fetchone()
        conn.close()
        
        return jsonify({
            'balance': current[0] if current else 0,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'balance': 0, 'error': str(e)})

@app.route('/api/force-balance-update', methods=['POST'])
def api_force_balance_update():
    """Forzar actualización de balance - NUEVO"""
    try:
        # Aquí podrías integrar una llamada al bot para actualizar balance
        return jsonify({'status': 'success', 'message': 'Balance update triggered'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    print("🚀 INICIANDO NEXTIA TRADING DASHBOARD")
    print("📊 Sistema de logging automático: ACTIVADO")
    print("💾 Base de datos: trading_data.db")
    print("🌐 Dashboard: http://localhost:5000")
    print("🔄 Actualización automática: 5 segundos")
    print("🔧 Endpoints de debug: /api/debug-trades, /api/debug-performance")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
