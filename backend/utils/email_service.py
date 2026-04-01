import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64

def enviar_email(destinatario, assunto, corpo_html, caminho_pdf_anexo=None, foto_em_base64=None):
    """
    Envia email com o formulário respondido e PDF anexado
    """
    try:
        # Configurar servidor SMTP (Gmail como exemplo)
        # Para usar com seu próprio servidor, ajuste as credenciais
        SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'seu_email@gmail.com')
        SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'sua_senha_app')
        SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

        # Criar mensagem
        msg = MIMEMultipart('alternative')
        msg['Subject'] = assunto
        msg['From'] = SENDER_EMAIL
        msg['To'] = destinatario

        # Corpo do email em HTML
        msg.attach(MIMEText(corpo_html, 'html'))

        # Anexar PDF se fornecido
        if caminho_pdf_anexo and os.path.exists(caminho_pdf_anexo):
            with open(caminho_pdf_anexo, 'rb') as anexo:
                parte = MIMEBase('application', 'octet-stream')
                parte.set_payload(anexo.read())
                encoders.encode_base64(parte)
                parte.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(caminho_pdf_anexo)}')
                msg.attach(parte)

        # Conectar ao servidor SMTP e enviar
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True, "Email enviado com sucesso"

    except Exception as e:
        print(f"Erro ao enviar email: {str(e)}")
        return False, f"Erro ao enviar email: {str(e)}"


