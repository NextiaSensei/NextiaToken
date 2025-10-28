#!/usr/bin/env python3
"""
Módulo de Análisis Técnico - Indicadores y Señales
"""

import numpy as np
import pandas as pd
from utils.logger import trading_logger

class TechnicalAnalysis:
    def __init__(self):
        self.logger = trading_logger
    
    def calculate_sma(self, prices, period):
        """Calcular Media Móvil Simple (SMA)"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    def calculate_ema(self, prices, period):
        """Calcular Media Móvil Exponencial (EMA)"""
        if len(prices) < period:
            return None
        
        prices_series = pd.Series(prices)
        ema = prices_series.ewm(span=period, adjust=False).mean()
        return ema.iloc[-1]
    
    def calculate_rsi(self, prices, period=14):
        """Calcular Índice de Fuerza Relativa (RSI)"""
        if len(prices) < period + 1:
            return None
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calcular MACD"""
        if len(prices) < slow:
            return None, None
        
        prices_series = pd.Series(prices)
        
        ema_fast = prices_series.ewm(span=fast, adjust=False).mean()
        ema_slow = prices_series.ewm(span=slow, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]
    
    def generate_signals(self, symbol, current_price, historical_prices):
        """Generar señales de trading basadas en indicadores"""
        signals = []
        
        # Calcular indicadores
        sma_20 = self.calculate_sma(historical_prices, 20)
        sma_50 = self.calculate_sma(historical_prices, 50)
        rsi = self.calculate_rsi(historical_prices)
        macd, signal, histogram = self.calculate_macd(historical_prices)
        
        # Señal SMA Crossover
        if sma_20 and sma_50:
            if sma_20 > sma_50 and len(historical_prices) >= 2:
                if historical_prices[-2] <= sma_50 and current_price > sma_20:
                    signals.append({
                        'type': 'BUY',
                        'strength': 0.7,
                        'indicator': 'SMA_CROSSOVER',
                        'message': f'💰 SMA 20 cruzó por encima de SMA 50'
                    })
        
        # Señal RSI
        if rsi:
            if rsi < 30:
                signals.append({
                    'type': 'BUY',
                    'strength': 0.6,
                    'indicator': 'RSI_OVERSOLD',
                    'message': f'📉 RSI en zona de sobreventa: {rsi:.2f}'
                })
            elif rsi > 70:
                signals.append({
                    'type': 'SELL',
                    'strength': 0.6,
                    'indicator': 'RSI_OVERBOUGHT',
                    'message': f'📈 RSI en zona de sobrecompra: {rsi:.2f}'
                })
        
        # Señal MACD
        if macd and signal:
            if macd > signal and histogram > 0:
                signals.append({
                    'type': 'BUY',
                    'strength': 0.5,
                    'indicator': 'MACD_BULLISH',
                    'message': f'🐂 MACD tendencia alcista'
                })
        
        return signals, {
            'sma_20': sma_20,
            'sma_50': sma_50,
            'rsi': rsi,
            'macd': macd,
            'signal_line': signal
        }

# Instancia global
technical_analyzer = TechnicalAnalysis()
