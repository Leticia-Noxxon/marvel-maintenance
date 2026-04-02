# Google Drive Setup - Marvel Maintenance

## 📋 Passos para Configurar Autenticação com Google Drive

### 1️⃣ Criar um Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Create Project"** (ou selecione um projeto existente)
3. Nomeie o projeto: `Marvel Maintenance`
4. Clique em **Create**

### 2️⃣ Habilitar Google Drive API

1. Vá para **APIs & Services** → **Library**
2. Procure por **"Google Drive API"**
3. Clique em **"Enable"**

### 3️⃣ Criar Credenciais (OAuth 2.0)

1. Vá para **APIs & Services** → **Credentials**
2. Clique em **"+ Create Credentials"** → **OAuth client ID**
3. Será solicitado criar uma **"OAuth consent screen"**:
   - Escolha **"External"**
   - Preencha:
     - App name: `Marvel Maintenance`
     - User support email: seu_email@gmail.com
     - Developer contact: seu_email@gmail.com
   - Clique **Save and Continue**
4. Na aba **Scopes**, clique **Add or Remove Scopes**:
   - Procure por `drive.file` e clique na **checkbox**
   - Clique **Update**
5. Clique **Save and Continue**
6. Volte a **Credentials** e clique **+ Create Credentials** novamente
7. Escolha **"OAuth client ID"**
8. Selecione **"Desktop app"** como tipo de aplicativo
9. Clique **Create**

### 4️⃣ Baixar credentials.json

1. Clique no ícone de download do cliente OAuth criado
2. Salve o arquivo como **`credentials.json`**
3. Coloque na pasta **`backend/`** do Marvel Maintenance:
   ```
   Marvel/
   ├── backend/
   │   ├── credentials.json ← AQUI!
   │   ├── main.py
   │   ├── requirements.txt
   │   └── ...
   ```

### 5️⃣ Primeira Autenticação (Local)

1. No seu computador, abra terminal na pasta `backend/`:
   ```bash
   cd c:\Marvel\backend
   python -c "from utils.google_drive_service import autenticar_google; autenticar_google()"
   ```

2. Uma janela do navegador vai abrir pedindo para:
   - Fazer login com sua conta Google
   - Autorizar acesso ao Google Drive

3. Após autorizar, um arquivo **`token.json`** será criado automaticamente

4. Agora está pronto! Você pode fazer upload de imagens automaticamente! ✅

### 6️⃣ Deploy no Render

⚠️ **IMPORTANTE**: No Render, você precisa:

1. **Não commitar** `credentials.json` (é privado!)
2. Adicionar `.gitignore`:
   ```
   credentials.json
   token.json
   ```

3. No Render, faça upload do `credentials.json` via:
   - **Render Dashboard** → Seu Projeto → **Files** (ou SSH)
   - Ou adicione via **Environment Variables** com conteúdo base64

---

## 🎯 Resultado Final

✅ Imagens salvam automaticamente no Google Drive  
✅ Excel tem hyperlinks clicáveis  
✅ Nada fica no servidor do Render  
✅ Espaço infinito e gratuito! 🚀

