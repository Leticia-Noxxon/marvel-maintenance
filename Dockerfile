# Usar imagem Node para fazer build do React
FROM node:18-alpine AS react-build

WORKDIR /app/frontend

# Copiar package.json
COPY frontend/package*.json ./

# Instalar dependências com NODE_OPTIONS para mais memória
ENV NODE_OPTIONS="--max-old-space-size=3072"
ENV CI=false
RUN npm install --legacy-peer-deps

# Copiar código fonte
COPY frontend/ ./

# Fazer build para produção
RUN npm run build

# Usar imagem Python para o backend
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/ ./backend/

# Criar arquivo .env padrão se não existir
RUN if [ ! -f ./backend/.env ]; then \
    echo "EMAIL_USER=nao-configurado" > ./backend/.env && \
    echo "EMAIL_PASSWORD=nao-configurado" >> ./backend/.env && \
    echo "EMAIL_DESTINO=nao-configurado@email.com" >> ./backend/.env && \
    echo "PASTA_UPLOADS=./uploads" >> ./backend/.env && \
    echo "FLASK_ENV=production" >> ./backend/.env && \
    echo "FLASK_DEBUG=False" >> ./backend/.env && \
    echo "PORT=8080" >> ./backend/.env && \
    echo "CORS_ORIGIN=*" >> ./backend/.env; \
fi

# Copiar build do React
COPY --from=react-build /app/frontend/build ./frontend/build

# Variáveis de ambiente padrão
ENV FLASK_APP=backend/main.py
ENV FLASK_ENV=production
ENV PORT=8080

# Expor porta
EXPOSE 8080

# Executar Flask
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
