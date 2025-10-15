#!/usr/bin/env python3
"""
Nextia Market Analyzer 2025 - Análisis de tendencias y trading
Herramienta oficial del ecosistema Nextia Token
"""
import requests
import time
import json
import pandas as pd
import os
from datetime import datetime, timedelta

class NextiaMarketAnalyzer:
    def __init__(self):
        self.setup_logging()
        # Símbolos a analizar (NXT se agregará cuando esté en exchanges)
        self.symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT']
        
    def setup_logging(self):
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('NextiaMarketAnalyzer')
    
    def get_price_data(self, symbol, interval='1h', limit=100):
        """Obtener datos de precios históricos desde Binance"""
        try:
            url = f"https://api.binance.com/api/v3/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Procesar datos en DataFrame
            df = pd.DataFrame(data, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Convertir tipos de datos
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_columns:
                df[col] = df[col].astype(float)
            
            # Convertir timestamps
            df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error obteniendo datos de {symbol}: {e}")
            return None
    
    def calculate_sma(self, df, period=20):
        """Calcular Media Móvil Simple"""
        return df['close'].rolling(window=period).mean()
    
    def calculate_ema(self, df, period=12):
        """Calcular Media Móvil Exponencial"""
        return df['close'].ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, df, period=14):
        """Calcular RSI (Relative Strength Index)"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, df):
        """Calcular MACD"""
        ema_12 = self.calculate_ema(df, 12)
        ema_26 = self.calculate_ema(df, 26)
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        return macd, signal, histogram
    
    def analyze_trend(self, df):
        """Analizar tendencia del mercado"""
        if len(df) < 50:
            return {"error": "Insuficientes datos para análisis"}
        
        try:
            # Calcular indicadores
            sma_20 = self.calculate_sma(df, 20)
            sma_50 = self.calculate_sma(df, 50)
            rsi = self.calculate_rsi(df, 14)
            macd, signal, histogram = self.calculate_macd(df)
            
            current_price = df['close'].iloc[-1]
            sma_20_current = sma_20.iloc[-1]
            sma_50_current = sma_50.iloc[-1]
            rsi_current = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
            macd_current = macd.iloc[-1] if not pd.isna(macd.iloc[-1]) else 0
            signal_current = signal.iloc[-1] if not pd.isna(signal.iloc[-1]) else 0
            
            # Determinar tendencia principal
            if current_price > sma_20_current > sma_50_current:
                trend_strength = "FUERTE ALCISTA"
                trend_emoji = "📈"
            elif current_price > sma_20_current:
                trend_strength = "ALCISTA MODERADA" 
                trend_emoji = "↗️"
            elif current_price < sma_20_current < sma_50_current:
                trend_strength = "FUERTE BAJISTA"
                trend_emoji = "📉"
            elif current_price < sma_20_current:
                trend_strength = "BAJISTA MODERADA"
                trend_emoji = "↘️"
            else:
                trend_strength = "LATERAL"
                trend_emoji = "➡️"
            
            # Análisis RSI
            if rsi_current > 70:
                rsi_signal = "SOBRECOMPRADO"
                rsi_emoji = "📛"
            elif rsi_current < 30:
                rsi_signal = "SOBREVENDIDO" 
                rsi_emoji = "🟢"
            else:
                rsi_signal = "NEUTRO"
                rsi_emoji = "⚪"
            
            # Análisis MACD
            if macd_current > signal_current:
                macd_signal = "ALCISTA"
                macd_emoji = "🟢"
            else:
                macd_signal = "BAJISTA"
                macd_emoji = "🔴"
            
            return {
                'trend': f"{trend_emoji} {trend_strength}",
                'rsi': f"{rsi_emoji} RSI: {rsi_current:.1f} - {rsi_signal}",
                'macd': f"{macd_emoji} MACD: {macd_signal}",
                'current_price': current_price,
                'sma_20': sma_20_current,
                'sma_50': sma_50_current,
                'rsi_value': rsi_current,
                'macd_value': macd_current,
                'signal_value': signal_current
            }
            
        except Exception as e:
            return {"error": f"Error en análisis: {e}"}
    
    def generate_signals(self, analysis):
        """Generar señales de trading"""
        if "error" in analysis:
            return ["⚪ ANÁLISIS NO DISPONIBLE"]
        
        signals = []
        current_price = analysis['current_price']
        rsi = analysis['rsi_value']
        macd = analysis['macd_value']
        signal = analysis['signal_value']
        
        # Señales basadas en RSI
        if rsi < 30:
            signals.append("🎯 OPORTUNIDAD COMPRA - RSI indica SOBREVENTA")
        elif rsi > 70:
            signals.append("⚠️ PRECAUCIÓN - RSI indica SOBRECOMPRA")
        
        # Señales basadas en tendencia y RSI
        if "ALCISTA" in analysis['trend'] and rsi < 65:
            signals.append("🟢 SEÑAL COMPRA - Tendencia alcista con RSI favorable")
        
        if "BAJISTA" in analysis['trend'] and rsi > 35:
            signals.append("🔴 SEÑAL VENTA - Tendencia bajista con RSI alto")
        
        # Señales MACD
        if macd > signal and rsi < 60:
            signals.append("📈 MOMENTO ALCISTA - MACD positivo")
        elif macd < signal and rsi > 40:
            signals.append("📉 MOMENTO BAJISTA - MACD negativo")
        
        return signals if signals else ["⚪ SIN SEÑALES CLARAS - Mercado en consolidación"]
    
    def get_current_price(self, symbol):
        """Obtener precio actual"""
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(url, timeout=10)
            data = response.json()
            return float(data['price'])
        except:
            return None
    
    def run_analysis(self):
        """Ejecutar análisis completo para todos los símbolos"""
        print(f"\n{'='*70}")
        print("🚀 NEXTIA MARKET ANALYZER 2025 - ANÁLISIS EN TIEMPO REAL")
        print(f"{'='*70}")
        
        for symbol in self.symbols:
            try:
                print(f"\n📊 ANALIZANDO: {symbol}")
                print("-" * 50)
                
                # Obtener datos
                df = self.get_price_data(symbol)
                if df is None or len(df) < 50:
                    print(f"❌ Datos insuficientes para {symbol}")
                    continue
                
                # Análisis técnico
                analysis = self.analyze_trend(df)
                
                if "error" in analysis:
                    print(f"❌ Error en análisis: {analysis['error']}")
                    continue
                
                # Mostrar resultados
                current_price = self.get_current_price(symbol)
                if current_price:
                    print(f"💰 Precio Actual: ${current_price:,.2f}")
                
                print(f"📈 {analysis['trend']}")
                print(f"📊 {analysis['rsi']}")
                print(f"🎯 {analysis['macd']}")
                print(f"📏 SMA 20: ${analysis['sma_20']:,.2f}")
                print(f"📏 SMA 50: ${analysis['sma_50']:,.2f}")
                
                # Señales de trading
                signals = self.generate_signals(analysis)
                print(f"\n🔔 SEÑALES DE TRADING:")
                for signal in signals:
                    print(f"   • {signal}")
                
                # Guardar análisis
                self.save_analysis(symbol, analysis, signals)
                
            except Exception as e:
                print(f"❌ Error analizando {symbol}: {e}")
    
    def save_analysis(self, symbol, analysis, signals):
        """Guardar análisis para histórico"""
        # Asegurar que el directorio existe
        os.makedirs('security/trading-bots/market-analyzer/logs', exist_ok=True)
        
        analysis_data = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis,
            'signals': signals
        }
        
        log_file = 'security/trading-bots/market-analyzer/logs/analysis_log.json'
        with open(log_file, 'a') as f:
            f.write(json.dumps(analysis_data) + '\n')
    
    def run_continuous_analysis(self, interval_minutes=60):
        """Ejecutar análisis continuo"""
        print("🚀 NEXTIA MARKET ANALYZER 2025")
        print("💡 Análisis técnico automático de criptomercados")
        print(f"⏰ Actualizando cada {interval_minutes} minutos...")
        print("📍 Presiona CTRL + C para detener")
        print("💎 Símbolos monitoreados: BTC, ETH, ADA, DOT")
        print("")
        
        analysis_count = 0
        
        try:
            while True:
                analysis_count += 1
                print(f"\n🔄 ANÁLISIS #{analysis_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                self.run_analysis()
                
                print(f"\n💤 Próximo análisis en {interval_minutes} minutos...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Market Analyzer detenido")
            print(f"📊 Total de análisis realizados: {analysis_count}")

if __name__ == "__main__":
    analyzer = NextiaMarketAnalyzer()
    analyzer.run_continuous_analysis(interval_minutes=60)  # Análisis cada hora
