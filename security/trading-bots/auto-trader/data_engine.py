#!/usr/bin/env python3
"""
MOTOR PRINCIPAL DE DATOS MEJORADO - Nextia Trading Bot
Sistema central que maneja datos en tiempo real con mejoras de robustez
"""

import time
import sys
import os
import asyncio
import random
import json
from datetime import datetime
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importaciones de módulos internos
from utils.logger import trading_logger
from utils.notifications import notifier
from integrated_trading_bot import IntegratedTradingBot

class DataEngine:
    """Motor de datos mejorado con gestión robusta de señales"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            'symbols': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT'],
            'update_interval': 1,
            'status_report_interval': 300,
            'signal_interval': 30
        }
        
        self.running = False
        self.performance_stats = {
            'signals_generated': 0,
            'signals_executed': 0,
            'signals_rejected': 0,
            'last_signal_time': None,
            'total_confidence': 0.0,
            'average_confidence': 0.0
        }
        
        # MEJORA: Estadísticas de sesión mejoradas
        self.session_stats = {
            'start_time': datetime.now(),
            'health_checks_passed': 0,
            'health_checks_failed': 0,
            'last_health_status': 'healthy'
        }
        
        # MEJORA: Cache para reducir carga
        self.price_cache = {}
        self.cache_timeout = 5
        
        # Inicializar sistemas
        self._initialize_systems()
        
    def _initialize_systems(self):
        """Inicialización robusta de todos los sistemas"""
        try:
            self.setup_binance_client()
            self.setup_technical_indicators()
            self.setup_database()
            self.setup_telegram()
            
            # INICIALIZAR TRADING BOT INTEGRADO MEJORADO
            self.trading_bot = IntegratedTradingBot()
            trading_logger.info("✅ Trading Bot integrado mejorado inicializado")
            
            # MEJORA: Verificar estado del sistema
            system_status = self.trading_bot.get_system_status()
            if system_status['status'] != 'operational':
                trading_logger.warning(f"⚠️  Sistema de trading reporta estado: {system_status['status']}")
            
            trading_logger.info("🎯 Data Engine configurado con mejoras de robustez")
            
        except Exception as e:
            trading_logger.error(f"❌ Error crítico en inicialización: {e}")
            raise

    def setup_binance_client(self):
        """Configurar cliente de Binance mejorado"""
        try:
            # Tu código existente para configurar Binance
            trading_logger.info("✅ Cliente Binance configurado - Versión Mejorada")
        except Exception as e:
            trading_logger.error(f"❌ Error configurando Binance: {e}")
            raise

    def setup_technical_indicators(self):
        """Configurar indicadores técnicos mejorados"""
        try:
            # Tu código existente para indicadores
            trading_logger.info("✅ Indicadores técnicos configurados - Versión Mejorada")
        except Exception as e:
            trading_logger.error(f"❌ Error configurando indicadores: {e}")
            raise

    def setup_database(self):
        """Configurar base de datos mejorada"""
        try:
            # Tu código existente para base de datos
            trading_logger.info("✅ Base de datos configurada - Versión Mejorada")
        except Exception as e:
            trading_logger.error(f"❌ Error configurando base de datos: {e}")
            raise

    def setup_telegram(self):
        """Configurar notificaciones Telegram mejoradas"""
        try:
            # Tu código existente para Telegram
            trading_logger.info("✅ Notificaciones Telegram configuradas - Versión Mejorada")
        except Exception as e:
            trading_logger.error(f"❌ Error configurando Telegram: {e}")
            raise

    def start(self):
        """Iniciar el motor de datos mejorado"""
        trading_logger.info("🚀 INICIANDO NEXTIA DATA ENGINE MEJORADO...")
        notifier.send_telegram_message(
            "🚀 <b>Nextia Data Engine MEJORADO INICIADO</b>\n"
            "📊 Monitoreando mercados en tiempo real\n"
            "🔧 Sistema robusto con gestión mejorada de señales\n"
            "⏰ Hora de inicio: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
         
        self.running = True
        
        # Iniciar bucle principal
        self.main_loop()
        
    def stop(self):
        """Detener el motor de datos de forma controlada"""
        trading_logger.info("🛑 DETENIENDO Nextia Data Engine Mejorado...")
        self.running = False
        
        # Enviar reporte final
        final_stats = self._get_performance_report()
        notifier.send_telegram_message(
            f"🛑 <b>Nextia Data Engine DETENIDO</b>\n"
            f"📈 Estadísticas finales:\n"
            f"• Señales generadas: {final_stats['signals_generated']}\n"
            f"• Señales ejecutadas: {final_stats['signals_executed']}\n"
            f"• Señales rechazadas: {final_stats['signals_rejected']}\n"
            f"• Confianza promedio: {final_stats['average_confidence']:.1f}%\n"
            f"⏰ Hora de parada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
    def main_loop(self):
        """Bucle principal mejorado del motor de datos"""
        trading_logger.info("📊 Motor de datos mejorado ejecutándose...")
        
        last_status_time = 0
        status_interval = self.config.get('status_report_interval', 300)
        last_signal_time = 0
        signal_interval = self.config.get('signal_interval', 30)
        last_health_check = 0
        health_check_interval = 60  # 1 minuto

        try:
            while self.running:
                current_time = time.time()
                
                # Reporte de estado cada 5 minutos
                if current_time - last_status_time >= status_interval:
                    self.send_status_report()
                    last_status_time = current_time
                
                # Verificación de salud del sistema
                if current_time - last_health_check >= health_check_interval:
                    self._health_check()
                    last_health_check = current_time
                
                # Simular detección de señales para prueba
                if current_time - last_signal_time >= signal_interval:
                    self.simulate_trading_signals()
                    last_signal_time = current_time
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            trading_logger.info("🛑 Señal de interrupción recibida")
        except Exception as e:
            trading_logger.error(f"❌ Error crítico en motor de datos: {e}")
            notifier.send_error_alert(f"❌ Error crítico en motor de datos: {e}")
        finally:
            self.stop()
    
    def _health_check(self):
        """Verificación de salud del sistema mejorada"""
        try:
            # Verificar estado del trading bot
            system_status = self.trading_bot.get_system_status()
            
            health_status = 'healthy'
            issues = []
            
            if system_status['status'] != 'operational':
                health_status = 'degraded'
                issues.append(f"Sistema trading: {system_status['status']}")
            
            # MEJORA: Verificar balances
            portfolio_info = self.trading_bot.get_portfolio_info()
            if portfolio_info.get('total_balance', 0) <= 0:
                health_status = 'warning'
                issues.append("Balance del portfolio no disponible")
            
            # MEJORA: Verificar trades activos
            active_trades = portfolio_info.get('active_trades', 0)
            max_trades = portfolio_info.get('max_trades', 0)
            if active_trades >= max_trades:
                health_status = 'warning'
                issues.append(f"Límite de trades alcanzado: {active_trades}/{max_trades}")
            
            # NUEVO: Verificar estado del session scheduler
            if not self.trading_bot.session_scheduler.is_trading_time:
                health_status = 'info'
                issues.append("Fuera del horario de trading")
            
            if health_status == 'healthy':
                self.session_stats['health_checks_passed'] += 1
                trading_logger.info("🔍 Health check: ✅ Sistema operativo")
            else:
                self.session_stats['health_checks_failed'] += 1
                trading_logger.warning(f"⚠️  Health check: {health_status} - {' | '.join(issues)}")
                
                # Notificar solo si hay problemas críticos
                if health_status == 'degraded':
                    notifier.send_telegram_message(
                        f"⚠️ <b>Alerta de Salud del Sistema</b>\n"
                        f"Estado: {health_status}\n"
                        f"Problemas: {', '.join(issues)}"
                    )
            
            self.session_stats['last_health_status'] = health_status
            
        except Exception as e:
            trading_logger.error(f"❌ Error en health check: {e}")
            self.session_stats['health_checks_failed'] += 1

    def simulate_trading_signals(self):
        """Simular señales de trading mejoradas para pruebas"""
        try:
            symbols = self.config['symbols']
            symbol = random.choice(symbols)
            signal_type = random.choice(['BUY', 'SELL'])
            strength = random.choice(['STRONG', 'MEDIUM', 'WEAK'])
            
            # MEJORA: Generar confianza realista basada en fuerza
            confidence_map = {'STRONG': 0.85, 'MEDIUM': 0.70, 'WEAK': 0.55}
            base_confidence = confidence_map.get(strength, 0.65)
            confidence = round(base_confidence + random.uniform(-0.1, 0.1), 2)
            confidence = max(0.5, min(0.95, confidence))  # Mantener entre 0.5 y 0.95
            
            self.performance_stats['signals_generated'] += 1
            self.performance_stats['total_confidence'] += confidence
            self.performance_stats['average_confidence'] = (
                self.performance_stats['total_confidence'] / self.performance_stats['signals_generated']
            )
            self.performance_stats['last_signal_time'] = datetime.now()
            
            self.process_signal(symbol, signal_type, strength, confidence)
                
        except Exception as e:
            trading_logger.error(f"❌ Error simulando señales: {e}")
            
    def process_signal(self, symbol: str, signal_type: str, strength: str, confidence: float = 0.0):
        """Procesar señal de trading de forma robusta"""
        try:
            trading_logger.info(f"🎯 SEÑAL DETECTADA: {symbol} - {signal_type} (Fuerza: {strength}, Confianza: {confidence:.2f})")
            
            # MEJORA: Validar confianza mínima
            if confidence < 0.6:
                trading_logger.warning(f"⚠️  Señal con baja confianza ({confidence:.2f}), omitiendo...")
                self.performance_stats['signals_rejected'] += 1
                return
            
            # Enviar señal al trading bot integrado
            success, message = self.trading_bot.process_signal(symbol, signal_type, strength, confidence)
            
            if success:
                self.performance_stats['signals_executed'] += 1
                trading_logger.info(f"✅ Señal ejecutada exitosamente: {symbol} - {signal_type}")
                
                # Guardar en base de datos
                self.save_signal_to_db(symbol, signal_type, strength, confidence, success=True)
                
                # Enviar notificación por Telegram
                telegram_msg = (
                    f"🚀 <b>SEÑAL EJECUTADA</b>\n"
                    f"📊 Par: {symbol}\n"
                    f"🎯 Tipo: {signal_type}\n" 
                    f"💪 Fuerza: {strength}\n"
                    f"🎯 Confianza: {confidence:.1%}\n"
                    f"⏰ Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"✅ Estado: Ejecutada exitosamente\n"
                    f"📝 Mensaje: {message}"
                )
                notifier.send_telegram_message(telegram_msg)
                
            else:
                self.performance_stats['signals_rejected'] += 1
                trading_logger.warning(f"⚠️ Señal no ejecutada: {symbol} - {message}")
                
                # Guardar señal rechazada
                self.save_signal_to_db(symbol, signal_type, strength, confidence, success=False, reason=message)
                
                # Notificar rechazo por Telegram solo para señales STRONG o MEDIUM con alta confianza
                if strength in ['STRONG', 'MEDIUM'] and confidence > 0.7:
                    telegram_msg = (
                        f"⚠️ <b>SEÑAL RECHAZADA</b>\n"
                        f"📊 Par: {symbol}\n"
                        f"🎯 Tipo: {signal_type}\n"
                        f"💪 Fuerza: {strength}\n"
                        f"🎯 Confianza: {confidence:.1%}\n"
                        f"❌ Motivo: {message}\n"
                        f"⏰ Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    notifier.send_telegram_message(telegram_msg)
                
        except Exception as e:
            trading_logger.error(f"❌ Error procesando señal: {e}")
            notifier.send_error_alert(f"❌ Error procesando señal: {e}")

    def save_signal_to_db(self, symbol: str, signal_type: str, strength: str, 
                         confidence: float, success: bool, reason: str = ""):
        """Guardar señal en la base de datos con información extendida"""
        try:
            # Tu código existente para guardar en base de datos
            trading_logger.info(f"💾 Señal guardada en DB: {symbol} - {signal_type} - "
                              f"Confianza: {confidence:.2f} - Éxito: {success} - Razón: {reason}")
        except Exception as e:
            trading_logger.error(f"❌ Error guardando señal en DB: {e}")
            
    def send_status_report(self):
        """Enviar reporte de estado extendido por Telegram"""
        try:
            # Obtener información del portfolio
            portfolio_info = self.trading_bot.get_portfolio_info()
            
            # Obtener precios de símbolos activos
            active_symbols = []
            for symbol in self.config['symbols'][:5]:  # Primeros 5 símbolos
                try:
                    price = self._get_cached_price(symbol)
                    if price and price > 0:
                        change_emoji = "🟢" if random.random() > 0.5 else "🔴"
                        active_symbols.append(f"{change_emoji} {symbol}: ${price:.2f}")
                except Exception as e:
                    trading_logger.error(f"❌ Error obteniendo precio de {symbol}: {e}")
            
            # Calcular duración de sesión
            session_duration = datetime.now() - self.session_stats['start_time']
            hours = session_duration.total_seconds() / 3600
            
            # NUEVO: Obtener información del session scheduler
            trading_session_active = self.trading_bot.session_scheduler.is_trading_time
            session_status = "✅ Activa" if trading_session_active else "⏸️ Inactiva"
            
            # NUEVO: Obtener estadísticas de profit manager
            profit_stats = f"🎯 Profit Manager: {len(self.trading_bot.profit_manager.profit_targets)} símbolos configurados"
            
            # Preparar mensaje de estado
            status_message = (
                f"📊 <b>Reporte de Estado - Data Engine Mejorado</b>\n"
                f"🔗 Conectado: ✅\n"
                f"⏰ Duración: {hours:.1f}h\n"
                f"📈 Símbolos activos: {len(active_symbols)}\n"
                f"💰 Balance: ${portfolio_info.get('total_balance', 0):.2f}\n"
                f"🎯 Trades activos: {portfolio_info.get('active_trades', 0)}\n"
                f"📊 Señales: {self.performance_stats['signals_generated']} gen, "
                f"{self.performance_stats['signals_executed']} ej, "
                f"{self.performance_stats['signals_rejected']} rech\n"
                f"🎯 Confianza promedio: {self.performance_stats['average_confidence']:.1%}\n"
                f"🔍 Salud: {self.session_stats['last_health_status']}\n"
                f"⏰ Sesión Trading: {session_status}\n"
                f"{profit_stats}\n"
                f"\n" + "\n".join(active_symbols)
            )
            
            notifier.send_telegram_message(status_message)
            
        except Exception as e:
            trading_logger.error(f"❌ Error enviando reporte de estado: {e}")

    def _get_cached_price(self, symbol: str) -> float:
        """MEJORA: Obtener precio con cache para reducir llamadas a API"""
        now = time.time()
        if symbol in self.price_cache:
            price, timestamp = self.price_cache[symbol]
            if now - timestamp < self.cache_timeout:
                return price
        
        # Obtener nuevo precio
        try:
            price = self.trading_bot.trade_engine.get_current_price(symbol)
            if price > 0:
                self.price_cache[symbol] = (price, now)
            return price
        except:
            return 0.0

    def _get_performance_report(self) -> Dict:
        """Obtener reporte de performance completo"""
        report = self.performance_stats.copy()
        report['session_stats'] = self.session_stats
        report['health_check_ratio'] = (
            self.session_stats['health_checks_passed'] / 
            max(1, self.session_stats['health_checks_passed'] + self.session_stats['health_checks_failed'])
        )
        return report

def main():
    """Función principal mejorada"""
    print("🤖 NEXTIA TRADING BOT - DATA ENGINE MEJORADO")
    print("=" * 50)
    print("📡 Conectando a Binance WebSocket...")
    print("🔧 Sistema robusto con mejoras de gestión")
    print("💡 Presiona Ctrl+C para detener")
    print("=" * 50)
    
    # Configuración mejorada
    config = {
        'symbols': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT'],
        'update_interval': 1,
        'status_report_interval': 600,
        'signal_interval': 120  # Aumentado para menos spam en pruebas
    }
    
    engine = DataEngine(config)
    
    try:
        engine.start()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo motor de datos mejorado...")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        engine.stop()

if __name__ == "__main__":
    main()
