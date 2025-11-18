# market_scanner.py
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json

class NextiaMarketScanner:
    def __init__(self):
        self.binance_url = "https://api.binance.com/api/v3"
        self.coingecko_url = "https://api.coingecko.com/api/v3"
        
    def get_fear_greed_index(self):
        """Obtener Fear & Greed Index de Crypto"""
        try:
            url = "https://api.alternative.me/fng/"
            response = requests.get(url, timeout=10)
            data = response.json()
            return {
                'value': int(data['data'][0]['value']),
                'classification': data['data'][0]['value_classification']
            }
        except Exception as e:
            print(f"❌ Error Fear & Greed: {e}")
            return {'value': 50, 'classification': 'Neutral'}
    
    def get_btc_dominance(self):
        """Obtener Dominancia de Bitcoin"""
        try:
            url = f"{self.coingecko_url}/global"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data['data']['market_cap_percentage']['btc']
        except Exception as e:
            print(f"❌ Error BTC Dominance: {e}")
            return 40.0

    def get_eth_dominance(self):
        """Obtener Dominancia de Ethereum"""
        try:
            url = f"{self.coingecko_url}/global"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data['data']['market_cap_percentage']['eth']
        except Exception as e:
            print(f"❌ Error ETH Dominance: {e}")
            return 18.0
    
    def get_crypto_volatility(self, symbol="BTCUSDT"):
        """Calcular volatilidad mejorada"""
        try:
            url = f"{self.binance_url}/klines"
            params = {
                'symbol': symbol,
                'interval': '1h',
                'limit': 48  # 48 horas para mejor análisis
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if not data:
                return 0.0
                
            closes = [float(candle[4]) for candle in data]
            highs = [float(candle[2]) for candle in data]
            lows = [float(candle[3]) for candle in data]
            
            # Calcular volatilidad porcentual
            price_changes = []
            for i in range(1, len(closes)):
                change = ((closes[i] - closes[i-1]) / closes[i-1]) * 100
                price_changes.append(abs(change))
            
            avg_volatility = np.mean(price_changes) if price_changes else 0
            
            # Rango de trading adicional
            max_high = max(highs)
            min_low = min(lows)
            range_volatility = ((max_high - min_low) / min_low) * 100
            
            # Combinar ambas medidas
            total_volatility = (avg_volatility + range_volatility) / 2
            
            return round(total_volatility, 2)
        except Exception as e:
            print(f"❌ Error volatilidad {symbol}: {e}")
            return 0.0

    def get_btc_eth_volatility(self):
        """Obtener volatilidad combinada BTC y ETH"""
        btc_vol = self.get_crypto_volatility("BTCUSDT")
        eth_vol = self.get_crypto_volatility("ETHUSDT")
        
        # Usar la mayor volatilidad entre BTC y ETH
        combined_volatility = max(btc_vol, eth_vol)
        
        return {
            'btc_volatility': btc_vol,
            'eth_volatility': eth_vol,
            'combined_volatility': combined_volatility
        }
    
    def get_market_volume(self):
        """Obtener volumen de mercado mejorado"""
        try:
            # Volumen de BTC y ETH
            btc_volume = self.get_symbol_volume("BTCUSDT")
            eth_volume = self.get_symbol_volume("ETHUSDT")
            
            total_volume = btc_volume + eth_volume
            
            return {
                'btc_volume': btc_volume,
                'eth_volume': eth_volume,
                'total_volume': total_volume
            }
        except Exception as e:
            print(f"❌ Error volumen mercado: {e}")
            return {'btc_volume': 0, 'eth_volume': 0, 'total_volume': 0}
    
    def get_symbol_volume(self, symbol):
        """Obtener volumen para un símbolo específico"""
        try:
            url = f"{self.binance_url}/ticker/24hr"
            params = {'symbol': symbol}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return float(data['volume'])
        except:
            return 0

    def get_market_trend(self):
        """Determinar tendencia del mercado"""
        try:
            # Precios de BTC y ETH últimas 24h
            btc_data = self.get_24h_change("BTCUSDT")
            eth_data = self.get_24h_change("ETHUSDT")
            
            avg_change = (btc_data['priceChangePercent'] + eth_data['priceChangePercent']) / 2
            
            if avg_change > 2:
                return "BULLISH", avg_change
            elif avg_change < -2:
                return "BEARISH", avg_change
            else:
                return "SIDEWAYS", avg_change
                
        except Exception as e:
            print(f"❌ Error tendencia mercado: {e}")
            return "NEUTRAL", 0

    def get_24h_change(self, symbol):
        """Obtener cambio de precio en 24h"""
        try:
            url = f"{self.binance_url}/ticker/24hr"
            params = {'symbol': symbol}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return {
                'symbol': symbol,
                'priceChangePercent': float(data['priceChangePercent']),
                'lastPrice': float(data['lastPrice'])
            }
        except:
            return {'symbol': symbol, 'priceChangePercent': 0, 'lastPrice': 0}

    def calculate_risk_score(self, fear_greed, volatility_data, btc_dominance, eth_dominance, market_trend):
        """Calcular puntuación de riesgo mejorada"""
        risk_score = 0
        factors = []
        
        # 1. ANÁLISIS FEAR & GREED (25%)
        fg_value = fear_greed['value']
        if fg_value <= 20:  # Extreme Fear
            risk_score += 15
            fg_risk = "LOW"
        elif fg_value <= 40:  # Fear
            risk_score += 30
            fg_risk = "MEDIUM_LOW"
        elif fg_value <= 60:  # Neutral
            risk_score += 50
            fg_risk = "MEDIUM"
        elif fg_value <= 80:  # Greed
            risk_score += 70
            fg_risk = "MEDIUM_HIGH"
        else:  # Extreme Greed
            risk_score += 90
            fg_risk = "HIGH"
        factors.append(("Fear & Greed", fg_risk, fg_value))
        
        # 2. ANÁLISIS VOLATILIDAD (30%)
        volatility = volatility_data['combined_volatility']
        if volatility < 2:
            risk_score += 10
            vol_risk = "LOW"
        elif volatility < 4:
            risk_score += 25
            vol_risk = "MEDIUM_LOW"
        elif volatility < 7:
            risk_score += 45
            vol_risk = "MEDIUM"
        elif volatility < 10:
            risk_score += 70
            vol_risk = "MEDIUM_HIGH"
        else:
            risk_score += 90
            vol_risk = "HIGH"
        factors.append(("Volatility", vol_risk, volatility))
        
        # 3. ANÁLISIS DOMINANCIA (20%)
        total_dominance = btc_dominance + eth_dominance
        if total_dominance > 70:  # Mercado concentrado = más estable
            risk_score += 20
            dom_risk = "LOW"
        elif total_dominance > 60:
            risk_score += 40
            dom_risk = "MEDIUM"
        else:  # Baja dominancia = más riesgo en altcoins
            risk_score += 70
            dom_risk = "HIGH"
        factors.append(("BTC+ETH Dominance", dom_risk, total_dominance))
        
        # 4. ANÁLISIS TENDENCIA (25%)
        trend, trend_strength = market_trend
        if trend == "BULLISH" and abs(trend_strength) < 5:
            risk_score += 20
            trend_risk = "LOW"
        elif trend == "SIDEWAYS":
            risk_score += 40
            trend_risk = "MEDIUM"
        else:  # Bearish o movimientos muy fuertes
            risk_score += 70
            trend_risk = "HIGH"
        factors.append(("Market Trend", trend_risk, trend_strength))
        
        # Calcular riesgo promedio
        avg_risk = risk_score / 4
        
        # Determinar nivel de riesgo y recomendación
        if avg_risk <= 30:
            risk_level = "LOW"
            recommendation = "🟢 EXECUTE_BOT"
            confidence = "HIGH"
        elif avg_risk <= 50:
            risk_level = "MEDIUM"
            recommendation = "🟡 CAUTION - REDUCE POSITION SIZE"
            confidence = "MEDIUM"
        else:
            risk_level = "HIGH"
            recommendation = "🔴 WAIT - MARKET TOO RISKY"
            confidence = "HIGH"
        
        return {
            'risk_score': round(avg_risk, 1),
            'risk_level': risk_level,
            'recommendation': recommendation,
            'confidence': confidence,
            'factors': factors
        }

    def analyze_market_conditions(self):
        """Analizar todas las condiciones del mercado - VERSIÓN MEJORADA"""
        print("🔍 Analizando condiciones del mercado...")
        
        try:
            # Obtener todos los datos del mercado
            fear_greed = self.get_fear_greed_index()
            btc_dominance = self.get_btc_dominance()
            eth_dominance = self.get_eth_dominance()
            volatility_data = self.get_btc_eth_volatility()
            volume_data = self.get_market_volume()
            market_trend = self.get_market_trend()
            
            # Calcular riesgo mejorado
            risk_analysis = self.calculate_risk_score(
                fear_greed, volatility_data, btc_dominance, eth_dominance, market_trend
            )
            
            # Determinar mejores pares para trading
            best_pairs = self.get_recommended_pairs(risk_analysis['risk_level'])
            
            # Generar reporte completo
            report = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "recommendation": risk_analysis['recommendation'],
                "risk_level": risk_analysis['risk_level'],
                "risk_score": risk_analysis['risk_score'],
                "confidence": risk_analysis['confidence'],
                "market_analysis": {
                    "fear_greed": fear_greed,
                    "btc_dominance": round(btc_dominance, 1),
                    "eth_dominance": round(eth_dominance, 1),
                    "total_dominance": round(btc_dominance + eth_dominance, 1),
                    "volatility": {
                        'btc': volatility_data['btc_volatility'],
                        'eth': volatility_data['eth_volatility'],
                        'combined': volatility_data['combined_volatility']
                    },
                    "volume": volume_data,
                    "market_trend": {
                        'direction': market_trend[0],
                        'strength': round(market_trend[1], 2)
                    }
                },
                "risk_factors": risk_analysis['factors'],
                "trading_recommendations": {
                    "best_pairs": best_pairs,
                    "position_size": "60%" if risk_analysis['risk_level'] == "LOW" else "30%" if risk_analysis['risk_level'] == "MEDIUM" else "0%",
                    "optimal_hours": "14:00-18:00 UTC",
                    "max_trades": 15 if risk_analysis['risk_level'] == "LOW" else 8 if risk_analysis['risk_level'] == "MEDIUM" else 0
                }
            }
            
            return report
            
        except Exception as e:
            print(f"❌ Error en análisis de mercado: {e}")
            # Reporte de error
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "recommendation": "🔴 ERROR - NO DATA",
                "risk_level": "UNKNOWN",
                "risk_score": 100,
                "error": str(e)
            }

    def get_recommended_pairs(self, risk_level):
        """Obtener pares recomendados según el nivel de riesgo"""
        if risk_level == "LOW":
            return ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOTUSDT"]
        elif risk_level == "MEDIUM":
            return ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT"]
        else:
            return ["BTCUSDT"]  # Solo BTC en alto riesgo

    def continuous_monitoring(self, interval_minutes=5):
        """Monitoreo continuo del mercado - VERSIÓN MEJORADA"""
        print("🚀 INICIANDO NEXTIA MARKET SCANNER - VERSIÓN MEJORADA")
        print("📊 Incluye análisis BTC + ETH + Volatilidad + Tendencia")
        print("=" * 60)
        
        while True:
            try:
                report = self.analyze_market_conditions()
                
                # Display mejorado
                print(f"\n🕐 {report['timestamp']}")
                print(f"📈 RECOMENDACIÓN: {report['recommendation']}")
                print(f"⚠️  NIVEL RIESGO: {report['risk_level']} ({report['risk_score']}/100)")
                print(f"🎯 CONFIANZA: {report['confidence']}")
                
                # Análisis detallado
                print(f"\n📊 ANÁLISIS DETALLADO:")
                print(f"😨 FEAR/GREED: {report['market_analysis']['fear_greed']['value']} ({report['market_analysis']['fear_greed']['classification']})")
                print(f"₿ BTC DOMINANCE: {report['market_analysis']['btc_dominance']}%")
                print(f"🔷 ETH DOMINANCE: {report['market_analysis']['eth_dominance']}%")
                print(f"📊 VOLATILIDAD BTC: {report['market_analysis']['volatility']['btc']}%")
                print(f"📊 VOLATILIDAD ETH: {report['market_analysis']['volatility']['eth']}%")
                print(f"📈 TENDENCIA: {report['market_analysis']['market_trend']['direction']} ({report['market_analysis']['market_trend']['strength']}%)")
                print(f"💧 VOLUMEN BTC: {report['market_analysis']['volume']['btc_volume']:,.0f}")
                print(f"💧 VOLUMEN ETH: {report['market_analysis']['volume']['eth_volume']:,.0f}")
                
                # Factores de riesgo
                print(f"\n🔍 FACTORES DE RIESGO:")
                for factor, risk, value in report['risk_factors']:
                    print(f"   • {factor}: {risk} ({value})")
                
                # Recomendaciones de trading
                print(f"\n💡 RECOMENDACIONES DE TRADING:")
                print(f"   • Mejores pares: {', '.join(report['trading_recommendations']['best_pairs'])}")
                print(f"   • Tamaño posición: {report['trading_recommendations']['position_size']}")
                print(f"   • Máx trades/día: {report['trading_recommendations']['max_trades']}")
                print(f"   • Horario óptimo: {report['trading_recommendations']['optimal_hours']}")
                
                if report['recommendation'] == "🟢 EXECUTE_BOT":
                    print(f"\n🎯 ¡CONDICIONES ÓPTIMAS DETECTADAS!")
                    print("💡 Recomendación: Ejecutar trading bot con configuración normal")
                elif report['recommendation'] == "🟡 CAUTION - REDUCE POSITION SIZE":
                    print(f"\n⚠️  CONDICIONES MODERADAS")
                    print("💡 Recomendación: Reducir tamaño de posición y número de trades")
                else:
                    print(f"\n⏳ CONDICIONES DE ALTO RIESGO")
                    print("💡 Recomendación: Esperar mejor momento del mercado")
                
                print("=" * 60)
                
            except Exception as e:
                print(f"❌ Error en monitoreo: {e}")
                print("🔄 Reintentando en 30 segundos...")
                time.sleep(30)
                continue
            
            time.sleep(interval_minutes * 60)

# Función principal
if __name__ == "__main__":
    scanner = NextiaMarketScanner()
    scanner.continuous_monitoring()
