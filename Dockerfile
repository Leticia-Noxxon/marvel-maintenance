# Usar imagem Node para fazer build do React
FROM node:18-alpine AS react-build

WORKDIR /app/frontend

# Copiar package.json
COPY frontend/package*.json ./

# Instalar dependências
RUN npm ci

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
