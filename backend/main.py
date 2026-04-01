from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime
import base64

# Importar serviços
from utils.email_service import enviar_email, gerar_corpo_email, gerar_corpo_email_manutencao
from utils.pdf_service import gerar_pdf, gerar_pdf_manutencao
from utils.sheets_service import enviar_para_google_sheets
from utils.excel_service import atualizar_excel_manutencoes

# Carregar variáveis de ambiente
load_dotenv()

# Configurar pasta estática do React build (para produção)
frontend_build_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')
app = Flask(__name__, static_folder=frontend_build_path, static_url_path='')
CORS(app)

# Configurações
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
PASTA_UPLOADS = os.getenv('PASTA_UPLOADS', 'uploads')

# Criar pasta de uploads se não existir
os.makedirs(PASTA_UPLOADS, exist_ok=True)


@app.route('/api/health', methods=['GET'])
def health():
    """Verificar se a API está funcionando"""
    return jsonify({
        'status': 'ok',
        'message': 'API de Formulário está rodando',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/formulario/enviar', methods=['POST'])
def enviar_formulario():
    """
    Recebe os dados do formulário, gera PDF e envia por email
    """
    try:
        dados = request.get_json()

        # Validar dados essenciais
        if not dados.get('nome') or not dados.get('email'):
            return jsonify({
                'status': 'erro',
                'message': 'Nome e Email são obrigatórios'
            }), 400

        if not dados.get('latitude') or not dados.get('longitude'):
            return jsonify({
                'status': 'erro',
                'message': 'Localização é obrigatória'
            }), 400

        if not dados.get('foto'):
            return jsonify({
                'status': 'erro',
                'message': 'Foto é obrigatória'
            }), 400

        # Gerar PDF
        try:
            pdf_bytes = gerar_pdf(dados, dados.get('foto'))

            # Salvar PDF localmente
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_pdf = f"formulario_{dados['nome'].replace(' ', '_')}_{timestamp}.pdf"
            caminho_pdf = os.path.join(PASTA_UPLOADS, nome_pdf)

            with open(caminho_pdf, 'wb') as f:
                f.write(pdf_bytes)

        except Exception as e:
            print(f"Erro ao gerar PDF: {str(e)}")
            return jsonify({
                'status': 'erro',
                'message': f'Erro ao gerar PDF: {str(e)}'
            }), 500

        # Gerar corpo do email
        corpo_html = gerar_corpo_email(dados)

        # Enviar email
        sucesso, mensagem = enviar_email(
            destinatario=dados['email'],
            assunto=f"Confirmação de Formulário - {dados.get('assunto', 'Sem assunto')}",
            corpo_html=corpo_html,
            caminho_pdf_anexo=caminho_pdf,
            foto_em_base64=dados.get('foto')
        )

        if sucesso:
            return jsonify({
                'status': 'sucesso',
                'message': 'Formulário enviado com sucesso!',
                'pdf_name': nome_pdf,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'erro',
                'message': mensagem
            }), 500

    except Exception as e:
        print(f"Erro na API: {str(e)}")
        return jsonify({
            'status': 'erro',
            'message': f'Erro ao processar formulário: {str(e)}'
        }), 500


@app.route('/api/formulario/listar', methods=['GET'])
def listar_formularios():
    """
    Lista todos os PDFs gerados
    """
    try:
        formularios = []

        if os.path.exists(PASTA_UPLOADS):
            for arquivo in os.listdir(PASTA_UPLOADS):
                if arquivo.endswith('.pdf'):
                    caminho_completo = os.path.join(PASTA_UPLOADS, arquivo)
                    tamanho = os.path.getsize(caminho_completo)
                    data_criacao = datetime.fromtimestamp(
                        os.path.getctime(caminho_completo)
                    ).isoformat()

                    formularios.append({
                        'nome': arquivo,
                        'tamanho': f"{tamanho / 1024:.2f} KB",
                        'data_criacao': data_criacao
                    })

        return jsonify({
            'status': 'sucesso',
            'total': len(formularios),
            'formularios': formularios
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'erro',
            'message': f'Erro ao listar formulários: {str(e)}'
        }), 500


@app.route('/api/download-excel', methods=['GET'])
def download_excel():
    """
    Baixa o arquivo Excel com todas as manutenções
    """
    try:
        arquivo_excel = os.path.join(PASTA_UPLOADS, 'Manutenções_Marvel.xlsx')
        
        if not os.path.exists(arquivo_excel):
            return jsonify({
                'status': 'erro',
                'message': 'Arquivo Excel não encontrado. Nenhum formulário foi enviado ainda.'
            }), 404
        
        return send_file(
            arquivo_excel,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Manutenções_Marvel.xlsx'
        )
    
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'message': f'Erro ao baixar Excel: {str(e)}'
        }), 500


# ROTAS DO FRONTEND (React) - Servir em produção
@app.route('/')
def serve_index():
    """Servir página principal do React"""
    index_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(app.static_folder, 'index.html')
    return jsonify({'status': 'erro', 'message': 'Frontend não configurado'}), 404


