# Railway Deployment Guide - Manutenção Marvel

Railway oferece **$5/mês em crédito GRATUITO** - mais que o suficiente para este app!

## 🚀 Setup em 5 Minutos

### Passo 1: Criar Conta no Railway
1. Acesse: https://railway.app
2. Clique "Start Project" 
3. Faça login com GitHub (ou email)

### Passo 2: Conectar o Repositório
Você tem duas opções:

#### Opção A: Git (Recomendado)
```bash
# Na raiz do projeto
git init
git add .
git commit -m "Initial Marvel Maintenance App"
git remote add origin https://github.com/SEU_USUARIO/marvel-maintenance.git
git push -u origin main
```

Depois no Railway:
- Click "New Project" > "Deploy from GitHub"
- Selecione o repositório
- Railway detecta automaticamente e faz deploy

#### Opção B: Sem Git (Mais Rápido)
1. No Railway, selecione "Deploy from Plugin"
2. Escolha "Blank Canvas"
3. Faça upload dos arquivos

### Passo 3: Configurar Variáveis de Ambiente
No painel do Railway, vá em "Variables" e adicione:

```
FLASK_ENV=production
FLASK_DEBUG=False
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
EMAIL_DESTINO=seu_email@gmail.com
GOOGLE_SHEETS_API_KEY=sua_chave_aqui (opcional)
CORS_ORIGIN=https://seu-app.railway.app
```

### Passo 4: Build & Deploy
Railway detecta automaticamente:
- Root: `package.json` → Node.js
- Raiz: `requirements.txt` → Python

Você precisa criar um `Procfile` para indicar como rodar os dois serviços.

---

## 📁 Estrutura Necessária

Criar arquivo na raiz: `/railway.json`

```json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "startCommand": "python backend/main.py & npm --prefix frontend start"
  }
}
```

**OU** criar um `Procfile` na raiz:

```
web: npm --prefix frontend start & python backend/main.py
```

---

## 🔨 Versão Simplificada com Docker (Recomendado)

Criar arquivo: `/Dockerfile` na raiz

```dockerfile
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

# Backend
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Frontend (copiar build anterior)
COPY --from=frontend-builder /app/frontend/build ./frontend/build
COPY backend/ ./backend/
COPY frontend/package*.json ./frontend/

EXPOSE 5000 3000

CMD ["sh", "-c", "cd backend && python main.py"]
```

---

## 🎯 Steps Finais

1. Abra https://railway.app
2. Clique "New Project"
3. Escolha "Deploy from GitHub" ou "Deploy from URL"
4. Railway auto-detectar e fazer deploy
5. Em 2-3 minutos, você recebe um link tipo:
   ```
   https://marvel-maintenance.railway.app
   ```

---

## 🔗 Resultado Final
```
🌍 Frontend:  https://seu-app.railway.app
🔌 API:       https://seu-app.railway.app/api
📥 Download:  https://seu-app.railway.app/api/download-excel
```

Qualquer pessoa em qualquer lugar consegue acessar! ✨

---

## ⚠️ Cuidados

1. **Variáveis de Ambiente**: Nunca comita .env na repo
2. **Email**: Se usar Gmail, precisa de "App Password" (2FA ativado)
3. **Storage**: Railway usa storage temporário - Excel fica por 24h

---

## 💰 Custo
- **Gratuito**: $5/mês em crédito (suficiente!)
- **Pago**: Começa em $5/mês se ultrapassar o crédito

---

## 🆘 Problemas Comuns

**"Port 3000 não encontrada"**
→ Railway detecta automaticamente. Se não, ajuste em railway.json

**"Erro ao conectar API"**
→ Atualize CORS_ORIGIN em variáveis de ambiente

**"Excel não salva"**
→ Usar banco de dados persistente (PostgreSQL no Railway é gratuito!)

---

### Quer que eu configure tudo para você?
Só me dizer e faço os arquivos necessários!
