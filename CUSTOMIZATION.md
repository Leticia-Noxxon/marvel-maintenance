# ⚙️ Configuração de Campos do Formulário

Este arquivo explica como customizar os campos do formulário para suas necessidades específicas.

## 📝 Campos Disponíveis

### Campos Obrigatórios (Sistema)

Estes campos são automaticamente capturados pelo sistema:

```javascript
{
  nome: '',              // Nome completo
  email: '',             // Email para contato
  telefone: '',          // Telefone
  empresa: '',           // Empresa
  departamento: '',      // Departamento
  assunto: '',           // Assunto principal
  descricao: '',         // Descrição detalhada
  data: '',              // Data (automática)
  hora: '',              // Hora (automática)
  localizacao: '',       // Localização (automática)
  latitude: null,        // Latitude (automática)
  longitude: null,       // Longitude (automática)
  foto: null             // Foto capturada
}
```

### Campos Customizáveis (campo1 até campo15)

São 15 campos adicionais que você pode customizar conforme necessário:

```javascript
{
  campo1: '',
  campo2: '',
  campo3: '',
  campo4: '',
  campo5: '',
  campo6: '',
  campo7: '',
  campo8: '',
  campo9: '',
  campo10: '',
  campo11: '',
  campo12: '',
  campo13: '',
  campo14: '',
  campo15: ''
}
```

## 🔧 Como Adicionar/Customizar Campos

### 1. Adicionar Campo no Frontend

**Arquivo:** `frontend/src/components/FormularioComponent.js`

**Passo 1:** Adicione o campo no estado inicial:

```javascript
const [formData, setFormData] = useState({
  // ... campos existentes ...
  campo1: '',
  campo2: '',
  // ... adicione aqui ...
  seu_novo_campo: '',  // ← Adicione com nome descritivo
});
```

**Passo 2:** Adicione no formulário HTML:

```jsx
<div className="form-grupo">
  <label>Seu Novo Campo *</label>
  <input
    type="text"
    name="seu_novo_campo"
    value={formData.seu_novo_campo}
    onChange={handleInputChange}
    placeholder="Digite aqui"
    required
  />
</div>
```

**Passo 3:** Se for um campo especial (checkbox, select, textarea), adapte:

```jsx
// Para textarea
<textarea
  name="seu_novo_campo"
  value={formData.seu_novo_campo}
  onChange={handleInputChange}
  rows="5"
/>

// Para select
<select
  name="seu_novo_campo"
  value={formData.seu_novo_campo}
  onChange={handleInputChange}
>
  <option value="">Selecione uma opção</option>
  <option value="opcao1">Opção 1</option>
  <option value="opcao2">Opção 2</option>
</select>

// Para checkbox
<input
  type="checkbox"
  name="seu_novo_campo"
  checked={formData.seu_novo_campo}
  onChange={handleInputChange}
/>

// Para radio
<input
  type="radio"
  name="seu_novo_campo"
  value="opcao1"
  onChange={handleInputChange}
/>
```

**Passo 4:** Adicione o resumo (opcional):

```jsx
// Em FormularioComponent.js, na seção "resumo-dados"
<p><strong>Seu Novo Campo:</strong> {formData.seu_novo_campo}</p>
```

### 2. Atualizar PDF para incluir novo campo

**Arquivo:** `backend/utils/pdf_service.py`

Adicione na função `gerar_pdf()`:

```python
dados_customizados = [
    ['Campo', 'Informação'],
    ['Seu Novo Campo', dados_formulario.get('seu_novo_campo', 'N/A')],
]

tabela_custom = Table(dados_customizados, colWidths=[2*inch, 4.5*inch])
# ... estilo ...
story.append(tabela_custom)
```

### 3. Atualizar Email para incluir novo campo

**Arquivo:** `backend/utils/email_service.py`

Adicione na função `gerar_corpo_email()`:

```html
<div class="campo">
    <div class="label">Seu Novo Campo</div>
    <div class="valor">{dados_formulario.get('seu_novo_campo', 'N/A')}</div>
</div>
```

## 📋 Exemplos de Customizações

### Exemplo 1: Adicionar Campos de Endereço

```javascript
// No estado
endereço_rua: '',
endereço_numero: '',
endereço_bairro: '',
endereço_cidade: '',
endereço_estado: '',
endereço_cep: '',

// No formulário
<div className="form-grupo">
  <label>Rua</label>
  <input type="text" name="endereço_rua" ... />
</div>
<div className="form-grupo">
  <label>Número</label>
  <input type="text" name="endereço_numero" ... />
</div>
// ... etc
```

### Exemplo 2: Adicionar Campo de Categoria

