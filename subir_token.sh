#!/bin/bash

# Ir directamente al directorio de trabajo REAL
cd /home/jorgesensei33/proyectos/nextia/trading/token

echo "🚀 Subiendo cambios al repo NextiaToken..."

# Forzar el remote correcto
git remote set-url origin https://github.com/NextiaSensei/NextiaToken.git

# Proceso normal de subida
git add .
git commit -m "$1"
git push origin main

echo "✅ ¡Cambios subidos a NextiaToken!"
