@echo off
REM Script para iniciar todos os serviços no Windows

echo 🚀 Iniciando Formulário Inteligente...
echo.

REM Abrir Backend em nova janela
echo 📦 Iniciando Backend (FastAPI)...
start "Backend - FastAPI" cmd /k "cd backend && python main.py"

REM Aguardar um pouco
timeout /t 3 /nobreak

REM Abrir Frontend em nova janela
echo ⚛️  Iniciando Frontend (React)...
start "Frontend - React" cmd /k "cd frontend && npm start"

echo.
echo ✅ Ambos os serviços foram iniciados em novas janelas!
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Feche as janelas para parar os serviços.
