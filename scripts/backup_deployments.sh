#!/bin/bash
set -e
TS=$(date +%F_%H%M%S)
OUT="backups/nextia_backup_$TS"
mkdir -p "$OUT"

# Copiamos lo crítico
cp -r deployments "$OUT/" 2>/dev/null || true
cp -r artifacts "$OUT/" 2>/dev/null || true
cp package.json "$OUT/" 2>/dev/null || true
cp README.md "$OUT/" 2>/dev/null || true
cp -r docs "$OUT/" 2>/dev/null || true

# Archivamos
tar -czvf "${OUT}.tar.gz" -C backups "nextia_backup_$TS"

# Ciframos con GPG (interactivo: te pedirá passphrase)
gpg -c --cipher-algo AES256 "${OUT}.tar.gz"

# Limpieza opcional: borrar la carpeta sin comprimir
rm -rf "$OUT"
echo "Backup creado y cifrado: ${OUT}.tar.gz.gpg"