```javascript
// No estado
categoria: '',

// No formulário HTML
<select name="categoria" value={formData.categoria} onChange={handleInputChange}>
  <option value="">Selecione uma categoria</option>
  <option value="vendas">Vendas</option>
  <option value="suporte">Suporte</option>
  <option value="financeiro">Financeiro</option>
  <option value="outros">Outros</option>
</select>
```

### Exemplo 3: Adicionar Campo de Prioridade

```javascript
// No estado
prioridade: '',

// Radio buttons
<label>
  <input
    type="radio"
    name="prioridade"
    value="baixa"
    onChange={handleInputChange}
  />
  Baixa
</label>
<label>
  <input
    type="radio"
    name="prioridade"
    value="media"
    onChange={handleInputChange}
  />
  Média
</label>
<label>
  <input
    type="radio"
    name="prioridade"
    value="alta"
    onChange={handleInputChange}
  />
  Alta
</label>
```

### Exemplo 4: Adicionar Checkbox de Termos

```javascript
// No estado
aceita_termos: false,
aceita_marketing: false,

// No formulário
<div className="form-grupo">
  <label>
    <input
      type="checkbox"
      name="aceita_termos"
      checked={formData.aceita_termos}
      onChange={handleInputChange}
    />
    Eu aceito os termos e condições *
  </label>
</div>
```

## 🎨 Styling de Campos

### Adicionar classe CSS customizada

```jsx
<div className="form-grupo form-grupo-destaque">
  <label>Campo em Destaque</label>
  <input type="text" name="... " />
</div>
```

```css
/* No FormularioComponent.css */
.form-grupo-destaque input {
  border-color: #ff9500;
  background: #fff9f0;
}

.form-grupo-destaque input:focus {
  border-color: #ff9500;
  background: #fffaf5;
}
```

## 🔄 Validação de Campos

### Adicionar validação customizada

```javascript
const validarFormulario = () => {
  if (!formData.seu_novo_campo) {
    setMensagem('❌ Campo obrigatório não preenchido');
    return false;
  }

  if (formData.seu_novo_campo.length < 5) {
    setMensagem('❌ Campo deve ter pelo menos 5 caracteres');
    return false;
  }

  return true;
};

// Usar na função handleEnviar
if (!validarFormulario()) return;
```

## 📊 Agrupar Campos em Seções

Para melhor organização, divida os campos em etapas:

```jsx
// etapa === 'basico'
// ... campos pessoais ...

// etapa === 'endereco'
// ... campos de endereço ...

// etapa === 'detalhes'
// ... campos específicos ...

// etapa === 'camera'
// ... já existe ...

// etapa === 'resumo'
// ... já existe ...
```

Atualize o navegador de etapas:

```jsx
<div className="etapas">
  <div className={`etapa-item ${etapa === 'basico' ? 'ativa' : ''}`}>
    <span>1</span>
    <span>Dados</span>
  </div>
  <div className={`etapa-item ${etapa === 'endereco' ? 'ativa' : ''}`}>
    <span>2</span>
    <span>Endereço</span>
  </div>
  <div className={`etapa-item ${etapa === 'detalhes' ? 'ativa' : ''}`}>
    <span>3</span>
    <span>Detalhes</span>
  </div>
  {/* ... resto ... */}
</div>
```

## 💾 Campos na API

Quando enviar para a API, todos os campos devem ir no JSON:

```json
{
  "nome": "...",
  "email": "...",
  "seu_novo_campo": "seu_valor",
  "outro_novo_campo": "outro_valor"
}
```

A API não valida campos customizados, apenas os obrigatórios (nome, email, localização, foto).

## 🔐 Campos Sensíveis

Para campos com dados sensíveis (senha, token, etc):

**NÃO RECOMENDÁVEL** adicionar ao formulário, mas se necessário:

```javascript
// Usar input type="password"
<input type="password" name="campo_sensivel" />

// E não enviar no email/PDF sem encriptação
```

## 🔍 Debugging

Para verificar quais campos estão sendo enviados:

```javascript
// No console do navegador
console.log(JSON.stringify(formData, null, 2));

// No backend (Python)
print(json.dumps(dados, indent=2, ensure_ascii=False))
```

---

## Tabela de Referência Rápida

| Tipo | Código | Exemplo |
|------|--------|---------|
| Texto | `<input type="text" />` | Nome, Email |
| Número | `<input type="number" />` | Idade, Quantidade |
| Email | `<input type="email" />` | Email |
| Telefone | `<input type="tel" />` | Telefone |
| Data | `<input type="date" />` | Data de nascimento |
| Hora | `<input type="time" />` | Horário |
| Textarea | `<textarea></textarea>` | Descrição longa |
| Select | `<select><option>...` | Categoria |
| Checkbox | `<input type="checkbox" />` | Aceitar termos |
| Radio | `<input type="radio" />` | Escolher opção |

---

**Pronto para customizar seus campos! 🎨️**
