#!/usr/bin/env python3
"""
Verificador de tiempo para Trading Bot
"""

import datetime
import pytz
import os

def check_trading_time():
    """Verificar si estamos en horario de trading"""
    
    # Zonas horarias
    ny_tz = pytz.timezone('America/New_York')
    utc_tz = pytz.timezone('UTC')
    local_tz = pytz.timezone('America/Mexico_City')  # Ajusta según tu zona
    
    # Tiempos actuales
    ny_time = datetime.datetime.now(ny_tz)
    utc_time = datetime.datetime.now(utc_tz)
    local_time = datetime.datetime.now(local_tz)
    
    print("🕒 VERIFICACIÓN DE TIEMPO PARA TRADING")
    print("=" * 50)
    print(f"📍 Hora Local:    {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌎 Hora New York: {ny_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⚡ Hora UTC:      {utc_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 Día de semana: {ny_time.strftime('%A')}")
    
    # Verificar horario de trading (9:00 AM - 5:00 PM NY)
    trading_start = ny_time.replace(hour=9, minute=0, second=0, microsecond=0)
    trading_end = ny_time.replace(hour=17, minute=0, second=0, microsecond=0)
    
    is_trading_hours = trading_start <= ny_time <= trading_end
    is_weekday = ny_time.weekday() < 5  # 0-4 = Lunes-Viernes
    
    print(f"📈 Horario Trading: {'✅ ACTIVO' if is_trading_hours else '❌ INACTIVO'}")
    print(f"📅 Día hábil: {'✅ SÍ' if is_weekday else '❌ NO'}")
    print(f"🎯 Trading Permitido: {'✅ SÍ' if (is_trading_hours and is_weekday) else '❌ NO'}")
    
    # Tiempo hasta próxima sesión
    if not is_trading_hours:
        if ny_time < trading_start:
            next_session = trading_start
        else:
            # Próximo día hábil
            days_ahead = 1
            next_day = ny_time + datetime.timedelta(days=days_ahead)
            while next_day.weekday() >= 5:  # Saltar fines de semana
                days_ahead += 1
                next_day = ny_time + datetime.timedelta(days=days_ahead)
            next_session = next_day.replace(hour=9, minute=0, second=0, microsecond=0)
        
        time_until = next_session - ny_time
        hours_until = time_until.total_seconds() / 3600
        print(f"⏰ Próxima sesión en: {hours_until:.1f} horas")
    
    return is_trading_hours and is_weekday

def check_binance_time_sync():
    """Verificar sincronización con Binance"""
    try:
        from binance.client import Client
        from dotenv import load_dotenv
        
        load_dotenv()
        
        client = Client(
            os.getenv('BINANCE_TESTNET_API_KEY'),
            os.getenv('BINANCE_TESTNET_SECRET_KEY'),
            testnet=True
        )
        
        server_time = client.get_server_time()
        binance_time = datetime.datetime.fromtimestamp(server_time['serverTime'] / 1000, pytz.UTC)
        local_time = datetime.datetime.now(pytz.UTC)
        
        time_diff = (local_time - binance_time).total_seconds() * 1000  # ms
        
        print("\n🔗 SINCRONIZACIÓN BINANCE:")
        print(f"⏰ Hora Binance: {binance_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"⏰ Hora Local:   {local_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"📏 Diferencia:   {time_diff:.0f} ms")
        
        if abs(time_diff) < 5000:  # 5 segundos de tolerancia
            print("✅ Sincronización: ÓPTIMA")
        else:
            print("⚠️  Sincronización: REQUIERE AJUSTE")
            
    except Exception as e:
        print(f"❌ Error verificando Binance: {e}")

if __name__ == "__main__":
    print("🚀 INICIANDO VERIFICACIÓN DE TIEMPO...")
    print()
    
    # Verificar horario trading
    can_trade = check_trading_time()
    
    print()
    
    # Verificar sincronización Binance
    check_binance_time_sync()
    
    print("\n" + "=" * 50)
    
    if can_trade:
        print("🎯 ESTADO: ✅ LISTO PARA TRADING")
        print("💡 Ejecuta: python main.py")
    else:
        print("🎯 ESTADO: ⏸️  FUERA DE HORARIO")
        print("💡 Espera hasta 9:00 AM NY (Lunes-Viernes)")
