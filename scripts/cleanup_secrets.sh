#!/usr/bin/env bash
# scripts/cleanup_secrets.sh
# Script para escanear secretos y aplicar remediaciones iniciales (no reescribe historial)
# Úsalo localmente en tu clon del repo. NO lo ejecutes en CI sin revisar.

set -euo pipefail

echo "== NextiaToken: Limpieza y escaneo inicial de secretos =="

# 1) Comprobar que estamos en un repositorio git
if [ ! -d .git ]; then
  echo "❌ No parece que estés en la raíz de un repositorio git. Clona el repo y ejecuta esto desde la raíz." >&2
  exit 1
fi

# 2) Añadir entradas críticas a .gitignore si no existen
echo "\n📝 Asegurando .gitignore..."
GITIGNORE_FILE=.gitignore
mkdir -p $(dirname "$GITIGNORE_FILE") || true

# Entradas que queremos asegurar
read -r -d '' ENTRIES << 'EOF' || true
venv/
.env
.env.*
__pycache__/
*.pyc
EOF

for entry in $(echo "$ENTRIES"); do
  if ! grep -qxF "$entry" "$GITIGNORE_FILE" 2>/dev/null; then
    echo "$entry" >> "$GITIGNORE_FILE"
    echo "  + Agregado: $entry"
  fi
done

# 3) Quitar venv/.env del índice (no borra del disco, solo del índice de git)
echo "\n🚮 Eliminando venv/ y .env del índice de git (si existen en el índice)..."

# Solo ejecutar git rm --cached si esos archivos/carpetas están en el índice
if git ls-files --error-unmatch venv >/dev/null 2>&1; then
  git rm -r --cached venv || true
  echo "  - venv/ removido del índice"
else
  echo "  - venv/ no estaba en el índice"
fi

if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  git rm --cached .env || true
  echo "  - .env removido del índice"
else
  echo "  - .env no estaba en el índice"
fi

# Añadir .gitignore al commit si hay cambios
if ! git diff --quiet -- "$GITIGNORE_FILE"; then
  git add "$GITIGNORE_FILE"
fi

# Detectar si hay cambios para commitear
if ! git diff --cached --quiet; then
  echo "\n📦 Preparando commit con cambios locales (no se hace push automáticamente)..."
  git commit -m "chore(security): remove venv and .env from index, ensure gitignore entries"
  echo "✅ Commit creado. Revisa los cambios y haz push cuando estés listo: git push"
else
  echo "✅ No hay cambios pendientes para commitear (o ya fueron aplicados)."
fi

# 4) Escaneo con gitleaks (si está instalado)
echo "\n🔍 Escaneando el repositorio con gitleaks (si está instalado)..."
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect -s . --report-path gitleaks-report.json || true
  if [ -s gitleaks-report.json ]; then
    echo "⚠️  gitleaks ha encontrado posibles secretos. Revisa gitleaks-report.json"
    echo "   - Si son falsos positivos, documenta por qué y añade excepciones al pipeline."
    echo "   - Si son secretos reales: rótalos inmediatamente antes de limpiar historial."
  else
    echo "✅ gitleaks no encontró secretos evidentes (gitleaks-report.json vacío o no hay coincidencias)."
  fi
else
  echo "ℹ️  gitleaks no está instalado. Recomendado: https://github.com/gitleaks/gitleaks"
  echo "   Instálalo y ejecuta: gitleaks detect -s . --report-path gitleaks-report.json"
fi

# 5) Informar siguiente pasos
cat <<'MSG'

Siguientes pasos recomendados (leer con atención):

1) Si gitleaks encontró secretos reales: RÓTALOS YA (Binance, Telegram, AWS, etc.).
   - Revoca la API key en el servicio correspondiente y crea una nueva.
   - Solo después de rotar, procede a purgar el historial (git-filter-repo o BFG).

2) Para purgar secretos del historial (esto REESCRIBE la historia):
   - Usar git-filter-repo (recomendado): https://github.com/newren/git-filter-repo
     Ejemplo:
       git clone --mirror https://github.com/NextiaSensei/NextiaToken.git
       cd NextiaToken.git
       # eliminar carpeta venv del historial
       git filter-repo --invert-paths --paths venv
       # o reemplazar textos sensibles usando un archivo replace.txt
       git filter-repo --replace-text ../replace.txt
       git push --force --mirror origin

   - O usar BFG (más simple para archivos comunes):
       git clone --mirror https://github.com/NextiaSensei/NextiaToken.git
       java -jar bfg.jar --delete-files ".env,venv" NextiaToken.git
       cd NextiaToken.git
       git reflog expire --expire=now --all && git gc --prune=now --aggressive
       git push --force --mirror origin

3) Después de reescribir la historia, INFORMA a todos los colaboradores que deben clonar de nuevo:
   - git clone https://github.com/NextiaSensei/NextiaToken.git

4) Añadir escaneo automático en CI (gitleaks) y hooks pre-commit (detect-secrets o gitleaks) para prevenir re-exposición.

MSG

echo "\n✅ Script completado. Revisa gitleaks-report.json si existe y dime si quieres que prepare los comandos para git-filter-repo/BFG (yo puedo generar el replace.txt listo para usar)."
