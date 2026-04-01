import base64
import os
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import io
from datetime import datetime

def gerar_pdf(dados_formulario, foto_base64=None):
    """
    Gera um PDF completo com os dados do formulário, foto e mapa
    """
    try:
        # Criar arquivo PDF em memória
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # Estilos customizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=1  # Centro
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            spaceBefore=12,
            borderPadding=10,
            borderLineWidth=2,
            borderLineColor=colors.HexColor('#667eea')
        )

        # Título
        story.append(Paragraph("📋 FORMULÁRIO INTELIGENTE", title_style))
        story.append(Spacer(1, 0.3 * inch))

        # Seção de Informações Pessoais
        story.append(Paragraph("📝 Informações Pessoais", heading_style))
        
        dados_pessoais = [
            ['Campo', 'Informação'],
            ['Nome', dados_formulario.get('nome', 'N/A')],
            ['Email', dados_formulario.get('email', 'N/A')],
            ['Telefone', dados_formulario.get('telefone', 'N/A')],
            ['Empresa', dados_formulario.get('empresa', 'N/A')],
            ['Departamento', dados_formulario.get('departamento', 'N/A')],
        ]

        tabela_pessoal = Table(dados_pessoais, colWidths=[2*inch, 4.5*inch])
        tabela_pessoal.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#667eea')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))

        story.append(tabela_pessoal)
        story.append(Spacer(1, 0.3 * inch))

        # Seção de Localização e Data
        story.append(Paragraph("📍 Localização e Data/Hora", heading_style))

        dados_localizacao = [
            ['Campo', 'Informação'],
            ['Localização', dados_formulario.get('localizacao', 'N/A')],
            ['Latitude', str(dados_formulario.get('latitude', 'N/A'))],
            ['Longitude', str(dados_formulario.get('longitude', 'N/A'))],
            ['Data', dados_formulario.get('data', 'N/A')],
            ['Hora', dados_formulario.get('hora', 'N/A')],
        ]

        tabela_localizacao = Table(dados_localizacao, colWidths=[2*inch, 4.5*inch])
        tabela_localizacao.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#764ba2')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f8ff')]),
        ]))

        story.append(tabela_localizacao)
        story.append(Spacer(1, 0.3 * inch))

        # Seção de Assunto e Descrição
        story.append(Paragraph("📄 Assunto e Descrição", heading_style))

        dados_descritiva = [
            ['Campo', 'Informação'],
            ['Assunto', dados_formulario.get('assunto', 'N/A')],
            ['Descrição', dados_formulario.get('descricao', 'N/A')],
        ]

        tabela_descritiva = Table(dados_descritiva, colWidths=[2*inch, 4.5*inch])
        tabela_descritiva.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff9500')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ff9500')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fffacd')]),
        ]))

        story.append(tabela_descritiva)
        story.append(Spacer(1, 0.3 * inch))

        # Foto se fornecida
        if foto_base64:
            story.append(PageBreak())
            story.append(Paragraph("📸 Foto Capturada", heading_style))

            try:
                # Decodificar base64
                foto_data = base64.b64decode(foto_base64.split(',')[1])
                foto_img = Image.open(BytesIO(foto_data))

                # Redimensionar se necessário
                max_width = 6 * inch
                max_height = 4 * inch
                foto_img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                # Salvar temporariamente
                temp_foto_path = '/tmp/foto_formulario.png'
                foto_img.save(temp_foto_path)

                # Adicionar ao PDF
                img = RLImage(temp_foto_path, width=6*inch, height=4*inch)
                story.append(img)
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph(
                    "<i>Foto capturada com metadados de localização e data/hora</i>",
                    styles['Normal']
                ))

            except Exception as e:
                print(f"Erro ao processar foto: {str(e)}")
                story.append(Paragraph(f"[Foto não pôde ser processada: {str(e)}]", styles['Normal']))

        # Rodapé
        story.append(Spacer(1, 0.5 * inch))
        rodape_style = ParagraphStyle(
            'Rodape',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", rodape_style))
        story.append(Paragraph("© 2025 Formulário Inteligente - Todos os direitos reservados", rodape_style))

        # Construir PDF
        doc.build(story)

        # Retornar o PDF como bytes
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()

    except Exception as e:
        print(f"Erro ao gerar PDF: {str(e)}")
        raise


def gerar_pdf_manutencao(dados_manutencao):
    """
    Gera um PDF de 6 páginas para registro de manutenção Marvel
    Página 1: Dados básicos
    Página 2: UCP
    Página 3: TDM
    Página 4: Switch
    Página 5: Antena
    Página 6: Observações
    """
    try:
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # Estilos customizados
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=20,
            alignment=1
        )

        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=10,
            spaceBefore=10
        )

        # PÁGINA 1: DADOS BÁSICOS
        story.append(Paragraph("🔧 MANUTENÇÃO MARVEL - DADOS BÁSICOS", title_style))
        
        dados_basicos = [
            ['Campo', 'Informação'],
            ['Nome do Técnico', dados_manutencao.get('nome', 'N/A')],
            ['Data', dados_manutencao.get('data', 'N/A')],
            ['Hora', dados_manutencao.get('hora', 'N/A')],
            ['Garagem', dados_manutencao.get('garagem', 'N/A')],
            ['Prefixo', str(dados_manutencao.get('prefixo', 'N/A'))],
            ['ID', str(dados_manutencao.get('id', 'N/A'))],
            ['Tecnologia', dados_manutencao.get('tecnologia', 'N/A')],
            ['Localização', dados_manutencao.get('localizacao_completa', 'N/A')],
            ['Latitude', str(dados_manutencao.get('latitude', 'N/A'))],
            ['Longitude', str(dados_manutencao.get('longitude', 'N/A'))],
        ]

        tabela_basicos = Table(dados_basicos, colWidths=[2*inch, 4.5*inch])
        tabela_basicos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#667eea')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))

        story.append(tabela_basicos)
        story.append(PageBreak())

        # Função auxiliar para criar seções de equipamento
        def criar_secao_equipamento(nome, sigla, problemas_lista, foto_antes, actions_lista, foto_depois):
            story.append(Paragraph(f"⚙️ {nome} ({sigla})", title_style))
            
            # Problemas
            story.append(Paragraph("🔍 Problemas Detectados:", heading_style))
            if problemas_lista:
                for problema in problemas_lista:
                    story.append(Paragraph(f"• {problema}", styles['Normal']))
            else:
                story.append(Paragraph("Nenhum problema detectado", styles['Normal']))
            
            story.append(Spacer(1, 0.15 * inch))

            # Foto antes
            if foto_antes:
                story.append(Paragraph("📸 Foto Antes:", heading_style))
                try:
                    foto_data = base64.b64decode(foto_antes.split(',')[1])
                    foto_img = Image.open(BytesIO(foto_data))
                    foto_img.thumbnail((4*inch, 3*inch), Image.Resampling.LANCZOS)
                    temp_path = f'/tmp/foto_{sigla}_antes.png'
                    foto_img.save(temp_path)
                    img = RLImage(temp_path, width=4*inch, height=3*inch)
                    story.append(img)
                except:
                    story.append(Paragraph("[Foto antes não disponível]", styles['Normal']))
                
                story.append(Spacer(1, 0.15 * inch))

            # Ações
            story.append(Paragraph("🔧 Ações Realizadas:", heading_style))
            if actions_lista:
                for acao in actions_lista:
                    story.append(Paragraph(f"• {acao}", styles['Normal']))
            else:
                story.append(Paragraph("Nenhuma ação realizada", styles['Normal']))
            
            story.append(Spacer(1, 0.15 * inch))

            # Foto depois
            if foto_depois:
                story.append(Paragraph("📸 Foto Depois:", heading_style))
                try:
                    foto_data = base64.b64decode(foto_depois.split(',')[1])
                    foto_img = Image.open(BytesIO(foto_data))
                    foto_img.thumbnail((4*inch, 3*inch), Image.Resampling.LANCZOS)
                    temp_path = f'/tmp/foto_{sigla}_depois.png'
                    foto_img.save(temp_path)
                    img = RLImage(temp_path, width=4*inch, height=3*inch)
                    story.append(img)
                except:
                    story.append(Paragraph("[Foto depois não disponível]", styles['Normal']))
            
            story.append(PageBreak())

        # PÁGINA 2: UCP
        criar_secao_equipamento(
            "Unidade Central de Processamento",
            "UCP",
            dados_manutencao.get('ucp_problemas', []),
            dados_manutencao.get('ucp_foto_antes'),
            dados_manutencao.get('ucp_acoes', []),
            dados_manutencao.get('ucp_foto_depois')
        )

        # PÁGINA 3: TDM
        criar_secao_equipamento(
            "Terminal de Dados Móvel",
            "TDM",
            dados_manutencao.get('tdm_problemas', []),
            dados_manutencao.get('tdm_foto_antes'),
            dados_manutencao.get('tdm_acoes', []),
            dados_manutencao.get('tdm_foto_depois')
        )

        # PÁGINA 4: SWITCH
        criar_secao_equipamento(
            "Switch",
            "SW",
            dados_manutencao.get('switch_problemas', []),
            dados_manutencao.get('switch_foto_antes'),
            dados_manutencao.get('switch_acoes', []),
            dados_manutencao.get('switch_foto_depois')
        )

        # PÁGINA 5: ANTENA
        criar_secao_equipamento(
            "Antena GPS/GSM",
            "ANT",
            dados_manutencao.get('antena_problemas', []),
            dados_manutencao.get('antena_foto_antes'),
            dados_manutencao.get('antena_acoes', []),
            dados_manutencao.get('antena_foto_depois')
        )

        # PÁGINA 6: OBSERVAÇÕES
        story.append(Paragraph("📝 OBSERVAÇÕES E CONCLUSÕES", title_style))
        
        observacao = dados_manutencao.get('observacao', 'Nenhuma observação adicional')
        story.append(Paragraph(f"<b>Observações:</b><br/>{observacao}", styles['Normal']))
        
        story.append(Spacer(1, 0.3 * inch))

        # Imagens adicionais
        imagens_adicionais = dados_manutencao.get('imagens_adicionais', [])
        if imagens_adicionais:
            story.append(Paragraph("📸 Imagens Adicionais:", heading_style))
            for idx, imagem_path in enumerate(imagens_adicionais, 1):
                story.append(Paragraph(f"Imagem Adicional {idx}:", styles['Normal']))
                try:
                    if imagem_path.startswith('data:image'):
                        img_data = base64.b64decode(imagem_path.split(',')[1])
                        img = Image.open(BytesIO(img_data))
                    else:
                        img = Image.open(imagem_path)
                    
                    img.thumbnail((4*inch, 3*inch), Image.Resampling.LANCZOS)
                    temp_path = f'/tmp/imagem_adicional_{idx}.png'
                    img.save(temp_path)
                    rl_img = RLImage(temp_path, width=4*inch, height=3*inch)
                    story.append(rl_img)
                except:
                    story.append(Paragraph(f"[Imagem {idx} não disponível]", styles['Normal']))
                
                story.append(Spacer(1, 0.1 * inch))

        # Rodapé
        story.append(Spacer(1, 0.5 * inch))
        rodape_style = ParagraphStyle(
            'Rodape',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Paragraph(
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}<br/>" +
            "© 2025 Manutenção Marvel - Sistema de Controle de Frota",
            rodape_style
        ))

        # Construir PDF
        doc.build(story)

        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()

    except Exception as e:
        print(f"Erro ao gerar PDF de manutenção: {str(e)}")
        raise
