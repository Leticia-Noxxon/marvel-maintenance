# Integração com Google Sheets - Instruções

## Setup Rápido com Google Apps Script

### Passo 1: Criar um Google Sheet
1. Acesse https://sheets.google.com
2. Crie uma nova planilha chamada "Manutenção Marvel - Registros"
3. **Copie o ID da planilha**:
   - URL tem este formato: `https://docs.google.com/spreadsheets/d/AQUI-ESTA-O-ID/edit`
   - Copie a parte entre `/d/` e `/edit` (tudo entre esses dois)
   - Salve este ID - você vai precisar no passo 2

4. Renomeie a primeira aba para "Registros" (clique com botão direito na aba inferior)

5. Adicione as seguintes colunas na primeira linha:
   - A: Data/Hora
   - B: Técnico
   - C: Prefixo
   - D: ID
   - E: Garagem
   - F: Tecnologia
   - G: Localização
   - H: UCP Problemas
   - I: UCP Ações
   - J: TDM Problemas
   - K: TDM Ações
   - L: Switch Problemas
   - M: Switch Ações
   - N: Antena Problemas
   - O: Antena Ações
   - P: Observações

### Passo 2: Criar Google Apps Script
1. Acesse https://script.google.com
2. Crie um novo projeto
3. Cole o código abaixo:

```javascript
// Substitua pela ID da sua planilha (copie do URL: /spreadsheets/d/AQUI)
const SPREADSHEET_ID = "SEU_SHEET_ID_AQUI";
const SHEET_NAME = "Registros"; // Nome da aba onde os dados serão salvos

function doPost(e) {
  try {
    // Validar entrada
    if (!e || !e.postData || !e.postData.contents) {
      return createResponse(400, 'erro', 'Dados inválidos ou vazios');
    }

    // Parse dos dados
    let data;
    try {
      data = JSON.parse(e.postData.contents);
    } catch (parseError) {
      Logger.log('Erro ao fazer parse: ' + parseError.toString());
      return createResponse(400, 'erro', 'JSON inválido');
    }

    // Validar campos obrigatórios
    if (!data.nome || !data.prefixo) {
      return createResponse(400, 'erro', 'Nome e Prefixo são obrigatórios');
    }

    // Abrir a planilha
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    let sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    // Se a aba não existe, criar
    if (!sheet) {
      sheet = spreadsheet.insertSheet(SHEET_NAME);
      // Adicionar cabeçalhos
      sheet.appendRow([
        'Data/Hora', 'Técnico', 'Prefixo', 'ID', 'Garagem', 'Tecnologia',
        'Localização', 'UCP Problemas', 'UCP Ações', 'TDM Problemas', 'TDM Ações',
        'Switch Problemas', 'Switch Ações', 'Antena Problemas', 'Antena Ações', 'Observações'
      ]);
    }

    // Preparar dados para inserção
    const newRow = [
      new Date().toLocaleString('pt-BR'),
      data.nome || '',
      data.prefixo || '',
      data.id || '',
      data.garagem || '',
      data.tecnologia || '',
      data.localizacao_completa || '',
      Array.isArray(data.ucp_problemas) ? data.ucp_problemas.join(', ') : '',
      Array.isArray(data.ucp_acoes) ? data.ucp_acoes.join(', ') : '',
      Array.isArray(data.tdm_problemas) ? data.tdm_problemas.join(', ') : '',
      Array.isArray(data.tdm_acoes) ? data.tdm_acoes.join(', ') : '',
      Array.isArray(data.switch_problemas) ? data.switch_problemas.join(', ') : '',
      Array.isArray(data.switch_acoes) ? data.switch_acoes.join(', ') : '',
      Array.isArray(data.antena_problemas) ? data.antena_problemas.join(', ') : '',
      Array.isArray(data.antena_acoes) ? data.antena_acoes.join(', ') : '',
      data.observacao || ''
    ];

    // Inserir nova linha
    sheet.appendRow(newRow);
    
    // Formatar a última linha (opcional - deixa com cor clara)
    const lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1, 1, newRow.length).setBackground('#f0f4f8');

    Logger.log('Dados inseridos com sucesso: ' + data.prefixo);

    return createResponse(200, 'sucesso', 'Registro salvo no Google Sheets com sucesso');

  } catch (error) {
    Logger.log('Erro no doPost: ' + error.toString());
    return createResponse(500, 'erro', 'Erro ao processar requisição: ' + error.toString());
  }
}

// Função auxiliar para criar respostas
function createResponse(statusCode, status, message) {
  const response = {
    code: statusCode,
    status: status,
    message: message,
    timestamp: new Date().toISOString()
  };
  
  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

// Função para testar o script (execute para debug)
function test() {
  const testData = {
    nome: 'Teste Técnico',
    prefixo: '1234',
    id: '12345',
    garagem: 'Garagem Centro',
    tecnologia: 'GPS',
    localizacao_completa: 'Rua das Flores, 100, Bairro Centro, São Paulo',
    ucp_problemas: ['Tela escura', 'Sem som'],
    ucp_acoes: ['Reinicializar', 'Verificar conexões'],
    tdm_problemas: [],
    tdm_acoes: [],
    switch_problemas: [],
    switch_acoes: [],
    antena_problemas: [],
    antena_acoes: [],
    observacao: 'Teste de funcionamento do script'
  };

  // Simular requisição POST
  const event = {
    postData: {
      contents: JSON.stringify(testData)
    }
  };

  const result = doPost(event);
  Logger.log('Resultado do teste: ' + result.getContent());
}
```

