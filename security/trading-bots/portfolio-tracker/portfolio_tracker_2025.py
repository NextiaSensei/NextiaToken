#!/usr/bin/env python3
"""
Nextia Portfolio Tracker 2025 - Seguimiento de inversiones en tiempo real
Herramienta oficial del ecosistema Nextia Token
"""
import requests
import json
import time
import os
import pandas as pd
from datetime import datetime, timedelta

class NextiaPortfolioTracker:
    def __init__(self, config_file="configs/portfolio_config.json"):
        self.config = self.load_config(config_file)
        self.portfolio_data = {}
        self.setup_logging()
        
    def load_config(self, config_file):
        """Cargar configuración del portfolio"""
        try:
            config_path = f"security/trading-bots/portfolio-tracker/{config_file}"
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Configuración por defecto"""
        return {
            "portfolio_name": "Nextia Default Portfolio",
            "currency": "USD",
            "update_interval": 300,
            "holdings": {
                "BTC": {"amount": 0.01, "buy_price": 50000},
                "ETH": {"amount": 0.1, "buy_price": 3500}
            },
            "watchlist": ["NXT", "ADA", "DOT", "SOL"]
        }
    
    def setup_logging(self):
        """Configurar sistema de logging"""
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('NextiaPortfolioTracker')
    
    def get_current_price(self, symbol):
        """Obtener precio actual desde Binance"""
        try:
            if symbol == "NXT":
                # Placeholder para cuando NXT esté en exchanges
                return 0.15  # Precio simulado para desarrollo
                
            # Para otras criptos, usar Binance
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
            response = requests.get(url, timeout=10)
            data = response.json()
            return float(data['price'])
        except Exception as e:
            self.logger.error(f"Error obteniendo precio de {symbol}: {e}")
            return None
    
    def calculate_portfolio_value(self):
        """Calcular valor total del portfolio"""
        total_invested = 0
        total_current = 0
        portfolio_details = {}
        
        print("🔄 Actualizando precios del portfolio...")
        
        for symbol, holding in self.config['holdings'].items():
            amount = holding['amount']
            buy_price = holding['buy_price']
            current_price = self.get_current_price(symbol)
            
            if current_price is not None:
                invested = amount * buy_price
                current_value = amount * current_price
                profit_loss = current_value - invested
                profit_loss_percent = (profit_loss / invested) * 100 if invested > 0 else 0
                
                portfolio_details[symbol] = {
                    'amount': amount,
                    'buy_price': buy_price,
                    'current_price': current_price,
                    'invested': invested,
                    'current_value': current_value,
                    'profit_loss': profit_loss,
                    'profit_loss_percent': profit_loss_percent
                }
                
                total_invested += invested
                total_current += current_value
        
        total_profit_loss = total_current - total_invested
        total_profit_loss_percent = (total_profit_loss / total_invested) * 100 if total_invested > 0 else 0
        
        self.portfolio_data = {
            'timestamp': datetime.now().isoformat(),
            'total_invested': total_invested,
            'total_current': total_current,
            'total_profit_loss': total_profit_loss,
            'total_profit_loss_percent': total_profit_loss_percent,
            'holdings': portfolio_details,
            'summary': self.generate_summary(total_invested, total_current, total_profit_loss)
        }
        
        return self.portfolio_data
    
    def generate_summary(self, invested, current, profit_loss):
        """Generar resumen del portfolio"""
        if profit_loss > 0:
            status = "🟢 EN GANANCIAS"
            emoji = "📈"
        else:
            status = "🔴 EN PÉRDIDAS"
            emoji = "📉"
        
        return {
            'status': status,
            'emoji': emoji,
            'roi': f"{((current - invested) / invested * 100):.2f}%" if invested > 0 else "0%"
        }
    
    def display_portfolio(self):
        """Mostrar portfolio en formato legible"""
        portfolio = self.calculate_portfolio_value()
        
        print(f"\n{'='*80}")
        print(f"💰 {self.config['portfolio_name']}")
        print(f"{'='*80}")
        print(f"📊 RESUMEN DEL PORTFOLIO")
        print(f"⏰ Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💵 Total Invertido: ${portfolio['total_invested']:,.2f}")
        print(f"💰 Valor Actual: ${portfolio['total_current']:,.2f}")
        print(f"🎯 Ganancia/Pérdida: ${portfolio['total_profit_loss']:,.2f}")
        print(f"📈 ROI: {portfolio['total_profit_loss_percent']:.2f}%")
        print(f"📊 Estado: {portfolio['summary']['status']} {portfolio['summary']['emoji']}")
        
        print(f"\n{'─'*80}")
        print(f"📋 DETALLE DE HOLDINGS")
        print(f"{'─'*80}")
        print(f"{'Símbolo':<10} {'Cantidad':<12} {'P. Compra':<12} {'P. Actual':<12} {'Invertido':<12} {'Valor Actual':<12} {'G/P':<12} {'G/P %':<10}")
        print(f"{'─'*80}")
        
        for symbol, data in portfolio['holdings'].items():
            profit_emoji = "🟢" if data['profit_loss'] >= 0 else "🔴"
            print(f"{symbol:<10} {data['amount']:<12.4f} ${data['buy_price']:<11.2f} ${data['current_price']:<11.2f} "
                  f"${data['invested']:<11.2f} ${data['current_value']:<11.2f} "
                  f"{profit_emoji} ${data['profit_loss']:<9.2f} {data['profit_loss_percent']:>6.2f}%")
    
    def display_watchlist(self):
        """Mostrar watchlist con precios actuales"""
        print(f"\n{'─'*80}")
        print(f"👀 WATCHLIST")
        print(f"{'─'*80}")
        print(f"{'Símbolo':<10} {'Precio Actual':<15} {'Nota':<20}")
        print(f"{'─'*80}")
        
        for symbol in self.config['watchlist']:
            price = self.get_current_price(symbol)
            if price is not None:
                if symbol == "NXT":
                    note = "🚀 PRÓXIMAMENTE"
                else:
                    note = "📊 MONITOREANDO"
                print(f"{symbol:<10} ${price:<14.4f} {note:<20}")
    
    def save_portfolio_snapshot(self):
        """Guardar snapshot del portfolio"""
        try:
            os.makedirs('security/trading-bots/portfolio-tracker/data', exist_ok=True)
            
            snapshot_file = f"security/trading-bots/portfolio-tracker/data/portfolio_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(snapshot_file, 'w') as f:
                json.dump(self.portfolio_data, f, indent=2)
            
            # También guardar en archivo de historial
            history_file = "security/trading-bots/portfolio-tracker/data/portfolio_history.json"
            history_data = []
            
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history_data = json.load(f)
            
            history_data.append(self.portfolio_data)
            
            # Mantener solo las últimas 1000 entradas
            if len(history_data) > 1000:
                history_data = history_data[-1000:]
            
            with open(history_file, 'w') as f:
                json.dump(history_data, f, indent=2)
                
            self.logger.info("✅ Snapshot del portfolio guardado")
            
        except Exception as e:
            self.logger.error(f"❌ Error guardando snapshot: {e}")
    
    def generate_performance_report(self):
        """Generar reporte de performance"""
        portfolio = self.portfolio_data
        
        print(f"\n{'─'*80}")
        print(f"📈 REPORTE DE PERFORMANCE")
        print(f"{'─'*80}")
        
        # Holding con mejor performance
        best_performer = max(
            portfolio['holdings'].items(), 
            key=lambda x: x[1]['profit_loss_percent'],
            default=(None, {})
        )
        
        # Holding con peor performance
        worst_performer = min(
            portfolio['holdings'].items(), 
            key=lambda x: x[1]['profit_loss_percent'],
            default=(None, {})
        )
        
        if best_performer[0]:
            print(f"🏆 MEJOR PERFORMANCE: {best_performer[0]} - {best_performer[1]['profit_loss_percent']:.2f}%")
        
        if worst_performer[0]:
            print(f"📉 PEOR PERFORMANCE: {worst_performer[0]} - {worst_performer[1]['profit_loss_percent']:.2f}%")
        
        # Distribución del portfolio
        print(f"\n📊 DISTRIBUCIÓN DEL PORTFOLIO:")
        for symbol, data in portfolio['holdings'].items():
            allocation = (data['current_value'] / portfolio['total_current']) * 100
            print(f"   {symbol}: {allocation:.1f}%")
    
    def run_continuous_tracking(self):
        """Ejecutar seguimiento continuo"""
        print("🚀 NEXTIA PORTFOLIO TRACKER 2025")
        print("💎 Seguimiento de inversiones en tiempo real")
        print(f"⏰ Actualizando cada {self.config['update_interval']} segundos...")
        print("📍 Presiona CTRL + C para detener")
        
        update_count = 0
        
        try:
            while True:
                update_count += 1
                print(f"\n🔄 ACTUALIZACIÓN #{update_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Mostrar portfolio
                self.display_portfolio()
                
                # Mostrar watchlist
                self.display_watchlist()
                
                # Generar reporte de performance
                self.generate_performance_report()
                
                # Guardar snapshot
                self.save_portfolio_snapshot()
                
                print(f"\n💤 Próxima actualización en {self.config['update_interval']} segundos...")
                time.sleep(self.config['update_interval'])
                
        except KeyboardInterrupt:
            print(f"\n🛑 Portfolio Tracker detenido")
            print(f"📊 Total de actualizaciones: {update_count}")

    def run_single_update(self):
        """Ejecutar una sola actualización"""
        print("🚀 NEXTIA PORTFOLIO TRACKER 2025 - ACTUALIZACIÓN ÚNICA")
        self.display_portfolio()
        self.display_watchlist()
        self.generate_performance_report()
        self.save_portfolio_snapshot()

if __name__ == "__main__":
    tracker = NextiaPortfolioTracker()
    
    # Preguntar modo de ejecución
    print("🎯 Selecciona modo de ejecución:")
    print("1. Seguimiento continuo (automático)")
    print("2. Actualización única")
    
    try:
        choice = input("👉 Ingresa tu elección (1 o 2): ").strip()
        
        if choice == "1":
            tracker.run_continuous_tracking()
        else:
            tracker.run_single_update()
            
    except KeyboardInterrupt:
        print("\n🛑 Ejecución cancelada por el usuario")
