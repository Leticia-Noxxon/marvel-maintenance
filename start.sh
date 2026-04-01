#!/bin/bash

# Script para iniciar todos os serviços

echo "🚀 Iniciando Formulário Inteligente..."

# Terminal 1: Backend
echo "📦 Iniciando Backend (FastAPI)..."
cd backend
python main.py &
BACKEND_PID=$!

# Aguardar o backend iniciar
sleep 3

# Terminal 2: Frontend
echo "⚛️  Iniciando Frontend (React)..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Ambos os serviços foram iniciados!"
echo ""
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Para parar:"
echo "  kill $BACKEND_PID  (Backend)"
echo "  kill $FRONTEND_PID (Frontend)"
echo ""
echo "Ou pressione Ctrl+C para interromper ambos"

# Manter scripts rodando
wait
