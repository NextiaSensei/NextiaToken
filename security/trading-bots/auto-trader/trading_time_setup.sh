#!/bin/bash
# trading_time_setup.sh

echo "🕐 Configurando hora para trading bot..."

# 1. Establecer zona New York
sudo timedatectl set-timezone America/New_York

# 2. Activar sincronización NTP
sudo timedatectl set-ntp true

# 3. Verificar configuración
echo "✅ Hora configurada:"
date
echo ""

# 4. Mostrar información completa
timedatectl status

# 5. Verificar sincronización
echo "🔍 Verificando sincronización NTP:"
timedatectl show | grep -i ntp
