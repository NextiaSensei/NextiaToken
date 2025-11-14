#!/usr/bin/env python3
"""
Script para detectar cambios de IP y notificar
"""
import requests
import os
from datetime import datetime

def get_current_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=10)
        return response.text.strip()
    except:
        return None

def main():
    current_ip = get_current_ip()
    if current_ip:
        print(f"🌐 TU IP ACTUAL: {current_ip}")
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n⚠️  RECUERDA:")
        print("1. Ve a Binance API Management")
        print("2. Actualiza la IP en 'Restricciones de acceso por IP'")
        print("3. Espera 10-15 minutos")
    else:
        print("❌ No se pudo obtener la IP")

if __name__ == "__main__":
    main()
