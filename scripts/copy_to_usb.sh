#!/bin/bash
# Copia el último backup al USB y verifica integridad

USB_PATH="/media/jorgesensei33/NUEVO VOL"
LATEST_BACKUP=$(ls -t backups/nextia_backup_*.tar.gz.gpg | head -n 1)

if [ ! -d "$USB_PATH" ]; then
  echo "⚠️  USB no montado en $USB_PATH"
  exit 1
fi

echo "📂 Copiando $LATEST_BACKUP al USB..."
cp "$LATEST_BACKUP" "$USB_PATH/"

echo "🔐 Verificando integridad..."
sha256sum "$LATEST_BACKUP" > backups/last_usb.sha256
cd "$USB_PATH"
sha256sum -c /home/jorgesensei33/proyectos/nextia/trading/token/backups/last_usb.sha256
