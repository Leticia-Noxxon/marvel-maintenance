# 🚀 Deployment no Railway - Guia Passo a Passo

Railway é gratuito para seus primeiros $5/mês! Perfeito para este app.

## ✅ Pré-requisitos

- [ ] Conta GitHub
- [ ] Código commitado no GitHub
- [ ] Arquivo `Dockerfile` (✓ já criado)
- [ ] Arquivo `.env.example` (✓ já criado)

---

## 📋 Passo 1: Preparar Repositório Git

```bash
# Na raiz do projeto
git init
git add .
git commit -m "Initial Marvel Maintenance App"
git remote add origin https://github.com/SEU_USUARIO/marvel-maintenance.git
git branch -M main
git push -u origin main
```

---

## 🔗 Passo 2: Conectar no Railway

1. Acesse: **https://railway.app**
2. Clique em **"Start a New Project"**
3. Escolha **"Deploy from GitHub"**
4. Autorize o Railway com sua conta GitHub
5. Selecione o repositório `marvel-maintenance`
6. Railway detecta automaticamente e inicia o deploy!

---

## ⚙️ Passo 3: Configurar Variáveis de Ambiente

No painel do Railway:

1. Vá para **"Variables"**
2. Adicione as seguintes variáveis:

```
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app_gmail
EMAIL_DESTINO=seu_email@email.com
FLASK_ENV=production
PORT=8080
CORS_ORIGIN=https://seu-domain-railway.up.railway.app
```

### ⚠️ Importante: Gmail App Password

Se usar Gmail, você precisa de uma **"Senha de App"**, não da senha da conta:

1. Ative 2FA em https://myaccount.google.com/security
2. Vá para https://myaccount.google.com/apppasswords
3. Escolha "Mail" e "Windows Computer"
4. Copie a senha gerada (16 caracteres)
5. Cole em `EMAIL_PASSWORD` no Railway

---

## 🏗️ Passo 4: Build & Deploy

Railway automaticamente:
1. Detecta o `Dockerfile`
2. Faz build da imagem
3. Compila o React
4. Instala dependências Python
5. Inicia o Flask na porta 8080

**Tempo de deploy: ~2-3 minutos**

---

## 🌍 Passo 5: Acessar o App

Após o deploy:

```
Frontend:  https://seu-domain-railway.up.railway.app
API:       https://seu-domain-railway.up.railway.app/api
Download:  https://seu-domain-railway.up.railway.app/api/download-excel
```

O Railway gera um domínio automaticamente. Você vê no painel principal!

---

## 🔄 Atualizações Futuras

Toda vez que você fizer `git push`:

```bash
git add .
git commit -m "Update: feature X"
git push origin main
```

Railway automaticamente faz redeploy! 🎉

---

## 🆘 Troubleshooting

### "Build failed"
- Verifique se o Dockerfile está no commit
- Verifique se `requirements.txt` existe
- Verifique se `package.json` do frontend existe

### "Port 8080 não encontrada"
- É normal! Railway redireciona automaticamente

### "API retorna 404"
- Certifique-se que CORS_ORIGIN está correto em Variables
- Verifique se o frontend está fazendo requests para `/api` (sem domínio)

### "Excel não faz download"
- Verifique pasta `uploads` - Railway tem storage temporário
- Para produção: use PostgreSQL do Railway para persistência

---

## 💰 Custos

- **Gratuito**: $5/mês em crédito (suficiente!)
- **Depois**: $5/mês se ultrapassar (ajuste conforme necessário)

---

## 🎯 Próximos Passos

1. **Domínio próprio**: Railway permite apontar domínio customizado
2. **Banco de dados**: PostgreSQL gratuito no Railway
3. **Monitoramento**: Logs em tempo real no painel

---

## ✨ Pronto!

Seu app estará online para qualquer pessoa acessar de qualquer dispositivo! 🚀

**Precisa de ajuda com algo específico? Avise!**
