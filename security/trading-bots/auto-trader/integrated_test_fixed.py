#!/usr/bin/env python3
"""
Nextia Trading Bot - VERSIÓN CORREGIDA CON TELEGRAM
"""

import logging
import time
import os
import random
import threading
from datetime import datetime
from dotenv import load_dotenv

# Cargar .env PRIMERO
load_dotenv()

try:
    from telegram import Bot
    from telegram.ext import Application, CommandHandler
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='🧪 %(asctime)s - TESTING - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class SimpleTelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.trades_count = 0
        self.bot_running = False
        
        if TELEGRAM_AVAILABLE and self.token:
            self.start_telegram()
        else:
            logger.warning("❌ Telegram no disponible")

    def start_telegram(self):
        """Iniciar bot de Telegram de manera SIMPLE"""
        try:
            self.app = Application.builder().token(self.token).build()
            
            # Comandos básicos que SÍ funcionan
            self.app.add_handler(CommandHandler("start", self.telegram_start))
            self.app.add_handler(CommandHandler("status", self.telegram_status))
            self.app.add_handler(CommandHandler("portfolio", self.telegram_portfolio))
            self.app.add_handler(CommandHandler("test_signal", self.telegram_test_signal))
            
            # Iniciar en hilo separado
            self.telegram_thread = threading.Thread(target=self.app.run_polling)
            self.telegram_thread.daemon = True
            self.telegram_thread.start()
            
            self.bot_running = True
            logger.info("✅ Telegram Bot iniciado CORRECTAMENTE")
            
            # Enviar mensaje de inicio
            bot = Bot(self.token)
            bot.send_message(
                chat_id=self.chat_id,
                text="🤖 *BOT TESTING INICIADO*\n\nEscribe /start para comenzar",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"❌ Error iniciando Telegram: {e}")

    async def telegram_start(self, update, context):
        await update.message.reply_text(
            "🤖 *BOT TESTING ACTIVO - VERSIÓN CORREGIDA*\n\n"
            "✅ Telegram funcionando\n"
            "🧪 Modo testing 24/7\n"
            "💵 Balance virtual: $50,000\n\n"
            "*Comandos:*\n"
            "/status - Estado del sistema\n"
            "/portfolio - Portfolio virtual\n"
            "/test_signal - Generar señal\n",
            parse_mode='Markdown'
        )

    async def telegram_status(self, update, context):
        status_text = f"""
📊 *ESTADO DEL SISTEMA*

💼 Balance: $50,000.00
📈 Trades ejecutados: {self.trades_count}
🎯 Win Rate: 95.0%
🔄 Señales: {random.randint(10, 50)}

🧪 Modo: TESTING 24/7
✅ Telegram: FUNCIONANDO

🕒 Hora: {datetime.now().strftime('%H:%M:%S')}
        """
        await update.message.reply_text(status_text, parse_mode='Markdown')

    async def telegram_portfolio(self, update, context):
        portfolio_text = """
💼 *PORTFOLIO VIRTUAL*

💰 Balance Total: $50,000.00
📊 Trades Activos: 2/5
🎯 Win Rate: 95.0%

📈 Rendimiento:
• BTCUSDT: +$1,250.50
• ETHUSDT: +$890.25  
• ADAUSDT: +$156.75

✅ Sistema estable
        """
        await update.message.reply_text(portfolio_text, parse_mode='Markdown')

    async def telegram_test_signal(self, update, context):
        symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT']
        symbol = random.choice(symbols)
        signal_type = random.choice(['BUY', 'SELL'])
        
        self.trades_count += 1
        
        signal_text = f"""
🎯 *SEÑAL DE PRUEBA GENERADA*

📊 Símbolo: {symbol}
🔄 Tipo: {signal_type}
✅ Éxito: SIMULADO
📈 Confianza: {random.randint(70, 95)}%

🧪 Modo testing activo
        """
        await update.message.reply_text(signal_text, parse_mode='Markdown')

    def run(self):
        """Bucle principal"""
        logger.info("🚀 BOT TESTING INICIADO - TELEGRAM CORREGIDO")
        
        try:
            while True:
                # Simular actividad cada 30 segundos
                time.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("🛑 Bot detenido")

if __name__ == "__main__":
    bot = SimpleTelegramBot()
    bot.run()
