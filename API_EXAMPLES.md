# Exemplos de Requisições à API

## 1. Verificar se a API está funcionando

```bash
curl -X GET http://localhost:5000/api/health
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "message": "API de Formulário está rodando",
  "timestamp": "2025-04-01T10:30:45.123456"
}
```

## 2. Enviar Formulário Completo

```bash
curl -X POST http://localhost:5000/api/formulario/enviar \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@empresa.com",
    "telefone": "(11) 98765-4321",
    "empresa": "Empresa XYZ",
    "departamento": "Vendas",
    "assunto": "Consulta de Produtos",
    "descricao": "Gostaria de mais informações sobre os produtos disponíveis.",
    "data": "01/04/2025",
    "hora": "14:30:00",
    "localizacao": "São Paulo, SP",
    "latitude": -23.5505,
    "longitude": -46.6333,
    "foto": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABg...",
    "campo1": "Informação 1",
    "campo2": "Informação 2"
  }'
```

**Resposta esperada:**
```json
{
  "status": "sucesso",
  "message": "Formulário enviado com sucesso!",
  "pdf_name": "formulario_joao_silva_20250401_143000.pdf",
  "timestamp": "2025-04-01T14:30:00.123456"
}
```

## 3. Listar todos os PDFs gerados

```bash
curl -X GET http://localhost:5000/api/formulario/listar
```

**Resposta esperada:**
```json
{
  "status": "sucesso",
  "total": 3,
  "formularios": [
    {
      "nome": "formulario_joao_silva_20250401_143000.pdf",
      "tamanho": "350.42 KB",
      "data_criacao": "2025-04-01T14:30:00"
    },
    {
      "nome": "formulario_maria_santos_20250401_150000.pdf",
      "tamanho": "275.15 KB",
      "data_criacao": "2025-04-01T15:00:00"
    }
  ]
}
```

## 4. Testar com Python Requests

```python
import requests
import json

# URL da API
API_URL = "http://localhost:5000"

# Dados do formulário
dados = {
    "nome": "Ana Costa",
    "email": "ana@empresa.com",
    "telefone": "(11) 91234-5678",
    "empresa": "Tech Solutions",
    "departamento": "Marketing",
    "assunto": "Parceria Comercial",
    "descricao": "Estou interessada em estabelecer uma parceria.",
    "data": "01/04/2025",
    "hora": "16:45:00",
    "localizacao": "Rio de Janeiro, RJ",
    "latitude": -22.9068,
    "longitude": -43.1729,
    "foto": "data:image/jpeg;base64,...",
    "campo1": "Valor 1"
}

# Enviar formulário
resposta = requests.post(
    f"{API_URL}/api/formulario/enviar",
    json=dados,
    headers={"Content-Type": "application/json"}
)

print("Status:", resposta.status_code)
print("Resposta:", resposta.json())

# Listar formulários
resposta_lista = requests.get(f"{API_URL}/api/formulario/listar")
print("\nFormulários salvos:")
print(json.dumps(resposta_lista.json(), indent=2, ensure_ascii=False))
```

## 5. Testar com JavaScript/Fetch

```javascript
// Enviar formulário
const dados = {
  nome: "Carlos Santos",
  email: "carlos@empresa.com",
  telefone: "(11) 99876-5432",
  empresa: "Global Corp",
  departamento: "TI",
  assunto: "Suporte Técnico",
  descricao: "Problema com acesso ao sistema",
  data: new Date().toLocaleDateString('pt-BR'),
  hora: new Date().toLocaleTimeString('pt-BR'),
  localizacao: "Curitiba, PR",
  latitude: -25.4284,
  longitude: -49.2733,
  foto: canvasElement.toDataURL('image/jpeg', 0.9)
};

fetch('http://localhost:5000/api/formulario/enviar', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(dados)
})
  .then(res => res.json())
  .then(data => {
    if (data.status === 'sucesso') {
      console.log('✅ Formulário enviado com sucesso!');
      console.log('PDF gerado:', data.pdf_name);
    } else {
      console.error('❌ Erro:', data.message);
    }
  })
  .catch(err => console.error('Erro de conexão:', err));
```

## 6. Testar com Postman/Insomnia

### Health Check
- **Method:** GET
- **URL:** `http://localhost:5000/api/health`

### Enviar Formulário
- **Method:** POST
- **URL:** `http://localhost:5000/api/formulario/enviar`
- **Headers:** 
  - `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "nome": "Teste",
  "email": "teste@email.com",
  "telefone": "(11) 9999-9999",
  "empresa": "Empresa Teste",
  "departamento": "Teste",
  "assunto": "Assunto Teste",
  "descricao": "Descrição teste",
  "data": "01/04/2025",
  "hora": "17:00:00",
  "localizacao": "Teresina, PI",
  "latitude": -5.0892,
  "longitude": -42.8019,
  "foto": "data:image/jpeg;base64,SUA_FOTO_AQUI"
}
```

### Listar Formulários
- **Method:** GET
- **URL:** `http://localhost:5000/api/formulario/listar`

## 7. Download Manual de PDF

Se quiser acessar o PDF gerado:

```bash
# Listar arquivos
ls -la backend/uploads/

# Abrir PDF (macOS)
open backend/uploads/formulario_nome_20250401_170000.pdf

# Abrir PDF (Windows)
start backend\uploads\formulario_nome_20250401_170000.pdf

# Abrir PDF (Linux)
xdg-open backend/uploads/formulario_nome_20250401_170000.pdf
```

## 8. Testar Tratamento de Erros

### Erro: Falta de dados obrigatórios
```bash
curl -X POST http://localhost:5000/api/formulario/enviar \
  -H "Content-Type: application/json" \
  -d '{"nome": "Teste"}'
```

**Resposta esperada (400):**
```json
{
  "status": "erro",
  "message": "Nome e Email são obrigatórios"
}
```

### Erro: Falta de geolocalização
```bash
curl -X POST http://localhost:5000/api/formulario/enviar \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste",
    "email": "teste@email.com"
  }'
```

**Resposta esperada (400):**
```json
{
  "status": "erro",
  "message": "Localização é obrigatória"
}
```

---

## Documentação da API

### Campos do Formulário

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| nome | string | ✅ | Nome completo |
| email | string | ✅ | Email válido |
| telefone | string | ❌ | Telefone com formatação |
| empresa | string | ❌ | Nome da empresa |
| departamento | string | ❌ | Departamento |
| assunto | string | ❌ | Assunto do formulário |
| descricao | string | ❌ | Descrição detalhada |
| data | string | ✅ | Data no formato dd/mm/yyyy |
| hora | string | ✅ | Hora no formato hh:mm:ss |
| localizacao | string | ✅ | Nome da localização |
| latitude | float | ✅ | Latitude (-90 a 90) |
| longitude | float | ✅ | Longitude (-180 a 180) |
| foto | string (base64) | ✅ | Foto em base64 |
| campo1-campo15 | string | ❌ | Campos customizáveis |

### Status Codes

- `200` - OK, operação sucesso
- `400` - Bad Request, dados inválidos
- `404` - Not Found, rota não existe
- `500` - Internal Server Error, erro do servidor

---

**Pronto para testar! 🚀**
