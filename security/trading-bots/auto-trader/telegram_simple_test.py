#!/usr/bin/env python3
"""
PRUEBA SUPER SIMPLE DE TELEGRAM - SÍ FUNCIONA
"""

import logging
import os
from telegram import Bot
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='🔔 %(asctime)s - TELEGRAM SIMPLE - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

async def start_command(update, context):
    await update.message.reply_text(
        "🤖 *BOT SIMPLE ACTIVO*\n\n"
        "✅ ¡Telegram funcionando correctamente!\n"
        "🎯 Este es un test mínimo",
        parse_mode='Markdown'
    )

async def status_command(update, context):
    await update.message.reply_text(
        "📊 *ESTADO SIMPLE*\n\n"
        "💼 Balance: $50,000\n"
        "📈 Trades: 25\n"
        "🎯 Win Rate: 85%\n\n"
        "✅ Todo funciona perfecto!",
        parse_mode='Markdown'
    )

def main():
    logger.info("🚀 INICIANDO PRUEBA SIMPLE DE TELEGRAM")
    
    if not TOKEN:
        logger.error("❌ No hay TOKEN")
        return
    
    logger.info(f"✅ Token encontrado: {TOKEN[:10]}...")
    
    try:
        # Crear aplicación de manera SIMPLE
        app = Application.builder().token(TOKEN).build()
        
        # Agregar comandos
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("status", status_command))
        app.add_handler(CommandHandler("test", start_command))
        
        logger.info("🔄 Iniciando bot...")
        
        # Enviar mensaje de que está vivo
        bot = Bot(TOKEN)
        bot.send_message(
            chat_id=CHAT_ID, 
            text="🔔 *BOT SIMPLE INICIADO*\n\nEscribe /start o /status", 
            parse_mode='Markdown'
        )
        
        logger.info("✅ Bot iniciado - ESCUCHANDO COMANDOS")
        
        # Iniciar polling
        app.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
