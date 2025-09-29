#!/bin/bash
# Script para flatten + slither, dentro o fuera de venv
# Uso: ./analyze_auto.sh

CONTRACT="contracts/NextiaToken.sol"
FLAT_DIR="flat"
RESULTS_DIR="results"
FLAT_FILE="$FLAT_DIR/NextiaToken_flat.sol"
FLAT_CLEAN="$FLAT_DIR/NextiaToken_flat_clean.sol"

# Crear carpetas si no existen
mkdir -p $FLAT_DIR $RESULTS_DIR

# Detectar si estamos en un venv de Python
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚡ No venv detectado, buscando slither y hardhat globales..."
    SLITHER_CMD=$(which slither)
    HARDHAT_CMD=$(which npx)
else
    echo "⚡ venv detectado, usando slither y hardhat del entorno..."
    SLITHER_CMD="$VIRTUAL_ENV/bin/slither"
    HARDHAT_CMD="npx"
fi

# Comprobar si los comandos existen
if [[ -z "$SLITHER_CMD" ]]; then
    echo "❌ Slither no encontrado. Instala con: pip install slither-analyzer --user"
    exit 1
fi

if [[ -z "$HARDHAT_CMD" ]]; then
    echo "❌ Hardhat (npx) no encontrado. Instala con: npm install -g hardhat"
    exit 1
fi

# Flatten
echo "🚀 Flattening contract..."
DOTENV_QUIET=true $HARDHAT_CMD hardhat flatten $CONTRACT > $FLAT_FILE

# Limpiar logs de dotenv (remover primeras 2 líneas)
echo "🧹 Cleaning dotenv logs..."
tail -n +3 $FLAT_FILE > $FLAT_CLEAN

# Ejecutar Slither
echo "🔍 Running Slither..."
$SLITHER_CMD $FLAT_CLEAN --json $RESULTS_DIR/slither-report.json

echo "✅ Done! Report generado en $RESULTS_DIR/slither-report.json"
