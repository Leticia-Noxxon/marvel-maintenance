# 🚀 Guia de Início Rápido

## Pré-requisitos

- Node.js 16+ e npm (para React)
- Python 3.8+ e pip (para FastAPI)
- Navegador moderno (Chrome, Firefox, Edge, Safari)
- Conexão com internet

## ⚡ Setup Rápido (5 minutos)

### Passo 1: Clone/Extraia o projeto
```bash
cd c:\Marvel
```

### Passo 2: Configure o Backend

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Editar .env com suas credenciais de email
# Abrir arquivo .env e substituir:
# SENDER_EMAIL=seu_email@gmail.com
# SENDER_PASSWORD=sua_senha_app_gmail

# Rodar o servidor
python main.py
```

**Saída esperada:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Passo 3: Configure o Frontend

**Em outro terminal:**

```bash
cd frontend

# Instalar dependências
npm install

# Rodar em desenvolvimento
npm start
```

**Saída esperada:**
```
On Your Network: http://192.168.X.X:3000/
Compiled successfully!
```

### Passo 4: Teste a Aplicação

1. Abra: [http://localhost:3000](http://localhost:3000)
2. Preencha os dados
3. Clique em "📍 Compartilhar Localização"
4. Clique em "📷 Iniciar Câmera"
5. Tire uma foto
6. Revise e envie

✅ **Pronto!** Você deve receber um email com PDF

## 📱 Testar no Celular

1. No terminal do frontend, copie o IP mostrado (ex: `192.168.1.100:3000`)
2. No celular, abra: `http://192.168.1.100:3000`
3. Clique em "📲 Instalar App"
4. Use normalmente

## ⚙️ Configurar Email

### Gmail (Recomendado)

1. Acesse: https://myaccount.google.com/apppasswords
2. Selecione "Mail" e "Windows Computer"
3. Google gerará uma senha de 16 caracteres
4. Copie e cole no `.env`:

```env
SENDER_EMAIL=seu_email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx
```

### Outlook/Hotmail

```env
SENDER_EMAIL=seu_email@outlook.com
SENDER_PASSWORD=sua_senha
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### Seu Próprio Servidor

```env
SENDER_EMAIL=seu_email@seudominio.com
SENDER_PASSWORD=sua_senha
SMTP_SERVER=mail.seudominio.com
SMTP_PORT=587
```

## 🧪 Testar Funcionalidades

### Testar Geolocalização
- Desktop: Navegador simula localização
- Celular: Ativa GPS real

### Testar Câmera
- Desktop: Webcam do computador
- Celular: Câmera traseira por padrão

### Testar Email
1. Preencha com email real seu
2. Envie o formulário
3. Verifique email (caixa de entrada ou spam)

### Testar PWA
```bash
# Build para produção
cd frontend
npm run build

# Servir localmente
npx serve -s build -l 3000
```

Depois acessar em HTTPS (PWA requer HTTPS em produção)

## 🔧 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Porta 3000 ocupada | `npm start -- --port 3001` |
| Porta 5000 ocupada | Mudar em `main.py`: `port=5001` |
| "Módulo não encontrado" | `pip install -r requirements.txt` |
| Email não chega | Verificar pasta spam e credenciais |
| Câmera não funciona | Permitir acesso nas permissões do navegador |
| CORS error | Certificar que backend está rodando |

## 🎨 Customização Rápida

### Mudar Cores Principais

Buscar em `**/*.css`:
- `#667eea` → sua cor primária
- `#764ba2` → sua cor secundária

### Adicionar Logo

Editar: `frontend/public/index.html`
```html
<link rel="icon" href="seu_logo.png" />
```

### Alterar Nome da App

Editar: `frontend/public/manifest.json`
```json
{
  "name": "Seu Nome de App",
  "short_name": "Nome Curto"
}
```

## 📊 Verificar PDFs Salvos

```bash
# Pasta onde PDFs são salvos
cd backend/uploads
dir  # ou ls no macOS/Linux
```

## 🌐 Deploy Rápido

### Frontend (Vercel)
```bash
cd frontend
npm run build
# Fazer deploy via Vercel CLI ou GitHub
```

### Backend (Heroku)
```bash
heroku login
heroku create seu-app-nome
git push heroku main
```

## 📞 Suporte Rápido

- **Erro de conexão**: Certificar que backend está rodando na porta 5000
- **Localiização bloqueada**: Usar HTTPS em produção
- **Email não autentica**: Usar "App Password" do Gmail (16 caracteres)

---

**Pronto! Você tem um formulário inteligente com PWA, câmera, localização e email configurado! 🎉**
