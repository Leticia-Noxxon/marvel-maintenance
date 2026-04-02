import os
import io
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from datetime import datetime

# ID da pasta compartilhada no Google Drive
GOOGLE_DRIVE_FOLDER_ID = "1Dj3_Av6NJOdRwC11cUqaudl57oyEhLIh"

# Permissões necessárias
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def autenticar_google():
    """
    Autentica com o Google Drive usando arquivo de credenciais
    """
    creds = None
    
    # Verificar se já existe token salvo
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Se não há credenciais válidas, fazer login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Nota: Você precisa baixar credentials.json do Google Cloud Console
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salvar credenciais para uso posterior
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def fazer_upload_imagem_para_drive(foto_base64, nome_arquivo=None):
    """
    Faz upload de uma imagem em base64 para o Google Drive
    Retorna a URL pública da imagem
    """
    try:
        # Autenticar
        creds = autenticar_google()
        service = build('drive', 'v3', credentials=creds)
        
        # Preparar nome do arquivo
        if not nome_arquivo:
            nome_arquivo = f"foto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        # Converter base64 para bytes
        if foto_base64.startswith('data:image'):
            foto_base64 = foto_base64.split(',')[1]
        
        foto_bytes = base64.b64decode(foto_base64)
        
        # Preparar arquivo para upload
        file_metadata = {
            'name': nome_arquivo,
            'parents': [GOOGLE_DRIVE_FOLDER_ID],
            'mimeType': 'image/jpeg'
        }
        
        # Fazer upload
        media = MediaIoBaseUpload(io.BytesIO(foto_bytes), mimetype='image/jpeg', resumable=True)
        arquivo = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink, webContentLink'
        ).execute()
        
        arquivo_id = arquivo.get('id')
        
        # Compartilhar arquivo (tornar público)
        service.permissions().create(
            fileId=arquivo_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        # Gerar URL pública para download
        url_publica = f"https://drive.google.com/uc?export=download&id={arquivo_id}"
        
        print(f"Upload bem-sucedido: {nome_arquivo} - {url_publica}")
        return url_publica
    
    except FileNotFoundError:
        print("AVISO: credentials.json não encontrado. Upload manual necessário.")
        return "PENDENTE_AUTENTICACAO"
    except HttpError as error:
        print(f'Erro no Google Drive: {error}')
        return None
    except Exception as e:
        print(f'Erro ao fazer upload: {str(e)}')
        return None

def fazer_upload_pdf_para_drive(caminho_pdf):
    """
    Faz upload de um PDF gerado para o Google Drive
    Retorna a URL pública
    """
    try:
        if not os.path.exists(caminho_pdf):
            print(f"Arquivo PDF não encontrado: {caminho_pdf}")
            return None
        
        creds = autenticar_google()
        service = build('drive', 'v3', credentials=creds)
        
        # Metadados do arquivo
        nome_arquivo = os.path.basename(caminho_pdf)
        file_metadata = {
            'name': nome_arquivo,
            'parents': [GOOGLE_DRIVE_FOLDER_ID],
            'mimeType': 'application/pdf'
        }
        
        # Upload
        media = MediaFileUpload(caminho_pdf, mimetype='application/pdf', resumable=True)
        arquivo = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        arquivo_id = arquivo.get('id')
        
        # Compartilhar (público)
        service.permissions().create(
            fileId=arquivo_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        # URL pública
        url_publica = f"https://drive.google.com/file/d/{arquivo_id}/view?usp=sharing"
        
        print(f"PDF uploadado: {nome_arquivo}")
        return url_publica
    
    except Exception as e:
        print(f'Erro ao upload PDF: {str(e)}')
        return None
