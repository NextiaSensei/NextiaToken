import requests
import os
from dotenv import load_dotenv

print("🔍 Buscando tu Chat ID de Telegram...")
print("=" * 50)

# Cargar variables del .env
load_dotenv()

# Obtener el token
token = os.getenv('TELEGRAM_BOT_TOKEN')
if not token:
    print("❌ ERROR: No encontré TELEGRAM_BOT_TOKEN en .env")
    print("💡 Asegúrate de que guardaste tu token en el archivo .env")
    exit(1)

print(f"✅ Token encontrado: {token[:10]}...")

# Hacer petición a Telegram API
url = f'https://api.telegram.org/bot{token}/getUpdates'
print("📡 Consultando mensajes recientes...")

try:
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if data['ok'] and data['result']:
        # Tomar el mensaje más reciente
        latest_message = data['result'][-1]
        chat_id = latest_message['message']['chat']['id']
        user_name = latest_message['message']['chat']['first_name']
        
        print("")
        print("🎉 ¡CHAT ID ENCONTRADO!")
        print("=" * 30)
        print(f"👤 Usuario: {user_name}")
        print(f"🆔 Chat ID: {chat_id}")
        print("")
        print("📝 COPIAR ESTO A TU .env:")
        print(f"TELEGRAM_CHAT_ID={chat_id}")
        print("")
        print("💡 Ejecuta: nano .env y pega esa línea")
        
    else:
        print("")
        print("❌ No hay mensajes recientes")
        print("💡 Envía un mensaje a @NextiaTradingBot y vuelve a ejecutar este script")
        print("   Mensaje sugerido: \"/start\"")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔧 Verifica tu conexión a internet")
