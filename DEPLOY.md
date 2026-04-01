# 🌐 Guia de Deploy

## Deploy Local (Desenvolvimento)

### Backend + Frontend Local

1. **Backend:**
```bash
cd backend
python main.py
# Rodará em: http://localhost:5000
```

2. **Frontend:**
```bash
cd frontend
npm start
# Rodará em: http://localhost:3000
```

Ou use o script automatizado:
```bash
# Windows
start.bat

# macOS/Linux
bash start.sh
```

---

## Deploy em Produção

### 1. Deploy Frontend (React)

#### Opção A: Vercel (Recomendado)

```bash
cd frontend
npm run build

# Instalar Vercel CLI
npm i -g vercel

# Fazer deploy
vercel
```

#### Opção B: Netlify

```bash
cd frontend
npm run build

# Instalar Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=build
```

#### Opção C: AWS S3 + CloudFront

```bash
cd frontend
npm run build

# Fazer upload para S3
aws s3 sync build/ s3://seu-bucket-nome

# Invalidar CloudFront (opcional)
aws cloudfront create-invalidation --distribution-id SEUS_ID --paths "/*"
```

#### Opção D: Seu Próprio Servidor (Nginx)

```bash
cd frontend
npm run build

# Copiar arquivos para servidor
scp -r build/* usuario@seu-servidor:/var/www/seu-app

# Configurar Nginx
# sudo nano /etc/nginx/sites-available/seu-app
```

Configuração Nginx:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    root /var/www/seu-app;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Deploy Backend (FastAPI)

#### Opção A: Heroku

```bash
cd backend

# Criar arquivo Procfile
echo "web: python main.py" > Procfile

# Criar arquivo runtime.txt
echo "python-3.10.0" > runtime.txt

# Fazer deploy
heroku login
heroku create seu-app-nome
heroku config:set SENDER_EMAIL=seu_email@gmail.com
heroku config:set SENDER_PASSWORD=sua_senha_app
git push heroku main
```

#### Opção B: Railway.app

```bash
cd backend

# Conectar com GitHub
# Configurar variáveis de ambiente via dashboard
# Deploy automático a cada push
```

#### Opção C: Render.com

```bash
# Copiar esquema em render.yaml:
services:
  - type: web
    name: formulario-app
    runtime: python
    startCommand: python main.py
    envVars:
      - key: SENDER_EMAIL
        value: seu_email@gmail.com
```

#### Opção D: Seu Próprio Servidor (Linux)

```bash
# 1. Conectar ao servidor
ssh usuario@seu-servidor.com

# 2. Instalar Python e pip
sudo apt update
sudo apt install python3 python3-pip git

# 3. Clonar projeto
git clone seu-repo.git
cd seu-repo/backend

# 4. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Configurar variáveis de ambiente
nano .env
# Adicionar credenciais

# 7. Testar localmente
python main.py

# 8. Instalar supervisor (para manter app rodando)
sudo apt install supervisor

# 9. Criar arquivo de configuração supervisor
sudo nano /etc/supervisor/conf.d/formulario.conf
```

Arquivo supervisor.conf:
```ini
[program:formulario-backend]
directory=/home/usuario/seu-repo/backend
command=/home/usuario/seu-repo/backend/venv/bin/python main.py
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/formulario-backend.log
```

```bash
# 10. Iniciar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start formulario-backend

# 11. Configure Nginx como reverse proxy
sudo nano /etc/nginx/sites-available/seu-app
```

#### Opção E: Docker (Recomendado para produção)

**Criar Dockerfile no backend:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

**Criar docker-compose.yml na raiz:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - SENDER_EMAIL=${SENDER_EMAIL}
      - SENDER_PASSWORD=${SENDER_PASSWORD}
    volumes:
      - ./backend/uploads:/app/uploads

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "3000:3000"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
```

**Deploy com Docker:**
```bash
docker-compose up -d
```

### 3. Configurar SSL/HTTPS

#### Let's Encrypt + Certbot

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Gerar certificado
sudo certbot certonly --standalone -d seu-dominio.com

# Configurar Nginx com SSL
sudo nano /etc/nginx/sites-available/seu-app
```

Configuração com SSL:
```nginx
server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;

    # ... resto da configuração
}

# Redirecionar HTTP para HTTPS
server {
    listen 80;
    server_name seu-dominio.com;
    return 301 https://$server_name$request_uri;
}
```

### 4. Configurar Build Automático (CI/CD)

#### GitHub Actions

Criar `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Deploy Frontend
      run: |
        cd frontend
        npm install
        npm run build
        # Adicionar comando de deploy (ex: vercel)

    - name: Deploy Backend
      run: |
        cd backend
        pip install -r requirements.txt
        # Adicionar comando de deploy (ex: heroku)
```

---

## Checklist de Segurança para Produção

- [ ] Alterar chave secreta ( gerada)
- [ ] Habilitar HTTPS/SSL
- [ ] Configurar CORS apenas para domínios permitidos
- [ ] Validar todos os inputs
- [ ] Usar variáveis de ambiente para credenciais
- [ ] Configurar rate limiting
- [ ] Adicionar logging
- [ ] Realizar backup regular
- [ ] Monitorar erros e performance
- [ ] Atualizar dependências regularmente

---

## Monitoramento

### Frontend
```bash
# Usar Sentry para error tracking
npm install @sentry/react

# Configurar em src/index.js
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "sua-dsn-do-sentry"
});
```

### Backend
```bash
# Usar LogRocket ou DataDog
pip install datadog

# Ou usar Sentry
pip install sentry-sdk
```

---

## Performance

### Frontend
```bash
# Análise de bundle
npm install -g webpack-bundle-analyzer

# Build otimizado
npm run build
```

### Backend
```bash
# Usar Gunicorn + multiple workers
pip install gunicorn
gunicorn --workers 4 --worker-class gthread main:app
```

---

**Deploy feito com sucesso! 🚀**
