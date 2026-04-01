# � Manutenção Marvel - Sistema de Controle de Frota

Sistema web completo e responsivo para rastreamento e manutenção de frotas de ônibus com formulários multi-página, geração de PDF, Excel e integração com email.

## ✨ Funcionalidades

✅ **Formulário 6 Páginas**
- Dados gerais (técnico, data, localização)  
- Equipamentos: UCP, TDM, Switch, Antena
- Observações e fotos

✅ **Geolocalização em Tempo Real**
- Captura de localização GPS
- Reverse geocoding (endereço completo)
- Mapa interativo

✅ **Câmera + Fotos**
- Captura de fotos via navegador
- Suporta antes/depois
- Otimizada para mobile

✅ **Exportação de Dados**
- PDF 6 páginas com todas as informações
- Excel auto-gerado com histórico
- Download em um clique

✅ **Email Automático**
- Notificação por email ao técnico
- PDF anexado
- Configurável

✅ **PWA (Progressive Web App)**
- Instalar como app
- Funciona offline (parcialmente)
- Responsivo mobile/desktop

## 🚀 Deployment Rápido

### 🎯 Railway (Gratuito!)

👉 **Guia passo a passo**: [RAILWAY_SETUP_PASSO_A_PASSO.md](./RAILWAY_SETUP_PASSO_A_PASSO.md)

```bash
git push origin main  # Railway faz deploy automaticamente
```

### 💻 Local (Desenvolvimento)

```bash
# Backend
cd backend && python main.py

# Frontend (outro terminal)
cd frontend && npm start
```

Acesse: http://localhost:3000
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── FormularioComponent.js
│   │       ├── FormularioComponent.css
│   │       ├── CameraComponent.js
│   │       ├── CameraComponent.css
│   │       ├── GeolocationComponent.js
│   │       ├── GeolocationComponent.css
│   │       ├── MapComponent.js
│   │       └── MapComponent.css
│   └── package.json
│
└── backend/                  # FastAPI
    ├── main.py
    ├── requirements.txt
    ├── .env
    ├── .env.example
    └── utils/
        ├── __init__.py
        ├── email_service.py
        └── pdf_service.py
```

## 🚀 Instalação e Configuração

### 1. **Frontend (React)**

```bash
cd c:\Marvel\frontend

# Instalar dependências
npm install

# Rodar em desenvolvimento (porta 3000)
npm start

# Build para produção
npm run build
```

### 2. **Backend (FastAPI)**

```bash
cd c:\Marvel\backend

# Criar ambiente virtual (opcional)
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (.env)
# Editar arquivo .env e adicionar suas credenciais de email

# Rodar servidor (porta 5000)
python main.py
```

## ⚙️ Configuração de Email

### Gmail (Recomendado)

1. Ativar "2-Step Verification" em sua conta Google
2. Gerar "App Password": https://myaccount.google.com/apppasswords
3. Adicionar ao arquivo `.env`:

```env
SENDER_EMAIL=seu_email@gmail.com
SENDER_PASSWORD=xxxxx xxxx xxxx xxxx  # Seu App Password (16 caracteres)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Outros Servidores SMTP

Ajuste as configurações no `.env`:

```env
SENDER_EMAIL=seu_email@seuservidor.com
SENDER_PASSWORD=sua_senha
SMTP_SERVER=smtp.seuservidor.com
SMTP_PORT=587  # ou 25, 465 dependendo do provedor
```

## 📱 Como Usar

### No Computador
1. Abra: `http://localhost:3000`
2. Preencha os campos básicos
3. Clique em "Compartilhar Localização"
4. Clique em "Iniciar Câmera" e tire uma foto
5. Revise o resumo
6. Clique em "Enviar Formulário"

### No Celular
1. Abra: `http://seu-ip:3000` (ex: `http://192.168.1.100:3000`)
2. Clique em "📲 Instalar App"
3. Siga o mesmo fluxo acima

