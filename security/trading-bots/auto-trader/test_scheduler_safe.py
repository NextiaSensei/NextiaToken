from session_scheduler import SessionScheduler
from datetime import datetime
import time

print("🧪 TEST SEGURO - Session Scheduler")
print("====================================")

# 1. Verificar hora actual del sistema
hora_actual = datetime.now()
print(f"📍 Hora actual del sistema: {hora_actual.strftime('%Y-%m-%d %H:%M:%S')}")

# 2. Crear scheduler
scheduler = SessionScheduler()

# 3. Verificar estado actual
estado_actual = scheduler.is_session_active()
print(f"📊 Estado de sesión: {'🟢 ACTIVA' if estado_actual else '🔴 INACTIVA'}")

# 4. Información de próxima sesión
proxima_sesion, tiempo_restante = scheduler.get_next_session_info()
if proxima_sesion:
    print(f"⏭️  Próxima sesión: {proxima_sesion.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Tiempo restante: {scheduler._format_timedelta(tiempo_restante)}")
else:
    print("❌ No hay sesiones programadas")

# 5. Simular algunas verificaciones (SOLO LECTURA)
print("\n🔍 Simulando 3 ciclos de verificación:")
for i in range(3):
    puede_trade, espera = scheduler.should_trade()
    estado = "🟢 TRADING" if puede_trade else "🔴 ESPERA"
    print(f"   Ciclo {i+1}: {estado} | Sleep: {espera}s")
    time.sleep(1)

print("\n✅ Test completado - Horario del sistema INTACTO")
print("💡 El scheduler está listo para usar en el bot real")
