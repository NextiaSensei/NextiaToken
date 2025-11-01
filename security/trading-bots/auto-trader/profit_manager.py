# profit_manager.py
import json
import logging
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class ProfitManager:
    def __init__(self, config_path='config/trading_sessions.json'):
        self.config_path = config_path
        self.profit_targets = {}
        self.stop_losses = {}
        self.trailing_stops = {}
        self.position_sizing = {}
        self.daily_limits = {}
        self.risk_profiles = {}
        self.trade_history = []
        self.daily_pnl = 0.0
        self.max_daily_loss = 0.0
        self.session_start_time = datetime.now()
        
        self.load_config()
        logging.info("✅ ProfitManager mejorado inicializado")
    
    def load_config(self):
        """Carga la configuración mejorada de gestión de profits"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                
                # Configuración básica
                self.profit_targets = config.get('profit_targets', {
                    'BTCUSDT': 2.5,    # 2.5% target
                    'ETHUSDT': 3.0,    # 3.0% target  
                    'ADAUSDT': 4.0,    # 4.0% target
                    'DOTUSDT': 4.0,    # 4.0% target
                    'LINKUSDT': 3.5    # 3.5% target
                })
                
                self.stop_losses = config.get('stop_losses', {
                    'BTCUSDT': 1.5,    # 1.5% stop loss
                    'ETHUSDT': 2.0,    # 2.0% stop loss
                    'ADAUSDT': 2.5,    # 2.5% stop loss
                    'DOTUSDT': 2.5,    # 2.5% stop loss
                    'LINKUSDT': 2.0    # 2.0% stop loss
                })
                
                # 🚀 NUEVO: Trailing Stops dinámicos
                self.trailing_stops = config.get('trailing_stops', {
                    'BTCUSDT': 1.0,    # 1.0% trailing stop
                    'ETHUSDT': 1.2,    # 1.2% trailing stop
                    'ADAUSDT': 1.5,    # 1.5% trailing stop
                    'DOTUSDT': 1.5,    # 1.5% trailing stop
                    'LINKUSDT': 1.3    # 1.3% trailing stop
                })
                
                # 🚀 NUEVO: Position Sizing inteligente
                self.position_sizing = config.get('position_sizing', {
                    'max_position_per_trade': 0.2,      # 20% del balance por trade
                    'max_daily_trades': 8,              # Máximo 8 trades por día
                    'volatility_adjustment': True,      # Ajustar por volatilidad
                    'max_portfolio_risk': 0.02          # 2% riesgo máximo del portfolio
                })
                
                # 🚀 NUEVO: Límites diarios de protección
                self.daily_limits = config.get('daily_limits', {
                    'max_daily_loss': 0.02,             # 2% pérdida máxima diaria
                    'max_drawdown': 0.05,               # 5% drawdown máximo
                    'daily_profit_target': 0.04,        # 4% target de profit diario
                    'emergency_stop_loss': 0.03         # 3% stop loss de emergencia
                })
                
                # 🚀 NUEVO: Perfiles de riesgo por par
                self.risk_profiles = config.get('risk_profiles', {
                    'BTCUSDT': {'risk_level': 'low', 'volatility': 'medium'},
                    'ETHUSDT': {'risk_level': 'medium', 'volatility': 'high'},
                    'ADAUSDT': {'risk_level': 'high', 'volatility': 'high'},
                    'DOTUSDT': {'risk_level': 'high', 'volatility': 'high'},
                    'LINKUSDT': {'risk_level': 'medium', 'volatility': 'medium'}
                })
                
            logging.info("✅ ProfitManager config mejorada cargada exitosamente")
            
        except Exception as e:
            logging.error(f"❌ Error cargando configuración ProfitManager: {e}")
            # Configuración por defecto robusta
            self.set_default_config()
    
    def set_default_config(self):
        """Configuración por defecto de emergencia"""
        self.profit_targets = {'default': 2.0}
        self.stop_losses = {'default': 1.5}
        self.trailing_stops = {'default': 1.0}
        self.position_sizing = {
            'max_position_per_trade': 0.15,
            'max_daily_trades': 5,
            'volatility_adjustment': False,
            'max_portfolio_risk': 0.015
        }
        self.daily_limits = {
            'max_daily_loss': 0.015,
            'max_drawdown': 0.04,
            'daily_profit_target': 0.03,
            'emergency_stop_loss': 0.025
        }
    
    def calculate_dynamic_position_size(self, symbol: str, current_balance: float, 
                                      volatility: float = 1.0) -> float:
        """Calcula el tamaño de posición dinámico basado en volatilidad y riesgo"""
        try:
            max_trade_size = self.position_sizing.get('max_position_per_trade', 0.2)
            base_size = current_balance * max_trade_size
            
            # Ajustar por volatilidad si está activado
            if self.position_sizing.get('volatility_adjustment', True):
                risk_profile = self.risk_profiles.get(symbol, {})
                risk_level = risk_profile.get('risk_level', 'medium')
                
                # Multiplicadores de riesgo
                risk_multipliers = {
                    'low': 0.7,
                    'medium': 1.0,
                    'high': 0.5  # Reducir tamaño en alta volatilidad
                }
                
                size_multiplier = risk_multipliers.get(risk_level, 1.0)
                base_size *= size_multiplier
            
            # Aplicar límite de riesgo del portfolio
            max_portfolio_risk = self.position_sizing.get('max_portfolio_risk', 0.02)
            portfolio_risk_limit = current_balance * max_portfolio_risk
            
            return min(base_size, portfolio_risk_limit)
            
        except Exception as e:
            logging.error(f"❌ Error calculando position size: {e}")
            return current_balance * 0.1  # 10% por defecto seguro
    
    def check_trailing_stop(self, symbol: str, current_price: float, 
                          entry_price: float, position_type: str, 
                          highest_price: float = None, lowest_price: float = None) -> Tuple[bool, float]:
        """Verifica y actualiza trailing stops dinámicos"""
        try:
            if symbol not in self.trailing_stops:
                return False, None
            
            trailing_percent = self.trailing_stops[symbol]
            current_stop_price = None
            
            if position_type == 'long':
                # Para posiciones largas
                if highest_price is None:
                    highest_price = current_price
                
                if current_price > highest_price:
                    highest_price = current_price
                
                # Calcular trailing stop
                trailing_stop_price = highest_price * (1 - trailing_percent / 100)
                current_stop_price = trailing_stop_price
                
                # Verificar si el precio actual activa el trailing stop
                if current_price <= trailing_stop_price:
                    return True, trailing_stop_price
                    
            elif position_type == 'short':
                # Para posiciones cortas
                if lowest_price is None:
                    lowest_price = current_price
                
                if current_price < lowest_price:
                    lowest_price = current_price
                
                # Calcular trailing stop
                trailing_stop_price = lowest_price * (1 + trailing_percent / 100)
                current_stop_price = trailing_stop_price
                
                # Verificar si el precio actual activa el trailing stop
                if current_price >= trailing_stop_price:
                    return True, trailing_stop_price
            
            return False, current_stop_price
            
        except Exception as e:
            logging.error(f"❌ Error en trailing stop: {e}")
            return False, None
    
    def check_profit_target(self, symbol: str, current_price: float, 
                          entry_price: float, position_type: str) -> bool:
        """Verifica si se alcanzó el profit target mejorado"""
        try:
            target_percent = self.profit_targets.get(symbol, self.profit_targets.get('default', 2.0))
            
            if position_type == 'long':
                profit_percent = ((current_price - entry_price) / entry_price) * 100
                return profit_percent >= target_percent
            else:
                # Para short positions
                profit_percent = ((entry_price - current_price) / entry_price) * 100
                return profit_percent >= target_percent
                
        except Exception as e:
            logging.error(f"❌ Error verificando profit target: {e}")
            return False
    
    def check_stop_loss(self, symbol: str, current_price: float, 
                       entry_price: float, position_type: str) -> bool:
        """Verifica si se activó el stop loss mejorado"""
        try:
            stop_percent = self.stop_losses.get(symbol, self.stop_losses.get('default', 1.5))
            
            if position_type == 'long':
                loss_percent = ((entry_price - current_price) / entry_price) * 100
                return loss_percent >= stop_percent
            else:
                # Para short positions
                loss_percent = ((current_price - entry_price) / entry_price) * 100
                return loss_percent >= stop_percent
                
        except Exception as e:
            logging.error(f"❌ Error verificando stop loss: {e}")
            return False
    
    def check_daily_limits(self, current_balance: float, initial_balance: float) -> Dict[str, bool]:
        """Verifica todos los límites diarios de protección"""
        try:
            daily_pnl = ((current_balance - initial_balance) / initial_balance) * 100
            self.daily_pnl = daily_pnl
            
            max_daily_loss = self.daily_limits.get('max_daily_loss', 2.0)
            max_drawdown = self.daily_limits.get('max_drawdown', 5.0)
            daily_profit_target = self.daily_limits.get('daily_profit_target', 4.0)
            emergency_stop_loss = self.daily_limits.get('emergency_stop_loss', 3.0)
            
            limits_status = {
                'max_daily_loss_breached': daily_pnl <= -max_daily_loss,
                'max_drawdown_breached': daily_pnl <= -max_drawdown,
                'daily_profit_target_reached': daily_pnl >= daily_profit_target,
                'emergency_stop_activated': daily_pnl <= -emergency_stop_loss
            }
            
            # Loggear alertas importantes
            if limits_status['max_daily_loss_breached']:
                logging.warning(f"🚨 Límite diario de pérdida alcanzado: {daily_pnl:.2f}%")
            if limits_status['daily_profit_target_reached']:
                logging.info(f"🎯 Target diario de profit alcanzado: {daily_pnl:.2f}%")
            if limits_status['emergency_stop_activated']:
                logging.error(f"🚨 EMERGENCY STOP activado: {daily_pnl:.2f}%")
            
            return limits_status
            
        except Exception as e:
            logging.error(f"❌ Error verificando límites diarios: {e}")
            return {}
    
    def should_close_position(self, symbol: str, current_price: float, 
                            entry_price: float, position_type: str,
                            highest_price: float = None, lowest_price: float = None,
                            current_balance: float = None, initial_balance: float = None) -> Tuple[bool, str, Dict]:
        """Determina si cerrar posición con múltiples criterios mejorados"""
        try:
            close_reasons = []
            metadata = {}
            
            # 1. Verificar profit target
            if self.check_profit_target(symbol, current_price, entry_price, position_type):
                close_reasons.append("profit_target")
                metadata['profit_reason'] = f"Target alcanzado en {symbol}"
            
            # 2. Verificar stop loss tradicional
            if self.check_stop_loss(symbol, current_price, entry_price, position_type):
                close_reasons.append("stop_loss")
                metadata['stop_loss_reason'] = f"Stop loss activado en {symbol}"
            
            # 3. Verificar trailing stop
            trailing_stop_activated, trailing_price = self.check_trailing_stop(
                symbol, current_price, entry_price, position_type, highest_price, lowest_price
            )
            if trailing_stop_activated:
                close_reasons.append("trailing_stop")
                metadata['trailing_stop_price'] = trailing_price
            
            # 4. Verificar límites diarios (si se proporciona balance)
            if current_balance and initial_balance:
                daily_limits = self.check_daily_limits(current_balance, initial_balance)
                metadata['daily_limits'] = daily_limits
                
                if daily_limits.get('emergency_stop_activated'):
                    close_reasons.append("emergency_stop")
                elif daily_limits.get('max_daily_loss_breached'):
                    close_reasons.append("max_daily_loss")
                elif daily_limits.get('daily_profit_target_reached'):
                    close_reasons.append("daily_profit_target")
            
            # 5. Calcular métricas de performance
            if position_type == 'long':
                pnl_percent = ((current_price - entry_price) / entry_price) * 100
            else:
                pnl_percent = ((entry_price - current_price) / entry_price) * 100
            
            metadata['pnl_percent'] = pnl_percent
            metadata['current_price'] = current_price
            metadata['entry_price'] = entry_price
            
            # Registrar en historial
            trade_record = {
                'symbol': symbol,
                'position_type': position_type,
                'entry_price': entry_price,
                'exit_price': current_price,
                'pnl_percent': pnl_percent,
                'timestamp': datetime.now(),
                'close_reasons': close_reasons
            }
            self.trade_history.append(trade_record)
            
            should_close = len(close_reasons) > 0
            primary_reason = close_reasons[0] if close_reasons else None
            
            return should_close, primary_reason, metadata
            
        except Exception as e:
            logging.error(f"❌ Error en should_close_position: {e}")
            return False, None, {}
    
    def get_trade_recommendation(self, symbol: str, current_balance: float, 
                               signal_strength: str) -> Dict:
        """Genera recomendación completa para un trade"""
        try:
            position_size = self.calculate_dynamic_position_size(symbol, current_balance)
            risk_profile = self.risk_profiles.get(symbol, {})
            
            recommendation = {
                'symbol': symbol,
                'recommended_position_size': position_size,
                'risk_level': risk_profile.get('risk_level', 'medium'),
                'volatility': risk_profile.get('volatility', 'medium'),
                'profit_target': self.profit_targets.get(symbol, 2.0),
                'stop_loss': self.stop_losses.get(symbol, 1.5),
                'trailing_stop': self.trailing_stops.get(symbol, 1.0),
                'max_risk_per_trade': self.position_sizing.get('max_portfolio_risk', 0.02) * current_balance,
                'signal_strength': signal_strength,
                'timestamp': datetime.now()
            }
            
            return recommendation
            
        except Exception as e:
            logging.error(f"❌ Error generando recomendación: {e}")
            return {}
    
    def get_performance_metrics(self) -> Dict:
        """Retorna métricas de performance completas"""
        try:
            if not self.trade_history:
                return {}
            
            total_trades = len(self.trade_history)
            winning_trades = [t for t in self.trade_history if t['pnl_percent'] > 0]
            losing_trades = [t for t in self.trade_history if t['pnl_percent'] <= 0]
            
            win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
            avg_win = np.mean([t['pnl_percent'] for t in winning_trades]) if winning_trades else 0
            avg_loss = np.mean([t['pnl_percent'] for t in losing_trades]) if losing_trades else 0
            profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
            
            return {
                'total_trades': total_trades,
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades),
                'win_rate': win_rate * 100,
                'average_win': avg_win,
                'average_loss': avg_loss,
                'profit_factor': profit_factor,
                'daily_pnl': self.daily_pnl,
                'session_duration': (datetime.now() - self.session_start_time).total_seconds() / 3600
            }
            
        except Exception as e:
            logging.error(f"❌ Error calculando métricas: {e}")
            return {}
    
    def reset_daily_metrics(self):
        """Resetea las métricas diarias para nueva sesión"""
        self.trade_history.clear()
        self.daily_pnl = 0.0
        self.session_start_time = datetime.now()
        logging.info("✅ Métricas diarias reseteadas")

# Ejemplo de uso mejorado
if __name__ == "__main__":
    # Test del ProfitManager mejorado
    pm = ProfitManager()
    
    # Ejemplo de recomendación de trade
    recommendation = pm.get_trade_recommendation("BTCUSDT", 100000, "STRONG")
    print("🎯 Recomendación de Trade:", recommendation)
    
    # Ejemplo de verificación de cierre
    should_close, reason, metadata = pm.should_close_position(
        symbol="BTCUSDT",
        current_price=112000,
        entry_price=110000,
        position_type="long",
        current_balance=112000,
        initial_balance=110000
    )
    print(f"🤔 Cerrar posición: {should_close}, Razón: {reason}")
    print(f"📊 Metadata: {metadata}")
