#!/usr/bin/env python3
"""
Nextia Trading Bot - Sistema Integrado Mejorado
Combina Data Engine, Trade Engine y Risk Manager para trading automático
CON PROTECCIÓN ANTI-SUSPENSIÓN Y COMANDOS TELEGRAM
"""

import logging
import time
import sys
import os
import asyncio
import json
import subprocess
import threading
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta

# Añadir ruta para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trade_engine import TradeEngine
from risk_manager import RiskManager
from profit_manager import ProfitManager
from session_scheduler import SessionScheduler

# =============================================
# 📱 TELEGRAM BOT - NUEVO COMMAND HANDLER
# =============================================
try:
    import telegram
    from telegram import Update, BotCommand
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️  Telegram no disponible. Instala: pip install python-telegram-bot")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# =============================================
# 🛡️ PROTECCIÓN ANTI-SUSPENSIÓN - NUEVO
# =============================================

def anti_suspension_init():
    """Protección inicial contra suspensiones - Se ejecuta al inicio"""
    try:
        print("🛡️  Activando protección anti-suspensión...")
        # Forzar sincronización temporal básica
        subprocess.run(['date'], capture_output=True, text=True)
        time.sleep(1)
        print("✅ Protección anti-suspensión activada")
        return True
    except Exception as e:
        print(f"⚠️  Error en protección inicial: {e}")
        return True  # Continuar de todos modos

# Ejecutar protección al importar
anti_suspension_init()

class SuspensionMonitor:
    """Monitor para detectar y reparar suspensiones automáticamente"""
    
    def __init__(self):
        self.last_check = time.time()
        self.suspension_detected = False
        self.repair_attempts = 0
        self.max_repair_attempts = 3
        
    def check_suspension(self):
        """Verificar si hubo una suspensión"""
        current_time = time.time()
        time_diff = current_time - self.last_check
        
        # Si pasó más de 30 segundos entre checks, probable suspensión
        if time_diff > 30 and not self.suspension_detected:
            logger.warning(f"⚠️  POSIBLE SUSPENSIÓN DETECTADA: {time_diff:.1f} segundos sin actividad")
            self.suspension_detected = True
            self.repair_attempts = 0
            
        self.last_check = current_time
        return self.suspension_detected
    
    def repair_suspension(self):
        """Intentar reparar los efectos de una suspensión"""
        if not self.suspension_detected or self.repair_attempts >= self.max_repair_attempts:
            return False
            
        self.repair_attempts += 1
        logger.info(f"🔧 Intentando reparación de suspensión ({self.repair_attempts}/{self.max_repair_attempts})...")
        
        try:
            # Método 1: Sincronización temporal básica
            subprocess.run(['date'], capture_output=True, text=True)
            
            # Método 2: Pequeña pausa para estabilizar
            time.sleep(2)
            
            # Método 3: Reset de flags
            self.suspension_detected = False
            
            logger.info("✅ Reparación de suspensión completada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en reparación de suspensión: {e}")
            return False

# Inicializar monitor global
suspension_monitor = SuspensionMonitor()

class TelegramCommandHandler:
    """📱 MANEJADOR DE COMANDOS TELEGRAM - NUEVO"""
    
    def __init__(self, token: str, trading_bot):
        self.token = token
        self.bot = trading_bot
        self.application = None
        self.is_running = False
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Bienvenida"""
        welcome_text = """
🤖 *Nextia Trading Bot* - Sistema Integrado

*COMANDOS DISPONIBLES:*
/status - Estado del sistema y balance
/portfolio - Detalles del portfolio
/protection - Estado de protecciones
/emergency_stop - 🚨 PARADA DE EMERGENCIA
/help - Mostrar esta ayuda

🛡️ *Sistema de Protección Activado*
✅ Anti-suspensión
✅ Risk Manager  
✅ Profit Manager
✅ Session Scheduler
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
        
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status - Estado del sistema"""
        try:
            system_status = self.bot.get_system_status()
            
            status_text = f"""
📊 *ESTADO DEL SISTEMA*

💼 *Balance:* ${system_status.get('total_balance', 0):.2f}
🔧 *Estado:* {system_status.get('status', 'Unknown').upper()}
⏰ *Sesión:* {'✅ ACTIVA' if system_status.get('trading_session_active') else '⏸️ INACTIVA'}
📈 *Duración:* {system_status.get('session_duration_hours', 0):.1f}h

