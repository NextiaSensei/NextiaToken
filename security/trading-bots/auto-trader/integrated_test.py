#!/usr/bin/env python3
"""
Nextia Trading Bot - VERSIÓN TESTING CON TELEGRAM ULTRA SIMPLE
"""

import logging
import time
import os
import random
import requests
import threading
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables PERO FORZAR MODO TESTING
load_dotenv()

# 🔒 FORZAR MODO TESTING - EVITA TRADES REALES
os.environ['TEST_MODE'] = 'True'
os.environ['SIMULATION_MODE'] = 'True'

logging.basicConfig(
    level=logging.INFO,
    format='🧪 %(asctime)s - TESTING - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class UltraSimpleTelegramBot:
    """Bot de Telegram ULTRA SIMPLE - SOLO TESTING"""
    
    def __init__(self):
        # 🔒 USAR TOKEN DE TESTING ESPECÍFICO
        self.token = os.getenv('TELEGRAM_TEST_TOKEN')  # CAMBIADO
        self.chat_id = os.getenv('TELEGRAM_TEST_CHAT_ID')  # CAMBIADO
        
        # 🔒 VERIFICACIÓN DE SEGURIDAD
        if not self.token or not self.chat_id:
            logger.error("🚨 CRÍTICO: No hay configuración de Telegram TESTING!")
            logger.error("🚨 Usando variables: TELEGRAM_TEST_TOKEN y TELEGRAM_TEST_CHAT_ID")
            raise Exception("Configuración de testing no encontrada")
            
        if os.getenv('TELEGRAM_BOT_TOKEN') == self.token:
            logger.warning("⚠️ ADVERTENCIA: Token de testing igual al token principal")
            
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = 0
        self.running = True
        
        # Métricas del bot - SOLO SIMULACIÓN
        self.performance_metrics = {
            'total_trades': 0, 
            'successful_trades': 0, 
            'win_rate': 0.0, 
            'daily_trades': 0
        }
        self.session_stats = {'start_time': datetime.now(), 'trades_executed': 0}
        
        # 🔒 INICIALIZAR SOLO TELEGRAM, SIN CONEXIÓN A EXCHANGES
        if self.token and self.chat_id:
            self.telegram_thread = threading.Thread(target=self.run_polling)
            self.telegram_thread.daemon = True
            self.telegram_thread.start()
            logger.info("✅ Telegram TESTING iniciado - Token específico para testing")
            logger.info(f"✅ Chat ID de testing: {self.chat_id}")
        else:
            logger.warning("❌ No hay configuración de Telegram TESTING")
    
    def send_message(self, text):
        """Enviar mensaje a Telegram TESTING"""
        # 🔒 AGREGAR INDICADOR DE TESTING EN TODOS LOS MENSAJES
        if not text.startswith("🧪"):
            text = f"🧪 {text}"
            
        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        try:
            response = requests.post(url, data=data, timeout=10)
            if response.json().get('ok', False):
                logger.info(f"📤 Mensaje enviado a chat TESTING: {text[:50]}...")
            return response.json().get('ok', False)
        except Exception as e:
            logger.error(f"❌ Error enviando mensaje a testing: {e}")
            return False
    
    def get_updates(self):
        """Obtener mensajes de Telegram TESTING"""
        url = f"{self.base_url}/getUpdates"
        params = {
            'offset': self.last_update_id + 1,
            'timeout': 10
        }
        try:
            response = requests.get(url, params=params, timeout=15)
            data = response.json()
            if data.get('ok'):
                return data.get('result', [])
        except Exception as e:
            logger.debug(f"⚠️ Error obteniendo updates testing: {e}")
        return []
    
    def process_command(self, message):
        """Procesar comandos de Telegram TESTING"""
        text = message.get('text', '').lower()
        user_name = message.get('from', {}).get('first_name', 'Usuario')
        
        logger.info(f"📨 Comando recibido en TESTING: {text} de {user_name}")
        
        if text == '/start':
            self.send_message(
                f"🤖 <b>NEXTIA TRADING BOT - TESTING PURA SIMULACIÓN</b>\n\n"
                f"👋 Hola <b>{user_name}</b>!\n\n"
                "🔒 <b>MODO TESTING BLOQUEADO</b>\n"
                "✅ No se ejecutarán órdenes reales\n"
                "💵 Balance virtual: $50,000\n"
                "📊 Chat: <b>TESTING SEPARADO</b>\n\n"
                "🧪 <b>SOLO SIMULACIÓN - SIN RIESGO</b>\n\n"
                "<b>Comandos disponibles:</b>\n"
                "/start - Este mensaje\n"
                "/status - Estado del sistema\n"
                "/portfolio - Portfolio virtual\n"
                "/test_signal - Generar señal de prueba\n"
                "/help - Ayuda"
            )
        
        elif text == '/status':
            status_text = f"""
📊 <b>ESTADO DEL SISTEMA TESTING</b>

👤 <b>Usuario:</b> {user_name}
🔒 <b>MODO:</b> TESTING PURA SIMULACIÓN
✅ <b>Seguridad:</b> BLOQUEADO A TRADES REALES
📱 <b>Chat:</b> TESTING SEPARADO

💼 <b>Balance Virtual:</b> $50,000.00
📈 <b>Trades Ejecutados:</b> {self.session_stats['trades_executed']}
🎯 <b>Win Rate:</b> {self.performance_metrics['win_rate']:.1f}%
🔄 <b>Trades Totales:</b> {self.performance_metrics['total_trades']}

🕒 <b>Actualizado:</b> {datetime.now().strftime('%H:%M:%S')}
            """
            self.send_message(status_text)
        
        elif text == '/portfolio':
            portfolio_text = f"""
💼 <b>PORTFOLIO VIRTUAL - TESTING</b>

👤 <b>Usuario:</b> {user_name}
🔒 <b>MODO SEGURO ACTIVADO</b>
📱 <b>Chat:</b> TESTING SEPARADO

💰 <b>Balance Total:</b> $50,000.00
📊 <b>Trades Activos:</b> 0/5
🎯 <b>Win Rate:</b> {self.performance_metrics['win_rate']:.1f}%

📈 <b>Rendimiento Simulado:</b>
• BTCUSDT: +$1,200.50
• ETHUSDT: +$850.25  
• ADAUSDT: +$320.75
• DOTUSDT: +$180.30
• LINKUSDT: +$210.45

✅ <b>Sistema en modo testing seguro</b>
            """
            self.send_message(portfolio_text)
        
        elif text == '/test_signal':
            # Generar señal de prueba - SOLO SIMULACIÓN
            symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT']
            symbol = random.choice(symbols)
            signal_type = random.choice(['BUY', 'SELL'])
            confidence = random.randint(70, 95)
            
            self.session_stats['trades_executed'] += 1
            self.performance_metrics['total_trades'] += 1
            self.performance_metrics['successful_trades'] += 1
            
            if self.performance_metrics['total_trades'] > 0:
                self.performance_metrics['win_rate'] = (
                    self.performance_metrics['successful_trades'] / 
                    self.performance_metrics['total_trades'] * 100
                )
            
            signal_text = f"""
🎯 <b>SEÑAL DE PRUEBA - SIMULACIÓN</b>

👤 <b>Usuario:</b> {user_name}
🔒 <b>MODO TESTING - SIN RIESGO</b>
📱 <b>Chat:</b> TESTING SEPARADO

📊 <b>Símbolo:</b> {symbol}
🔄 <b>Tipo:</b> {signal_type}
✅ <b>Resultado:</b> SIMULADO EXITOSO
📈 <b>Confianza:</b> {confidence}%

🧪 <b>Orden bloqueada - Solo simulación</b>
            """
            self.send_message(signal_text)
            logger.info(f"🧪 Señal de prueba generada para {user_name}: {symbol} {signal_type}")
        
        elif text == '/help':
            help_text = f"""
🤖 <b>BOT DE TESTING - AYUDA</b>

👤 <b>Usuario:</b> {user_name}
🔒 <b>MODO SEGURO ACTIVADO</b>
📱 <b>Chat:</b> TESTING SEPARADO
✅ No se ejecutarán órdenes reales

<b>Comandos disponibles:</b>
/start - Iniciar bot y mostrar ayuda
/status - Estado completo del sistema  
/portfolio - Información del portfolio virtual
/test_signal - Generar señal de prueba manual
/help - Mostrar este mensaje

🧪 <b>Características:</b>
• Opera 24/7 sin restricciones
• Balance virtual $50,000
• Órdenes simuladas
• Perfecto para desarrollo
• 🔒 Bloqueado a trades reales
• 📱 Chat separado del bot principal
            """
            self.send_message(help_text)
        else:
            self.send_message(f"❓ Comando no reconocido: <b>{text}</b>\n\nEscribe /help para ver comandos disponibles")
    
    def run_polling(self):
        """Bucle principal para escuchar Telegram TESTING"""
        logger.info("📱 Telegram TESTING - Escuchando comandos...")
        logger.info(f"📱 Chat ID de testing: {self.chat_id}")
        
        # Mensaje de inicio CON INDICADOR DE TESTING
        self.send_message(
            "🔔 <b>BOT DE TESTING INICIADO</b>\n\n"
            "🔒 <b>MODO SEGURO ACTIVADO</b>\n"
            "📱 <b>Chat:</b> TESTING SEPARADO\n\n"
            "Escribe /start para comenzar"
        )
        
        while self.running:
            try:
                updates = self.get_updates()
                for update in updates:
                    self.last_update_id = update['update_id']
                    if 'message' in update:
                        self.process_command(update['message'])
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Error en polling testing: {e}")
                time.sleep(5)
    
    def generate_auto_signal(self):
        """Generar señal automática para testing - SOLO SIMULACIÓN"""
        symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT']
        symbol = random.choice(symbols)
        signal_type = random.choice(['BUY', 'SELL'])
        strength = random.choice(['LOW', 'MEDIUM', 'HIGH', 'STRONG'])
        confidence = round(random.uniform(0.6, 0.95), 2)
        
        self.session_stats['trades_executed'] += 1
        self.performance_metrics['total_trades'] += 1
        self.performance_metrics['successful_trades'] += 1
        self.performance_metrics['daily_trades'] += 1
        
        if self.performance_metrics['total_trades'] > 0:
            self.performance_metrics['win_rate'] = (
                self.performance_metrics['successful_trades'] / 
                self.performance_metrics['total_trades'] * 100
            )
        
        logger.info(f"🧪 SEÑAL SIMULADA: {symbol} {signal_type} (Conf: {confidence})")
        
        # También enviar señal automática a Telegram TESTING
        signal_text = f"""
🤖 <b>SEÑAL AUTOMÁTICA TESTING</b>

📊 <b>Símbolo:</b> {symbol}
🔄 <b>Tipo:</b> {signal_type}  
✅ <b>Resultado:</b> SIMULADO EXITOSO
📈 <b>Confianza:</b> {confidence}%
💪 <b>Fuerza:</b> {strength}

🧪 <b>Señal automática - Solo simulación</b>
"""
        self.send_message(signal_text)
        
        return True, "🧪 ORDEN SIMULADA EXITOSA - MODO TESTING"

def main():
    logger.info("🚀 BOT TESTING INICIADO - TELEGRAM SEPARADO")
    logger.info("🔒 MODO SEGURO ACTIVADO - SIN TRADES REALES")
    logger.info("📱 Usando chat de TESTING separado")
    
    try:
        bot = UltraSimpleTelegramBot()
        test_count = 0
        
        while True:
            # Generar señales automáticas cada 2 minutos
            if test_count % 4 == 0:
                result = bot.generate_auto_signal()
                logger.info(f"🧪 Señal auto: {result[1]}")
            
            # Mostrar estado cada 10 ciclos
            if test_count % 10 == 0:
                logger.info(f"📊 Testing: {bot.performance_metrics['total_trades']} trades simulados, WR: {bot.performance_metrics['win_rate']:.1f}%")
            
            test_count += 1
            time.sleep(30)
            
    except KeyboardInterrupt:
        logger.info("🛑 Bot testing detenido")
    except Exception as e:
        logger.error(f"🚨 Error crítico: {e}")

if __name__ == "__main__":
    main()