@app.route('/<path:path>')
def serve_static(path):
    """Servir arquivos estáticos ou retornar index.html para React Router"""
    filepath = os.path.join(app.static_folder, path)
    
    # Se é um arquivo estático, servir
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return send_from_directory(app.static_folder, path)
    
    # Se não é API, retornar index.html para React Router
    if not path.startswith('api'):
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
    
    # Caso contrário, retornar 404
    return jsonify({
        'status': 'erro',
        'message': 'Rota não encontrada'
    }), 404


@app.errorhandler(404)
def not_found(error):
    """Tentar servir index.html, ou retornar erro JSON"""
    index_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(app.static_folder, 'index.html')
    return jsonify({
        'status': 'erro',
        'message': 'Rota não encontrada'
    }), 404


@app.route('/api/manutencao/enviar', methods=['POST'])
def enviar_manutencao():
    """
    Recebe dados da manutenção Marvel e envia por email com PDF
    """
    try:
        dados = request.get_json()

        # VALIDAÇÃO PÁGINA 1 - DADOS (OBRIGATÓRIA)
        campos_obrigatorios = [
            'nome', 'data', 'hora', 'garagem', 'prefixo', 'id', 
            'tecnologia', 'foto_frente_onibus', 'latitude', 'longitude', 
            'localizacao_completa'
        ]

        erros = []
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                erros.append(f"Campo obrigatório faltando: {campo}")

        if erros:
            return jsonify({
                'status': 'erro',
                'message': 'Página 1 (Dados) incompleta',
                'detalhes': erros
            }), 400

        # VALIDAÇÃO CONDICIONAL - Se problemas foram detectados, foto é obrigatória
        validacoes_equipamentos = [
            ('ucp', 'ucp_problemas', 'ucp_foto_antes'),
            ('tdm', 'tdm_problemas', 'tdm_foto_antes'),
            ('switch', 'switch_problemas', 'switch_foto_antes'),
            ('antena', 'antena_problemas', 'antena_foto_antes'),
        ]

        erros_equipamentos = []
        for nome_eq, campo_problemas, campo_foto in validacoes_equipamentos:
            problemas = dados.get(campo_problemas, [])
            if isinstance(problemas, list) and len(problemas) > 0:
                if not dados.get(campo_foto):
                    erros_equipamentos.append(
                        f"{nome_eq.upper()}: Se há problemas detectados, "
                        f"foto 'antes' é obrigatória"
                    )

        if erros_equipamentos:
            return jsonify({
                'status': 'erro',
                'message': 'Validação condicional falhou',
                'detalhes': erros_equipamentos
            }), 400

        # Gerar PDF (6 páginas)
        try:
            pdf_bytes = gerar_pdf_manutencao(dados)

            # Salvar PDF localmente
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_pdf = f"manutencao_{dados['prefixo']}_{timestamp}.pdf"
            caminho_pdf = os.path.join(PASTA_UPLOADS, nome_pdf)

            with open(caminho_pdf, 'wb') as f:
                f.write(pdf_bytes)

        except Exception as e:
            print(f"Erro ao gerar PDF de manutenção: {str(e)}")
            return jsonify({
                'status': 'erro',
                'message': f'Erro ao gerar PDF: {str(e)}'
            }), 500

        # Gerar corpo do email adaptado para manutenção
        corpo_html = gerar_corpo_email_manutencao(dados)

        # Enviar email
        sucesso, mensagem = enviar_email(
            destinatario=dados.get('email', os.getenv('EMAIL_DESTINO')),
            assunto=f"Manutenção Marvel - Prefixo {dados['prefixo']} - {dados['data']}",
            corpo_html=corpo_html,
            caminho_pdf_anexo=caminho_pdf,
            foto_em_base64=dados.get('foto_frente_onibus')
        )

        # Atualizar Excel com todos os registros (sempre, independente do email)
        try:
            atualizar_excel_manutencoes(dados)
        except Exception as e:
            print(f"Aviso: Erro ao atualizar Excel: {str(e)}")
        
        # Enviar dados para Google Sheets (não bloqueia se falhar)
        try:
            if sucesso:
                enviar_para_google_sheets(dados)
        except Exception as e:
            print(f"Aviso: Erro ao enviar para Google Sheets: {str(e)}")

        # Retornar resposta (sucesso mesmo que o email tenha falhado)
        return jsonify({
            'status': 'sucesso',
            'message': 'Manutenção registrada com sucesso!' if sucesso else 'Manutenção registrada (erro ao enviar email)',
            'pdf_name': nome_pdf,
            'excel_name': 'Manutenções_Marvel.xlsx',
            'email_enviado': sucesso,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        print(f"Erro na API de manutenção: {str(e)}")
        return jsonify({
            'status': 'erro',
            'message': f'Erro ao processar manutenção: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'erro',
        'message': 'Rota não encontrada'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'erro',
        'message': 'Erro interno do servidor'
    }), 500


if __name__ == '__main__':
    # Modo desenvolvimento
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