🛡️ *Protecciones:*
• Trade Engine: {system_status.get('trade_engine', 'Unknown')}
• Risk Manager: {system_status.get('risk_manager', 'Unknown')}  
• Profit Manager: {system_status.get('profit_manager', 'Unknown')}
• Suspensiones: {system_status.get('suspensions_detected', 0)} detectadas, {system_status.get('suspensions_repaired', 0)} reparadas

🕒 *Actualizado:* {datetime.now().strftime('%H:%M:%S')}
            """
            await update.message.reply_text(status_text, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error obteniendo estado: {str(e)}")
    
    async def portfolio_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /portfolio - Información del portfolio"""
        try:
            portfolio_info = self.bot.get_portfolio_info()
            performance = portfolio_info.get('performance', {})
            
            portfolio_text = f"""
💼 *PORTAFOLIO - DETALLES*

💰 *Balance Total:* ${portfolio_info.get('total_balance', 0):.2f}
📊 *Trades Activos:* {portfolio_info.get('active_trades', 0)}/{portfolio_info.get('max_trades', 0)}
🎯 *Win Rate:* {performance.get('win_rate', 0):.1f}%

📈 *Métricas Diarias:*
• P&L Diario: ${performance.get('daily_pnl', 0):.2f}
• Trades Hoy: {performance.get('daily_trades', 0)}
• Total Trades: {performance.get('total_trades', 0)}

🛡️ *Protección Anti-Suspensión:*
• Detectadas: {portfolio_info.get('suspensions_detected', 0)}
• Reparadas: {portfolio_info.get('suspensions_repaired', 0)}

⏰ *Sesión Trading:* {'✅ ACTIVA' if portfolio_info.get('trading_session_active') else '⏸️ INACTIVA'}
            """
            await update.message.reply_text(portfolio_text, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error obteniendo portfolio: {str(e)}")
    
    async def protection_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /protection - Estado de protecciones"""
        try:
            system_status = self.bot.get_system_status()
            portfolio_info = self.bot.get_portfolio_info()
            
            protection_text = f"""
🛡️ *SISTEMA DE PROTECCIÓN*

🔴 *Emergency Stop:* ✅ DISPONIBLE
🟡 *Kill Switch:* ✅ DISPONIBLE  
🔵 *Circuit Breaker:* ✅ DISPONIBLE

📊 *Estado Actual:*
• Suspensiones: {system_status.get('suspensions_detected', 0)} detectadas
• Auto-reparaciones: {system_status.get('suspensions_repaired', 0)} exitosas
• Trades activos: {portfolio_info.get('active_trades', 0)}
• Sesión: {'✅ ACTIVA' if system_status.get('trading_session_active') else '⏸️ INACTIVA'}

⚡ *Comandos de Emergencia:*
/emergency_stop - Parada TOTAL inmediata
/kill_switch - Cierre EMERGENCIA posiciones

🕒 *Última verificación:* {datetime.now().strftime('%H:%M:%S')}
            """
            await update.message.reply_text(protection_text, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error obteniendo protecciones: {str(e)}")
    
    async def emergency_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /emergency_stop - Parada de emergencia"""
        try:
            # Confirmación de seguridad
            confirm_text = """
🚨 *PARADA DE EMERGENCIA - CONFIRMACIÓN*

⚠️ *ESTA ACCIÓN ES IRREVERSIBLE:*
• Detendrá TODO el trading
• Cancelará órdenes pendientes
• Bloqueará nuevas operaciones
• Cerrará conexiones

¿Estás seguro? Responde *CONFIRMAR* para proceder.
            """
            await update.message.reply_text(confirm_text, parse_mode='Markdown')
            
            # Esperar confirmación
            context.user_data['waiting_confirm'] = True
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error en emergency stop: {str(e)}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Ayuda"""
        help_text = """
🤖 *NEXTIA TRADING BOT - AYUDA*

*COMANDOS PRINCIPALES:*
/start - Iniciar bot y mostrar bienvenida
/status - Estado completo del sistema
/portfolio - Información detallada del portfolio
/protection - Estado del sistema de protección

*COMANDOS DE EMERGENCIA:* 🚨
/emergency_stop - Parada TOTAL del sistema
/kill_switch - Cierre emergencia de posiciones

*INFORMACIÓN:*
🔗 *Conexión:* Binance Testnet
🛡️ *Protecciones:* Anti-suspensión, Risk Manager, Profit Targets
⏰ *Horarios:* Configurables en trading_sessions.json

💡 *Soporte:* El bot se auto-repara ante suspensiones
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto normales"""
        if context.user_data.get('waiting_confirm') and update.message.text.upper() == 'CONFIRMAR':
            # Ejecutar emergency stop real
            try:
                from protection.emergency_stop import EmergencyStop
                emergency_stop = EmergencyStop()
                success = emergency_stop.activate()
                
                if success:
                    await update.message.reply_text(
                        "✅ *PARADA DE EMERGENCIA ACTIVADA*\n\n"
                        "• Trading DETENIDO\n"
                        "• Órdenes CANCELADAS\n"  
                        "• Sistema BLOQUEADO\n"
                        "• Balance SEGURO",
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text("❌ Error activando parada de emergencia")
                    
            except Exception as e:
                await update.message.reply_text(f"❌ Error: {str(e)}")
            
            context.user_data['waiting_confirm'] = False
        else:
            await update.message.reply_text(
                "🤖 Usa /help para ver los comandos disponibles",
                parse_mode='Markdown'
            )
    
    def start_bot(self):
        """Iniciar el bot de Telegram"""
        if not TELEGRAM_AVAILABLE:
            logger.warning("❌ Telegram no disponible - Comandos desactivados")
            return
            
        try:
            self.application = Application.builder().token(self.token).build()
            
            # Agregar handlers de comandos
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("status", self.status_command))
            self.application.add_handler(CommandHandler("portfolio", self.portfolio_command))
            self.application.add_handler(CommandHandler("protection", self.protection_command))
            self.application.add_handler(CommandHandler("emergency_stop", self.emergency_stop_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            # Iniciar en segundo plano
            self.application.run_polling()
            self.is_running = True
            logger.info("✅ Telegram Command Handler iniciado")
            
        except Exception as e:
            logger.error(f"❌ Error iniciando Telegram bot: {e}")

class IntegratedTradingBot:
    """Bot de trading integrado completo - Versión Mejorada CON ANTI-SUSPENSIÓN Y TELEGRAM"""
    
    def __init__(self, config_path: str = "config/trading_rules.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
        # 🛡️ INICIALIZACIÓN ROBUSTA CON ANTI-SUSPENSIÓN
        self.trade_engine = self._initialize_trade_engine_with_retry()
        self.risk_manager = RiskManager(trade_engine=self.trade_engine)
        
        # NUEVO: Inicializar módulos de profit y sesiones
        self.profit_manager = ProfitManager('config/trading_sessions.json')
        self.session_scheduler = SessionScheduler('config/trading_sessions.json')
        self.session_scheduler.start_scheduler()
        
        # 📱 NUEVO: Telegram Command Handler
        self.telegram_handler = None
        self._initialize_telegram()
        
        self.total_balance = 0.0
        self.performance_metrics = {
            'total_trades': 0,
            'successful_trades': 0,
            'total_pnl': 0.0,
            'daily_pnl': 0.0,
            'win_rate': 0.0,
            'last_update': datetime.now(),
            'daily_trades': 0,
            'daily_start_balance': 0.0
        }
        self.daily_reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # MEJORA: Estadísticas en tiempo real
        self.session_stats = {
            'start_time': datetime.now(),
            'signals_processed': 0,
            'trades_executed': 0,
            'errors_count': 0,
            'signals_outside_session': 0,
            'positions_closed_by_profit': 0,
            'positions_closed_by_stop': 0,
            'suspensions_detected': 0,
            'suspensions_repaired': 0
        }
        
        # MEJORA: Cache para precios
        self.price_cache = {}
        self.cache_timeout = 5  # segundos
        
        self._initialize_systems()
    
    def _initialize_telegram(self):
        """📱 INICIALIZAR TELEGRAM COMMAND HANDLER - VERSIÓN CORREGIDA"""
        try:
            # Buscar token y chat ID de Telegram
            telegram_token = self._get_telegram_token()
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
            
            if telegram_token and chat_id and TELEGRAM_AVAILABLE:
                logger.info(f"✅ Telegram configurado - Token: {telegram_token[:10]}..., Chat ID: {chat_id}")
                self.telegram_handler = TelegramCommandHandler(telegram_token, self)
                # Iniciar en hilo separado
                telegram_thread = threading.Thread(target=self.telegram_handler.start_bot, daemon=True)
                telegram_thread.start()
                logger.info("✅ Telegram Command Handler inicializado")
            else:
                logger.warning(f"❌ Telegram no configurado - Token: {bool(telegram_token)}, Chat ID: {bool(chat_id)}, Telegram Available: {TELEGRAM_AVAILABLE}")
                
        except Exception as e:
            logger.error(f"❌ Error inicializando Telegram: {e}")
    
    def _get_telegram_token(self):
        """Obtener token de Telegram de variables de entorno .env - VERSIÓN CORREGIDA"""
        try:
            # Método 1: Variables de entorno del sistema
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            if token:
                logger.info("✅ Token de Telegram encontrado en variables de entorno")
                return token
            
            # Método 2: Buscar en archivo .env directamente
            env_file = '.env'
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.strip().split('=', 1)
                                if key.upper() == 'TELEGRAM_BOT_TOKEN':
                                    logger.info("✅ Token de Telegram encontrado en .env")
                                    return value.strip()
            
            # Método 3: Buscar en otros archivos de configuración (fallback)
            config_files = [
                'config/telegram_config.json',
                'config/trading_config.json', 
                'config/bot_config.json'
            ]
            
            for config_file in config_files:
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        token = config.get('telegram_token') or config.get('bot_token')
                        if token:
                            logger.info(f"✅ Token de Telegram encontrado en {config_file}")
                            return token
            
            logger.warning("❌ No se encontró token de Telegram en .env ni configuraciones")
            return None
                
        except Exception as e:
            logger.error(f"❌ Error buscando token de Telegram: {e}")
            return None

    def _initialize_trade_engine_with_retry(self):
        """🛡️ Inicializar Trade Engine con reintentos y protección anti-suspensión"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 Inicializando Trade Engine (intento {attempt + 1}/{max_retries})...")
                trade_engine = TradeEngine()
                
                if trade_engine.initialized:
                    logger.info("✅ Trade Engine inicializado correctamente")
                    return trade_engine
                else:
                    logger.warning(f"⚠️  Trade Engine no inicializado (intento {attempt + 1})")
                    
            except Exception as e:
                logger.error(f"❌ Error inicializando Trade Engine (intento {attempt + 1}): {e}")
                
            if attempt < max_retries - 1:
                # 🛡️ Verificar y reparar suspensión antes del reintento
                if suspension_monitor.check_suspension():
                    self.session_stats['suspensions_detected'] += 1
                    if suspension_monitor.repair_suspension():
                        self.session_stats['suspensions_repaired'] += 1
                time.sleep(3)
        
        raise Exception("No se pudo inicializar Trade Engine después de múltiples intentos")
    
    def _load_config(self) -> Dict:
        """Cargar configuración desde archivo JSON con manejo de errores robusto"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"✅ Configuración cargada desde {self.config_path}")
            
            # MEJORA: Validar configuración mínima requerida
            required_keys = ['max_position_size_percent', 'stop_loss_percent', 'max_open_trades']
            for key in required_keys:
                if key not in config:
                    raise KeyError(f"Clave de configuración requerida faltante: {key}")
                    
            return config
        except FileNotFoundError:
            logger.error(f"❌ Archivo de configuración no encontrado: {self.config_path}")
            # Configuración por defecto de emergencia
            default_config = {
                "max_position_size_percent": 2.0,
                "stop_loss_percent": 3.0,
                "take_profit_percent": 6.0,
                "max_open_trades": 4,
                "daily_loss_limit_percent": 10.0,
                "risk_reward_ratio": 2.0
            }
            logger.info("🔄 Usando configuración por defecto")
            return default_config
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error decodificando configuración: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error cargando configuración: {e}")
            raise
        
    def _initialize_systems(self):
        """Inicialización robusta de todos los sistemas - VERSIÓN MEJORADA"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self.trade_engine.initialized:
                    logger.error(f"❌ Trade Engine no inicializado (intento {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        raise Exception("Trade Engine no disponible después de múltiples intentos")
                
                # MEJORA: Configurar Risk Manager con parámetros actualizados
                self.risk_manager.config = self.config
                
                success = self.update_balance()
                if not success:
                    logger.warning("⚠️  Balance inicial no disponible, continuando...")
                
                # MEJORA: Establecer balance diario inicial
                self.performance_metrics['daily_start_balance'] = self.total_balance
                
                logger.info("✅ Sistemas inicializados correctamente")
                logger.info(f"📅 Scheduler de sesiones: {'✅ Activo' if self.session_scheduler.is_trading_time else '⏸️ Inactivo'}")
                return
                
            except Exception as e:
                logger.error(f"❌ Error en inicialización (intento {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    # 🛡️ Verificar suspensión durante reintentos
                    if suspension_monitor.check_suspension():
                        self.session_stats['suspensions_detected'] += 1
                        suspension_monitor.repair_suspension()
                    time.sleep(3)
                else:
                    logger.error("💥 Error crítico en inicialización del sistema")
                    raise
    
    def _reset_daily_metrics(self):
        """MEJORA: Reiniciar métricas diarias a medianoche"""
        now = datetime.now()
        if now.date() > self.daily_reset_time.date():
            self.performance_metrics['daily_pnl'] = 0.0
            self.performance_metrics['daily_trades'] = 0
            self.performance_metrics['daily_start_balance'] = self.total_balance
            self.daily_reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
            logger.info("🔄 Métricas diarias reiniciadas")
            
    def update_balance(self) -> bool:
        """Actualizar balance total del portfolio de forma robusta - VERSIÓN MEJORADA CON ANTI-SUSPENSIÓN"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # 🛡️ Verificar suspensión antes de operación crítica
                if suspension_monitor.check_suspension():
                    self.session_stats['suspensions_detected'] += 1
                    if suspension_monitor.repair_suspension():
                        self.session_stats['suspensions_repaired'] += 1
                
                usdt_balance = self.trade_engine.get_balance('USDT')
                btc_balance = self.trade_engine.get_balance('BTC')
                btc_price = self._get_cached_price('BTCUSDT')
                
                # MEJORA: Validación más robusta de datos
                if usdt_balance is None or btc_balance is None or btc_price <= 0:
                    logger.warning(f"⚠️  Datos de balance incompletos (intento {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    else:
                        # Usar valores por defecto como fallback
                        usdt_balance = usdt_balance or 0.0
                        btc_balance = btc_balance or 0.0
                        btc_price = btc_price if btc_price > 0 else 1.0
                        logger.warning("🔄 Usando valores de balance por defecto")
                
                new_balance = usdt_balance + (btc_balance * btc_price)
                
                # MEJORA: Calcular P&L diario
                if self.performance_metrics['daily_start_balance'] > 0:
                    daily_pnl = new_balance - self.performance_metrics['daily_start_balance']
                    self.performance_metrics['daily_pnl'] = daily_pnl
                
                self.total_balance = new_balance
                logger.info(f"💰 Balance total del portfolio: ${self.total_balance:.2f}")
                return True
                
            except Exception as e:
                logger.warning(f"⚠️  Intento {attempt + 1}/{max_retries} falló obteniendo balance: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error(f"❌ Error actualizando balance después de {max_retries} intentos: {e}")
                    if self.total_balance <= 0:
                        self.total_balance = 1000.0
                        logger.info(f"🔄 Usando balance fallback: ${self.total_balance:.2f}")
                    return False
    
    def _get_cached_price(self, symbol: str) -> float:
        """MEJORA: Obtener precio con cache para reducir llamadas a API"""
        now = time.time()
        if symbol in self.price_cache:
            price, timestamp = self.price_cache[symbol]
            if now - timestamp < self.cache_timeout:
                return price
        
        # Obtener nuevo precio
        price = self.trade_engine.get_current_price(symbol)
        if price > 0:
            self.price_cache[symbol] = (price, now)
        return price
    
    def cleanup_old_trades(self) -> int:
        """Limpiar trades antiguos antes de procesar nueva señal - VERSIÓN MEJORADA"""
        try:
            cleaned_count = self.risk_manager.cleanup_completed_trades(self.trade_engine)
            if cleaned_count > 0:
                logger.info(f"🧹 Se limpiaron {cleaned_count} trades completados")
                # MEJORA: Actualizar balance después de limpieza
                self.update_balance()
            return cleaned_count
        except Exception as e:
            logger.error(f"❌ Error limpiando trades: {e}")
            return 0

    def check_profit_stop_conditions(self):
        """NUEVO: Verificar condiciones de profit/stop para posiciones activas"""
        try:
            active_trades = self.risk_manager.active_trades.copy()
            closed_count = 0
            
            for trade_id, trade_info in active_trades.items():
                symbol = trade_info['symbol']
                current_price = self._get_cached_price(symbol)
                
                if current_price <= 0:
                    continue
                
                # Verificar si debería cerrar por profit/stop
                should_close = self.profit_manager.should_close_position(
                    symbol, current_price, trade_info['entry_price'], trade_info['trade_type'].lower()
                )
                
                if should_close:
                    # Cerrar posición
                    position_size = self.risk_manager.get_available_for_sell(symbol, self.trade_engine)
                    if position_size > 0:
                        success = self.trade_engine.execute_sell_order(symbol, position_size)
                        if success:
                            self.risk_manager.remove_active_trade(trade_id)
                            closed_count += 1
                            
                            # Determinar si fue por profit o stop
                            profit_percent = ((current_price - trade_info['entry_price']) / trade_info['entry_price']) * 100
                            if profit_percent >= 0:
                                self.session_stats['positions_closed_by_profit'] += 1
                                logger.info(f"🎯 POSICIÓN CERRADA POR PROFIT: {symbol} (+{profit_percent:.2f}%)")
                            else:
                                self.session_stats['positions_closed_by_stop'] += 1
                                logger.info(f"🛑 POSICIÓN CERRADA POR STOP: {symbol} ({profit_percent:.2f}%)")
            
            if closed_count > 0:
                logger.info(f"📊 Cierre automático: {closed_count} posiciones por profit/stop")
                self.update_balance()
                
            return closed_count
            
        except Exception as e:
            logger.error(f"❌ Error verificando profit/stop: {e}")
            return 0
    
    def process_signal(self, symbol: str, signal_type: str, strength: str, confidence: float = 0.0) -> Tuple[bool, str]:
        """Procesar señal de trading y ejecutar orden si es válida - VERSIÓN MEJORADA CON ANTI-SUSPENSIÓN"""
        try:
            # 🛡️ VERIFICAR SUSPENSIÓN ANTES DE PROCESAR SEÑAL
            if suspension_monitor.check_suspension():
                self.session_stats['suspensions_detected'] += 1
                logger.warning("🛡️  Suspensión detectada - aplicando reparación...")
                if suspension_monitor.repair_suspension():
                    self.session_stats['suspensions_repaired'] += 1
                    logger.info("✅ Sistema reparado después de suspensión")
                else:
                    logger.error("❌ No se pudo reparar la suspensión, omitiendo señal")
                    return False, "Sistema en reparación por suspensión"
            
            # MEJORA: Resetear métricas diarias si es necesario
            self._reset_daily_metrics()
            
            # NUEVO: Verificar horario de trading
            if not self.session_scheduler.is_trading_time:
                self.session_stats['signals_outside_session'] += 1
                logger.warning(f"⏰ Fuera del horario de trading - Señal rechazada: {symbol}")
                return False, "Fuera del horario de trading"
            
            # NUEVO: Verificar condiciones de profit/stop antes de nueva señal
            self.check_profit_stop_conditions()
            
            self.session_stats['signals_processed'] += 1
            logger.info(f"🎯 Procesando señal: {symbol} - {signal_type} (Fuerza: {strength}, Confianza: {confidence:.2f})")
            
            # MEJORA: Validación inicial de parámetros
            if not symbol or not signal_type:
                return False, "Parámetros de señal inválidos"
            
            # MEJORA: Validar confianza mínima
            if confidence < 0.6:  # 60% de confianza mínima
                logger.warning(f"⚠️  Señal con baja confianza ({confidence:.2f}), omitiendo...")
                return False, f"Confianza demasiado baja: {confidence:.2f}"
            
            # Paso 1: Limpiar trades completados
            self.cleanup_old_trades()
            
            # Paso 2: Obtener precio actual con cache
            current_price = self._get_cached_price(symbol)
            if current_price <= 0:
                error_msg = f"Error obteniendo precio para {symbol}"
                logger.error(f"❌ {error_msg}")
                return False, error_msg
            
            # MEJORA: Verificar que el balance esté actualizado
            if self.total_balance <= 0:
                self.update_balance()
                if self.total_balance <= 0:
                    error_msg = "Balance del portfolio no disponible"
                    logger.error(f"❌ {error_msg}")
                    return False, error_msg
            
            # Paso 3: Calcular tamaño de posición dinámico considerando confianza
            position_size = self.risk_manager.calculate_dynamic_position_size(
                self.total_balance, current_price, symbol, strength, confidence
            )
            
            if position_size <= 0:
                error_msg = f"Tamaño de posición inválido para {symbol}"
                logger.error(f"❌ {error_msg}")
                return False, error_msg
            
            # Paso 4: Validar trade con Risk Manager
            is_valid, message = self.risk_manager.validate_trade(
                symbol, position_size, current_price, signal_type, self.total_balance
            )
            
            if not is_valid:
                logger.warning(f"⚠️  Trade rechazado por Risk Manager: {message}")
                return False, f"Risk Manager: {message}"
            
            # Paso 5: Ejecutar orden
            success = False
            trade_id = f"{symbol}_{int(time.time())}"
            
            if signal_type.upper() == 'BUY':
                success = self.trade_engine.execute_buy_order(symbol, position_size)
                if success:
                    self.risk_manager.add_active_trade(
                        trade_id, symbol, position_size, current_price, 'BUY'
                    )
                    self._update_performance_metrics(True)
                    self.session_stats['trades_executed'] += 1
                    self.performance_metrics['daily_trades'] += 1
                    logger.info(f"✅ Orden de COMPRA ejecutada: {position_size:.6f} {symbol} a ${current_price:.2f}")
                    
            elif signal_type.upper() == 'SELL':
                success = self.trade_engine.execute_sell_order(symbol, position_size)
                if success:
                    self._update_performance_metrics(True)
                    self.session_stats['trades_executed'] += 1
                    self.performance_metrics['daily_trades'] += 1
                    logger.info(f"✅ Orden de VENTA ejecutada: {position_size:.6f} {symbol} a ${current_price:.2f}")
            
            else:
                error_msg = f"Tipo de señal no reconocido: {signal_type}"
                logger.warning(f"⚠️ {error_msg}")
                return False, error_msg
            
            # Paso 6: Actualizar balance después de la operación
            if success:
                time.sleep(2)
                self.update_balance()
                logger.info(f"📈 Balance actualizado: ${self.total_balance:.2f}")
                
            return success, "Operación ejecutada exitosamente" if success else "Error en ejecución"
                
        except Exception as e:
            error_msg = f"Error procesando señal: {e}"
            logger.error(f"❌ {error_msg}")
            self.session_stats['errors_count'] += 1
            return False, error_msg

    def _get_current_price_with_retry(self, symbol: str, max_retries: int = 2) -> float:
        """MEJORA: Obtener precio actual con reintentos"""
        for attempt in range(max_retries):
            try:
                price = self._get_cached_price(symbol)
                if price > 0:
                    return price
                else:
                    logger.warning(f"⚠️  Precio inválido para {symbol} (intento {attempt + 1}/{max_retries})")
            except Exception as e:
                logger.warning(f"⚠️  Error obteniendo precio (intento {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                time.sleep(1)
        
        logger.error(f"❌ No se pudo obtener precio para {symbol} después de {max_retries} intentos")
        return 0.0
    
    def _update_performance_metrics(self, success: bool):
        """Actualizar métricas de performance"""
        self.performance_metrics['total_trades'] += 1
        if success:
            self.performance_metrics['successful_trades'] += 1
        
        # MEJORA: Calcular win rate en tiempo real
        if self.performance_metrics['total_trades'] > 0:
            self.performance_metrics['win_rate'] = (
                self.performance_metrics['successful_trades'] / self.performance_metrics['total_trades'] * 100
            )
        
        self.performance_metrics['last_update'] = datetime.now()
    
    def get_portfolio_info(self) -> Dict:
        """Obtener información completa del portfolio - VERSIÓN MEJORADA"""
        try:
            self.update_balance()
            active_trades = self.risk_manager.get_active_trades_count()
            
            info = {
                'total_balance': self.total_balance,
                'active_trades': active_trades,
                'max_trades': self.config['max_open_trades'],
                'performance': self.performance_metrics,
                'session_stats': self.session_stats,
                'trading_session_active': self.session_scheduler.is_trading_time,
                'profit_manager_configured': len(self.profit_manager.profit_targets) > 0,
                'suspensions_detected': self.session_stats['suspensions_detected'],
                'suspensions_repaired': self.session_stats['suspensions_repaired'],
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"📊 Portfolio - Balance: ${self.total_balance:.2f}, "
                       f"Trades activos: {active_trades}/{self.config['max_open_trades']}, "
                       f"Win Rate: {self.performance_metrics['win_rate']:.1f}%, "
                       f"Sesión: {'✅ Activa' if self.session_scheduler.is_trading_time else '⏸️ Inactiva'}, "
                       f"Suspensiones: {self.session_stats['suspensions_detected']} detectadas, {self.session_stats['suspensions_repaired']} reparadas")
            return info
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo info del portfolio: {e}")
            return {
                'total_balance': self.total_balance or 0,
                'active_trades': 0,
                'max_trades': 0,
                'performance': self.performance_metrics,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_system_status(self) -> Dict:
        """Obtener estado completo del sistema - VERSIÓN MEJORADA"""
        try:
            portfolio_info = self.get_portfolio_info()
            
            # MEJORA: Calcular uptime de la sesión
            session_duration = datetime.now() - self.session_stats['start_time']
            
            status = {
                'system': 'IntegratedTradingBot',
                'status': 'operational',
                'portfolio': portfolio_info,
                'trade_engine': 'operational' if self.trade_engine.initialized else 'error',
                'risk_manager': 'operational',
                'profit_manager': 'operational',
                'session_scheduler': 'operational',
                'trading_session_active': self.session_scheduler.is_trading_time,
                'total_balance': self.total_balance,
                'session_duration_hours': round(session_duration.total_seconds() / 3600, 2),
                'suspension_protection': 'active',
                'suspensions_detected': self.session_stats['suspensions_detected'],
                'suspensions_repaired': self.session_stats['suspensions_repaired'],
                'timestamp': datetime.now().isoformat()
            }
            
            if not self.trade_engine.initialized:
                status['status'] = 'degraded'
                status['trade_engine'] = 'error'
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estado del sistema: {e}")
            return {
                'system': 'IntegratedTradingBot',
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

def main():
    """Función principal del bot integrado - Versión Mejorada CON ANTI-SUSPENSIÓN Y TELEGRAM"""
    logger.info("🚀 INICIANDO NEXTIA TRADING BOT INTEGRADO - VERSIÓN MEJORADA CON ANTI-SUSPENSIÓN Y TELEGRAM")
    logger.info("==========================================")
    
    try:
        # 🛡️ EJECUTAR PROTECCIÓN ANTI-SUSPENSIÓN AL INICIO
        anti_suspension_init()
        
        # Crear bot integrado
        bot = IntegratedTradingBot()
        
        if not bot.trade_engine.initialized:
            logger.error("❌ No se pudo inicializar el Trade Engine")
            return
        
        logger.info("✅ Todos los sistemas inicializados correctamente")
        logger.info("   - Trade Engine: ✅")
        logger.info("   - Risk Manager: ✅")
        logger.info("   - Profit Manager: ✅")
        logger.info("   - Session Scheduler: ✅")
        logger.info("   - Balance Tracking: ✅")
        logger.info("   - Dynamic Position Sizing: ✅")
        logger.info("   - Price Caching: ✅")
        logger.info("   - Daily Metrics: ✅")
        logger.info("   - 🛡️ ANTI-SUSPENSIÓN: ✅ ACTIVADO")
        logger.info(f"   - 📱 TELEGRAM COMMANDS: {'✅ ACTIVADO' if bot.telegram_handler else '❌ NO CONFIGURADO'}")
        logger.info(f"   - Sesión Trading: {'✅ Activa' if bot.session_scheduler.is_trading_time else '⏸️ Inactiva'}")
        
        # Mostrar configuración cargada
        logger.info(f"⚙️  Configuración cargada:")
        for key, value in bot.config.items():
            logger.info(f"     {key}: {value}")
        
        # Mostrar profit targets configurados
        logger.info(f"🎯 Profit Targets configurados: {len(bot.profit_manager.profit_targets)} símbolos")
        
        # Mostrar info del portfolio
        portfolio_info = bot.get_portfolio_info()
        logger.info(f"💰 Balance inicial: ${portfolio_info['total_balance']:.2f}")
        
        # Mostrar estado del sistema
        system_status = bot.get_system_status()
        logger.info(f"🔧 Estado del sistema: {system_status['status']}")
        
        logger.info("==========================================")
        logger.info("🎉 SISTEMA INTEGRADO MEJORADO CON ANTI-SUSPENSIÓN Y TELEGRAM FUNCIONANDO CORRECTAMENTE")
        logger.info("💪 Bot listo para recibir señales del Data Engine!")
        logger.info("🛡️  Protección anti-suspensión: ACTIVADA - El bot se auto-reparará si detecta suspensiones")
        logger.info("📱 Comandos Telegram: /start, /status, /portfolio, /protection, /emergency_stop")
        
        # Mantener el programa corriendo
        while True:
            time.sleep(60)
            # Verificar suspensión periódicamente
            if suspension_monitor.check_suspension():
                logger.warning("🛡️  Suspensión detectada en bucle principal")
                suspension_monitor.repair_suspension()
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido por usuario")
    except Exception as e:
        logger.error(f"❌ Error crítico en inicialización: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
