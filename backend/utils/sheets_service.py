import requests
import os
from datetime import datetime

def enviar_para_google_sheets(dados_manutencao):
    """
    Envia dados de manutenção para Google Sheets via webhook
    """
    try:
        webhook_url = os.getenv('GOOGLE_SHEETS_WEBHOOK_URL')
        
        if not webhook_url:
            print("⚠️ GOOGLE_SHEETS_WEBHOOK_URL não configurada. Pulando envio para Google Sheets.")
            return True, "Google Sheets não configurado (opcional)"
        
        # Preparar dados para o Google Sheets
        dados_sheet = {
            'data_hora': datetime.now().isoformat(),
            'nome': dados_manutencao.get('nome', ''),
            'prefixo': dados_manutencao.get('prefixo', ''),
            'id': dados_manutencao.get('id', ''),
            'garagem': dados_manutencao.get('garagem', ''),
            'tecnologia': dados_manutencao.get('tecnologia', ''),
            'localizacao_completa': dados_manutencao.get('localizacao_completa', ''),
            'latitude': dados_manutencao.get('latitude', ''),
            'longitude': dados_manutencao.get('longitude', ''),
            'ucp_problemas': ', '.join(dados_manutencao.get('ucp_problemas', [])),
            'ucp_acoes': ', '.join(dados_manutencao.get('ucp_acoes', [])),
            'tdm_problemas': ', '.join(dados_manutencao.get('tdm_problemas', [])),
            'tdm_acoes': ', '.join(dados_manutencao.get('tdm_acoes', [])),
            'switch_problemas': ', '.join(dados_manutencao.get('switch_problemas', [])),
            'switch_acoes': ', '.join(dados_manutencao.get('switch_acoes', [])),
            'antena_problemas': ', '.join(dados_manutencao.get('antena_problemas', [])),
            'antena_acoes': ', '.join(dados_manutencao.get('antena_acoes', [])),
            'observacao': dados_manutencao.get('observacao', '')
        }
        
        # Enviar para Google Sheets
        response = requests.post(webhook_url, json=dados_sheet, timeout=10)
        
        if response.status_code == 200:
            print("✅ Dados enviados para Google Sheets com sucesso")
            return True, "Dados salvos no Google Sheets"
        else:
            print(f"⚠️ Erro ao enviar para Google Sheets: {response.status_code}")
            return True, "Dados salvos no servidor (Google Sheets indisponível)"
    
    except requests.exceptions.Timeout:
        print("⚠️ Timeout ao conectar com Google Sheets")
        return True, "Dados salvos no servidor"
    except Exception as e:
        print(f"⚠️ Erro ao enviar para Google Sheets: {str(e)}")
        return True, "Dados salvos no servidor"