def gerar_corpo_email(dados_formulario):
    """
    Gera o corpo do email em HTML com os dados do formulário
    """
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #f9f9f9; padding: 20px; border-radius: 8px; }}
            h2 {{ color: #667eea; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
            .secao {{ background: white; padding: 15px; margin: 15px 0; border-radius: 6px; border-left: 4px solid #667eea; }}
            .campo {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; font-size: 12px; text-transform: uppercase; }}
            .valor {{ color: #333; font-size: 14px; margin-top: 5px; }}
            .rodape {{ text-align: center; color: #999; font-size: 11px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📋 Novo Formulário Recebido</h2>

            <div class="secao">
                <h3 style="margin-top: 0; color: #333;">Informações Pessoais</h3>
                <div class="campo">
                    <div class="label">Nome</div>
                    <div class="valor">{dados_formulario.get('nome', 'N/A')}</div>
                </div>
                <div class="campo">
                    <div class="label">Email</div>
                    <div class="valor">{dados_formulario.get('email', 'N/A')}</div>
                </div>
                <div class="campo">
                    <div class="label">Telefone</div>
                    <div class="valor">{dados_formulario.get('telefone', 'N/A')}</div>
                </div>
                <div class="campo">
                    <div class="label">Empresa</div>
                    <div class="valor">{dados_formulario.get('empresa', 'N/A')}</div>
                </div>
            </div>

            <div class="secao">
                <h3 style="margin-top: 0; color: #333;">Informações de Localização e Data</h3>
                <div class="campo">
                    <div class="label">📍 Localização</div>
                    <div class="valor">{dados_formulario.get('localizacao', 'N/A')}</div>
                </div>
                <div class="campo">
                    <div class="label">🗺️ Coordenadas</div>
                    <div class="valor">Latitude: {dados_formulario.get('latitude', 'N/A')}, Longitude: {dados_formulario.get('longitude', 'N/A')}</div>
                </div>
                <div class="campo">
                    <div class="label">📅 Data</div>
                    <div class="valor">{dados_formulario.get('data', 'N/A')}</div>
                </div>
                <div class="campo">
                    <div class="label">🕐 Hora</div>
                    <div class="valor">{dados_formulario.get('hora', 'N/A')}</div>
                </div>
            </div>

            <div class="secao">
                <h3 style="margin-top: 0; color: #333;">Assunto e Descrição</h3>
                <div class="campo">
                    <div class="label">Assunto</div>
                    <div class="valor">{dados_formulario.get('assunto', 'N/A')}</div>
                </div>
                <div class="campo">
                    <div class="label">Descrição</div>
                    <div class="valor">{dados_formulario.get('descricao', 'N/A').replace(chr(10), '<br>')}</div>
                </div>
            </div>

            <div class="secao">
                <h3 style="margin-top: 0; color: #333;">📎 Anexos</h3>
                <p>Foto e PDF detalhado anexados neste email.</p>
            </div>

            <div class="rodape">
                <p>Este é um email automático. Por favor, não responda diretamente.</p>
                <p>© 2025 Formulário Inteligente</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def gerar_corpo_email_manutencao(dados_manutencao):
    """
    Gera o corpo do email em HTML para registro de manutenção Marvel
    """
    # Formatar listas de equipamentos
    def formatar_lista(items):
        if not items:
            return "Nenhum"
        return ", ".join(items) if isinstance(items, list) else str(items)

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 700px; margin: 0 auto; background: #f9f9f9; padding: 20px; border-radius: 8px; }}
            h2 {{ color: #667eea; border-bottom: 3px solid #667eea; padding-bottom: 10px; text-align: center; }}
            h3 {{ color: #764ba2; margin-top: 20px; margin-bottom: 10px; }}
            .secao {{ background: white; padding: 15px; margin: 15px 0; border-radius: 6px; border-left: 4px solid #667eea; }}
            .campo {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; font-size: 12px; text-transform: uppercase; }}
            .valor {{ color: #333; font-size: 14px; margin-top: 5px; }}
            .status-ok {{ color: #4caf50; font-weight: bold; }}
            .status-alerta {{ color: #ff9500; font-weight: bold; }}
            .status-critico {{ color: #f44336; font-weight: bold; }}
            .rodape {{ text-align: center; color: #999; font-size: 11px; margin-top: 20px; }}
            .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔧 Registro de Manutenção Marvel</h2>

            <div class="secao">
                <h3>📋 Dados da Manutenção</h3>
                <div class="grid-2">
                    <div class="campo">
                        <div class="label">Técnico</div>
                        <div class="valor">{dados_manutencao.get('nome', 'N/A')}</div>
                    </div>
                    <div class="campo">
                        <div class="label">Data/Hora</div>
                        <div class="valor">{dados_manutencao.get('data', 'N/A')} - {dados_manutencao.get('hora', 'N/A')}</div>
                    </div>
                    <div class="campo">
                        <div class="label">Prefixo (Ônibus)</div>
                        <div class="valor">{dados_manutencao.get('prefixo', 'N/A')}</div>
                    </div>
                    <div class="campo">
                        <div class="label">ID</div>
                        <div class="valor">{dados_manutencao.get('id', 'N/A')}</div>
                    </div>
                    <div class="campo">
                        <div class="label">Garagem</div>
                        <div class="valor">{dados_manutencao.get('garagem', 'N/A')}</div>
                    </div>
                    <div class="campo">
                        <div class="label">Tecnologia</div>
                        <div class="valor">{dados_manutencao.get('tecnologia', 'N/A')}</div>
                    </div>
                </div>
                <div class="campo" style="margin-top: 15px;">
                    <div class="label">📍 Localização</div>
                    <div class="valor">{dados_manutencao.get('localizacao_completa', 'N/A')}</div>
                </div>
            </div>

            <div class="secao">
                <h3>⚙️ Status dos Equipamentos</h3>
                
                <h4 style="color: #333; margin-top: 10px;">🔹 UCP (Unidade Central de Processamento)</h4>
                <div class="campo">
                    <div class="label">Problemas Detectados</div>
                    <div class="valor" style="color: 
                    {'#f44336' if dados_manutencao.get('ucp_problemas') else '#4caf50'};">
                        {formatar_lista(dados_manutencao.get('ucp_problemas', []))}
                    </div>
                </div>
                <div class="campo">
                    <div class="label">Ações Realizadas</div>
                    <div class="valor">{formatar_lista(dados_manutencao.get('ucp_acoes', []))}</div>
                </div>

                <h4 style="color: #333; margin-top: 10px;">🔹 TDM (Terminal de Dados Móvel)</h4>
                <div class="campo">
                    <div class="label">Problemas Detectados</div>
                    <div class="valor" style="color: 
                    {'#f44336' if dados_manutencao.get('tdm_problemas') else '#4caf50'};">
                        {formatar_lista(dados_manutencao.get('tdm_problemas', []))}
                    </div>
                </div>
                <div class="campo">
                    <div class="label">Ações Realizadas</div>
                    <div class="valor">{formatar_lista(dados_manutencao.get('tdm_acoes', []))}</div>
                </div>

                <h4 style="color: #333; margin-top: 10px;">🔹 Switch</h4>
                <div class="campo">
                    <div class="label">Problemas Detectados</div>
                    <div class="valor" style="color: 
                    {'#f44336' if dados_manutencao.get('switch_problemas') else '#4caf50'};">
                        {formatar_lista(dados_manutencao.get('switch_problemas', []))}
                    </div>
                </div>
                <div class="campo">
                    <div class="label">Ações Realizadas</div>
                    <div class="valor">{formatar_lista(dados_manutencao.get('switch_acoes', []))}</div>
                </div>

                <h4 style="color: #333; margin-top: 10px;">🔹 Antena (GPS/GSM)</h4>
                <div class="campo">
                    <div class="label">Problemas Detectados</div>
                    <div class="valor" style="color: 
                    {'#f44336' if dados_manutencao.get('antena_problemas') else '#4caf50'};">
                        {formatar_lista(dados_manutencao.get('antena_problemas', []))}
                    </div>
                </div>
                <div class="campo">
                    <div class="label">Ações Realizadas</div>
                    <div class="valor">{formatar_lista(dados_manutencao.get('antena_acoes', []))}</div>
                </div>
            </div>

            <div class="secao">
                <h3>📝 Observações</h3>
                <div class="campo">
                    <div class="valor">{dados_manutencao.get('observacao', 'Nenhuma observação adicional').replace(chr(10), '<br>')}</div>
                </div>
            </div>

            <div class="secao">
                <h3>📎 Documentação</h3>
                <p>Foto da frente do ônibus, fotos de equipamentos e PDF detalhado com 6 páginas de inspeção anexados.</p>
            </div>

            <div class="rodape">
                <p>Este é um email automático. Por favor, não responda diretamente.</p>
                <p>© 2025 Sistema de Manutenção Marvel - Controle de Frota</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html