### Passo 3: Publicar o Script
1. No editor do Google Apps Script, clique em **"Deploy"** no canto superior direito
2. Clique em **"New deployment"** (ícone de + ao lado de Deploy)
3. Tipo de deployment: **"Web app"**
4. "Execute como": **Sua conta Google**
5. "Quem tem acesso": **"Anyone"** (Qualquer um)
6. Clique em **"Deploy"**
7. Você receberá um aviso de segurança - clique em "Review permissions" e autorize
8. **Copie a URL fornecida** (ela começa com https://script.google.com/macros/s/)

### Passo 4: Configurar no Backend
1. Abra o arquivo `.env` na pasta `c:\Marvel\backend`
2. Localize ou adicione a linha: `GOOGLE_SHEETS_WEBHOOK_URL=`
3. Cole a URL que você copiou do Deploy, ficando assim:
   ```
   GOOGLE_SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/SEU_ID/usercontent
   ```
4. **Salve o arquivo** (.env deve estar em `c:\Marvel\backend\.env`)
5. **Reinicie o backend** (pare com Ctrl+C e execute novamente)

### Passo 5: Testar (Opcional)
1. No Google Apps Script, clique em "Run" para executar a função `test()`
2. Você deve ver uma linha de teste adicionada ao seu Google Sheets
3. Se funcionar, o script está correto!

## Resultado
✅ Agora toda vez que um formulário é enviado:
- Os dados aparecem **automaticamente no seu Google Sheets**
- Data/hora são registradas automaticamente
- Você pode compartilhar o sheet com sua equipe
- Fácil de exportar como Excel ou PDF

---

## 🐛 Troubleshooting (Se algo não funcionar)

### Erro: "Valores inválidos" ou dados não aparecem no sheet

**Solução 1: Verificar o ID da Planilha**
- Você copiou o ID correto? (entre `/d/` e `/edit` no URL)
- Tente copiar novamente com cuidado
- Atualize no Google Apps Script:
  ```javascript
  const SPREADSHEET_ID = "COLE_O_ID_CORRETO_AQUI";
  ```
- Clique em "Deploy" → "Manage deployments" → atualize

**Solução 2: Verificar permissões**
- O script foi publicado como "Anyone" (Qualquer um)?
- Tente republicar: Deploy → Manage deployments → Edit → Deploy

**Solução 3: Ver logs de erro**
- No Google Apps Script, clique em "Executions" (ícone de cronômetro)
- Procure por erros em vermelho
- Clique em um erro para ver detalhes

**Solução 4: Testar o script**
1. No Google Apps Script, no final do código há uma função `test()`
2. Clique em "Run" e execute
3. Verifique se uma linha de teste aparece no Google Sheets
4. Se aparecer, a integração está funcionando!

### Erro: "401 Unauthorized" ou "403 Forbidden"

- A URL do webhook está correta no arquivo `.env`?
- Tente copiar a URL novamente diretamente do Deploy
- Republique o script

### Backend não reiniciou?

1. Abra o terminal em `c:\Marvel\backend`
2. Pressione `Ctrl + C` para parar
3. Execute `python main.py` novamente
4. Verifique se a mensagem mostra que está rodando

---

## 💡 Dicas Avançadas

### Adicionar mais colunas
Se quiser adicionar mais informações:
1. Adicione a coluna no Google Sheets
2. Atualize o script - adicione a coluna no array de `newRow`
3. Republique o Deploy

### Usar múltiplas planilhas
Para separar por garagem ou tecnologia:
1. Crie múltiplas abas no Google Sheets
2. No script, mude:
   ```javascript
   const SHEET_NAME = "Registros"; // Altere conforme necessário
   ```
3. Ou use esta linha para detectar automaticamente:
   ```javascript
   let sheet = spreadsheet.getSheetByName(data.garagem);
   ```

### Feedback visual
Compartilhe o Google Sheets com sua equipe:
1. Clique em "Compartilhar" (canto superior direito)
2. Adicione os emails da equipe
3. Todos verão os dados em tempo real!

---

**Está tudo funcionando?** 🎉 Seus formulários de manutenção agora estão salvos online e organizados!
