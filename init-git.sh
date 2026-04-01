#!/usr/bin/env bash
# Script para inicializar Git e fazer primeiro push

cd "$(dirname "$0")"

echo "🚀 Inicializando repositório Git..."
git init

echo "📝 Configurando Git..."
git config user.email "seu_email@github.com"
git config user.name "Seu Nome"

echo "📦 Adicionando arquivos..."
git add .

echo "💾 Fazendo commit..."
git commit -m "Initial commit: Marvel Maintenance App - Pronto para Railway"

echo "
✅ Git inicializado!

PRÓXIMOS PASSOS:
================

1. Crie um repositório no GitHub: https://github.com/new
   - Nome: marvel-maintenance
   
2. Copie o URL do repositório (HTTPS)

3. Execute:
   git remote add origin https://github.com/SEU_USUARIO/marvel-maintenance.git
   git branch -M main
   git push -u origin main

4. Railway detectará automaticamente e fará deploy!
"
