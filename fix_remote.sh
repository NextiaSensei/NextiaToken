#!/bin/bash
echo "🔧 SOLUCIÓN DEFINITIVA"

cd ~/proyectos/nextia/trading/token

echo "📋 Remote actual:"
git remote -v

echo ""
echo "🎯 OPCIONES:"
echo "1. Usar repositorio EXISTENTE (nextia)"
echo "2. Crear NUEVO repositorio (nextia-trading-token)"
echo ""
read -p "Selecciona (1 o 2): " opcion

case $opcion in
    1)
        echo "🔄 Usando repositorio nextia existente..."
        git remote remove origin
        git remote add origin https://github.com/NextiaSensei/nextia.git
        echo "✅ Remote configurado a nextia"
        ;;
    2)
        echo "📝 PRIMERO crea el repositorio en GitHub:"
        echo "🌐 Ve a: https://github.com/new"
        echo "💎 Nombre: nextia-trading-token"
        echo "🔓 Público"
        echo "❌ NO inicializar con README"
        echo ""
        read -p "Presiona Enter cuando hayas creado el repositorio..."
        
        echo "🔄 Configurando nuevo remote..."
        git remote remove origin
        git remote add origin https://github.com/NextiaSensei/nextia-trading-token.git
        echo "✅ Remote configurado a nextia-trading-token"
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo "📤 Haciendo push..."
git push -u origin main

echo "🎉 ¡SOLUCIONADO!"
