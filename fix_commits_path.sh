#!/bin/bash
echo "🔧 Reconfigurando commits para nextia/trading/token"

# Ir al repositorio principal
cd ~/proyectos/nextia/

echo "📋 Estructura actual:"
ls -la trading/token/

echo "🔄 Agregando solo la carpeta token..."
git add trading/token/

echo "💾 Creando commit..."
git commit -m "NextiaToken: Actualización completa de contratos, tests y scripts"

echo "📤 Subiendo cambios..."
git push origin main

echo "✅ ¡Commis ahora van a nextia/trading/token!"
echo "🌐 Verifica en: https://github.com/NextiaSensei/nextia/tree/main/trading/token"
