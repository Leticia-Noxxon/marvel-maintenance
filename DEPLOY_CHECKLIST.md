# ✅ Checklist de Deployment - Railway

Tudo que você precisa fazer antes de colocar o app no ar!

## 📋 Preparação Local

- [ ] Certifique-se que o backend roda: `python backend/main.py`
- [ ] Certifique-se que o frontend roda: `npm --prefix frontend start`
- [ ] Teste o download do Excel: botão "Baixar Excel" funciona?
- [ ] Verifique configurações de email no `.env`

## 🔧 Configuração de Produção

- [ ] Arquivo `Dockerfile` existe na raiz ✓
- [ ] Arquivo `Procfile` existe na raiz ✓
- [ ] `.env.example` preenchido com valores de exemplo ✓
- [ ] `requirements.txt` atualizado ✓
- [ ] `package.json` (frontend) está correto ✓

## 🌐 GitHub (Repositório)

```bash
# 1️⃣ Iniciando Git
git init
git add .
git commit -m "Marvel Maintenance App - Ready for Production"

# 2️⃣ Conectando ao GitHub
git remote add origin https://github.com/SEU_USUARIO/marvel-maintenance.git
git branch -M main
git push -u origin main
```

- [ ] Repositório criado no GitHub
- [ ] Código commitado e pushed
- [ ] Arquivo `.gitignore` está funcionando
- [ ] `.env` **NÃO** foi commitado (apenas `.env.example`)

## 🚀 Railway Deployment

### Passo 1: Conectar Repository

- [ ] Conta criada em https://railway.app
- [ ] GitHub autorizado no Railway
- [ ] Repositório `marvel-maintenance` selecionado
- [ ] Deployment iniciado (Railway auto-detecta Dockerfile)

### Passo 2: Configurar Variáveis

No painel Railway → "Variables":

```
EMAIL_USER             seu_email@gmail.com
EMAIL_PASSWORD         sua_senha_app_gmail
EMAIL_DESTINO          seu_email@gmail.com
FLASK_ENV              production
PORT                   8080
CORS_ORIGIN            https://seu-app.railway.up.railway.app
```

- [ ] EMAIL_USER configurado
- [ ] EMAIL_PASSWORD configurado (App Password do Gmail)
- [ ] EMAIL_DESTINO configurado
- [ ] CORS_ORIGIN com o domínio correto do Railway

### Passo 3: Verificar Deploy

- [ ] Build completou com sucesso (2-3 minutos)
- [ ] Nenhum erro nos logs
- [ ] URL pública gerada

## 🎯 Teste Final

### Links para Testar

```
Frontend:   https://seu-domain-railway.up.railway.app
API Health: https://seu-domain-railway.up.railway.app/api/health
Download:   https://seu-domain-railway.up.railway.app/api/download-excel
```

### Testes a Fazer

- [ ] Abrir link do Frontend no navegador
- [ ] Preencher formulário completo
- [ ] Enviar formulário
- [ ] Clicar em "Baixar Excel"
- [ ] Verificar se arquivo foi criado
- [ ] Testar em celular/mobile

## 💾 Domínio Customizado (Opcional)

Se você tem um domínio próprio:

1. No Railway → Settings → Domains
2. Clique "Add Custom Domain"
3. Digite seu domínio: `app.suaempresa.com.br`
4. Configure DNS apontando para Railway
5. Atualizar `CORS_ORIGIN` com o novo domínio

- [ ] Domínio customizado configurado (se aplicável)
- [ ] CORS_ORIGIN atualizado

## 🔄 Atualizações Futuras

Para cada atualização:

```bash
git add .
git commit -m "Descrição da alteração"
git push origin main
```

Railway automaticamente faz redeploy! ✨

- [ ] Workflow de deploy automático compreendido

## 📊 Monitoramento

No painel Railway você pode:

- [ ] Ver logs em tempo real
- [ ] Monitorar uso de recursos
- [ ] Configurar alertas
- [ ] Ver histórico de deployments

## ✨ Pronto!

você completou todas as etapas?

✅ **SIM** → Seu app está no ar! 🎉
❌ **NÃO** → Volte para o passo anterior e revise

---

## 🆘 Troubleshooting

### "Build falhou"
```
Verifique:
- Dockerfile existe?
- requirements.txt existe?
- package.json existe?
- Nenhuma erro de sintaxe?
```

### "App está offline"
```
Verifique:
- CORS_ORIGIN está correto?
- EMAIL_PASSWORD está correto? (App Password, não senha normal)
- PORT=8080 está configurado?
```

### "Excel não faz download"
```
Railway tem storage temporário. Solução:
- Adicione PostgreSQL (gratuito no Railway)
- Mude PASTA_UPLOADS para persistência
```

---

## 🎯 Próximas Melhorias

1. Banco de dados PostgreSQL (Railway oferece!)
2. Autenticação de usuários
3. Dashboard de relatórios
4. Sincronização offline avançada

---

**Sucesso no deployment! 🚀**

Alguma dúvida? Verifique os guias:
- [RAILWAY_SETUP_PASSO_A_PASSO.md](./RAILWAY_SETUP_PASSO_A_PASSO.md)
- [README.md](./README.md)