### Usar a App Instalada
- Após instalar, icon aparecerá na home screen
- Funciona como app nativo
- Acesso offline funciona (com dados salvos)

## 📊 API Endpoints

### POST `/api/formulario/enviar`
Envia o formulário, gera PDF e envia email

**Payload:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "telefone": "(11) 99999-9999",
  "empresa": "Empresa ABC",
  "departamento": "TI",
  "assunto": "Suporte",
  "descricao": "Descrição detalhada...",
  "data": "01/04/2025",
  "hora": "10:30:45",
  "localizacao": "São Paulo, SP",
  "latitude": -23.5505,
  "longitude": -46.6333,
  "foto": "data:image/jpeg;base64,...",
  "campo1": "valor1",
  ...
}
```

**Resposta Sucesso (200):**
```json
{
  "status": "sucesso",
  "message": "Formulário enviado com sucesso!",
  "pdf_name": "formulario_joao_silva_20250401_103045.pdf",
  "timestamp": "2025-04-01T10:30:45.123456"
}
```

### GET `/api/formulario/listar`
Lista todos os PDFs gerados

**Resposta:**
```json
{
  "status": "sucesso",
  "total": 5,
  "formularios": [
    {
      "nome": "formulario_joao_silva_20250401_103045.pdf",
      "tamanho": "350.42 KB",
      "data_criacao": "2025-04-01T10:30:45"
    }
  ]
}
```

### GET `/api/health`
Verifica se API está funcionando

## 🔒 Permissões Necessárias

O aplicativo solicita:
- ✅ **Geolocalização** - Para capturar localização do usuário
- ✅ **Câmera** - Para tirar fotos
- ✅ **Armazenamento Local** - Para salvar rascunhos

## 📝 Customizações

### Adicionar Mais Campos
Editar [src/components/FormularioComponent.js](src/components/FormularioComponent.js) e adicionar campos no estado `formData`:

```javascript
const [formData, setFormData] = useState({
  // ... campos existentes
  seu_novo_campo: '',
});
```

### Alterar Cores do Tema
Editar variáveis CSS gradientes:
- `#667eea` e `#764ba2` são as cores primárias
- Buscar e replacar em arquivos `.css`

### Adicionar Mais Etapas
Adicionar nova case no condicional `etapa` em FormularioComponent.js

## 🐛 Troubleshooting

### "Câmera não funciona"
- Verificar permissões do navegador para câmera
- Em HTTPS, funciona melhor que HTTP
- Alguns navegadores antigos não suportam

### "Email não envia"
- Verificar credenciais em `.env`
- Para Gmail, confirmar "App Password"
- Verificar firewall/antivírus bloqueando SMTP

### "Localização não funciona"
- Ativar GPS/localização no dispositivo
- Em HTTPS, funciona melhor
- Alguns navegadores bloqueiam por padrão

### "PWA não instala"
- Acessar via HTTPS em produção (PWA requer HTTPS)
- Verificar manifest.json sintaxe
- Limpar cache do navegador

## 🌐 Deploy

### Produção (Firebase Hosting)

**Frontend:**
```bash
cd frontend
npm run build
# Configurar e fazer deploy com Firebase CLI
firebase deploy --only hosting
```

**Backend:**
```bash
# Deploy no Heroku, Railway, ou similar
# Configurar variáveis de ambiente no provedor
git push heroku main
```

## 📚 Tecnologias

- **Frontend:** React 18, Leaflet (mapas), Axios
- **Backend:** Flask, ReportLab (PDF), SMTP
- **PWA:** Service Workers, manifest.json
- **APIs:** Geolocation API, Camera API, localStorage

## 📄 Licença

MIT License - Livre para usar, modificar e distribuir

## 👨‍💻 Suporte

Para dúvidas ou problemas, verificar:
1. Console do navegador (F12)
2. Logs do servidor backend
3. Arquivo `.env` configurado corretamente

---

**© 2025 Formulário Inteligente** - Desenvolvido com ❤️
