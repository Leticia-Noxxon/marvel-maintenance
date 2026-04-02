import React, { useState, useEffect, useRef } from 'react';
import CameraComponent from './CameraComponent';
import ImageUploadButton from './ImageUploadButton';
import GeolocationComponent from './GeolocationComponent';
import MapComponent from './MapComponent';
import axios from 'axios';
import { API_ENDPOINTS } from '../config/api';
import './FormularioComponent.css';

const FormularioComponent = () => {
  const [etapa, setEtapa] = useState('dados');

  const [formData, setFormData] = useState({
    // Página 1 - Dados
    nome: '',
    data: '',
    hora: '',
    garagem: '',
    prefixo: '',
    id: '',
    tecnologia: '',
    foto_frente_onibus: null,
    localizacao_completa: '',
    latitude: null,
    longitude: null,

    // Página 2 - UCP
    ucp_problemas: [],
    ucp_foto_antes: null,
    ucp_acoes: [],
    ucp_foto_depois: null,

    // Página 3 - TDM
    tdm_problemas: [],
    tdm_foto_antes: null,
    tdm_acoes: [],
    tdm_foto_depois: null,

    // Página 4 - Switch
    switch_problemas: [],
    switch_foto_antes: null,
    switch_acoes: [],
    switch_foto_depois: null,

    // Página 5 - Antena
    antena_problemas: [],
    antena_foto_antes: null,
    antena_acoes: [],
    antena_foto_depois: null,

    // Página 6 - Observação
    observacao: '',
    imagens_adicionais: []
  });

  const [enviando, setEnviando] = useState(false);
  const [mensagem, setMensagem] = useState('');
  const [autoSalvo, setAutoSalvo] = useState(false);
  const [paginaAtiva, setPaginaAtiva] = useState(0);

  const garagens = [
    'Viação Metrópole AE Carvalho',
    'Viação Metrópole DePinedo',
    'Viação Metrópole Expandir',
    'Viação Metrópole Iguatemi',
    'Viação Metrópole Imperador',
    'Viação Metrópole Itaim',
    'Viação Metrópole M\'Boi'
  ];

  const tecnologias = ['Articulado', 'Básico', 'Midi', 'Mini', 'Padrão'];

  const ucpProblemas = [
    'UCP com GPS/GSM travado',
    'UCP sem comunicação',
    'Não inverte TP/TS',
    'UCP com cabeamento danificado ou solto',
    'UCP Instalada Incorretamente',
    'UCP não fixada corretamente',
    'Nenhum problema identificado'
  ];

  const ucpAcoes = [
    'Substituição de UCP',
    'Correção da Instalação da UCP',
    'Fixação da UCP',
    'Nenhuma ação realizada'
  ];

  const tdmProblemas = [
    'TDM apagado',
    'Erro de conexão com a UCP',
    'TDM não fixado corretamente',
    'TDM instalado incorretamente',
    'Cabos do TDM soltos ou desencaixados',
    'Nenhuma anomalia encontrada'
  ];

  const tdmAcoes = [
    'Substituição de TDM',
    'Correção da Instalação do TDM',
    'Fixação do TDM',
    'Correção e fixação dos cabos do TDM',
    'Nenhuma ação realizada'
  ];

  const switchProblemas = [
    'Falha no switch',
    'Tampa do switch desprendida',
    'Switch instalado incorretamente',
    'Nenhuma anomalia encontrada'
  ];

  const switchAcoes = [
    'Correção da Instalação do switch',
    'Substituição do switch',
    'Fixação do switch',
    'Nenhuma ação realizada'
  ];

  const antenaProblemas = [
    'Antena GPS solta ou mal posicionada',
    'Antena GPS inoperante',
    'Antena GSM solta ou mal posicionada',
    'Antena GSM inoperante',
    'Nenhuma anomalia encontrada'
  ];

  const antenaAcoes = [
    'Substituição da antena GPS',
    'Substituição da antena GSM',
    'Instalação da antena GPS',
    'Reposicionamento da antena GPS',
    'Nenhuma ação realizada'
  ];

  // Auto-salvar
  useEffect(() => {
    const interval = setInterval(() => {
      localStorage.setItem('manutencaoMarvel', JSON.stringify(formData));
      setAutoSalvo(true);
      setTimeout(() => setAutoSalvo(false), 2000);
    }, 30000);

    return () => clearInterval(interval);
  }, [formData]);

  // Carregar do localStorage
  useEffect(() => {
    const salvos = localStorage.getItem('manutencaoMarvel');
    if (salvos) {
      setFormData(JSON.parse(salvos));
    }

    // Atualizar data e hora
    const agora = new Date();
    setFormData(prev => ({
      ...prev,
      data: agora.toLocaleDateString('pt-BR'),
      hora: agora.toLocaleTimeString('pt-BR')
    }));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (field, option) => {
    setFormData(prev => {
      const arr = prev[field];
      if (arr.includes(option)) {
        return {
          ...prev,
          [field]: arr.filter(item => item !== option)
        };
      } else {
        return {
          ...prev,
          [field]: [...arr, option]
        };
      }
    });
  };

  const handleGeolocation = (geoData) => {
    setFormData(prev => ({
      ...prev,
      localizacao_completa: geoData.localizacao_completa || geoData.localizacao,
      latitude: geoData.latitude,
      longitude: geoData.longitude
    }));
  };

  const handleFoto = (fotoData, campo) => {
    setFormData(prev => ({
      ...prev,
      [campo]: fotoData
    }));
  };

  const handleImagemAdicional = (e) => {
    const files = Array.from(e.target.files);
    const reader = new FileReader();
    
    reader.onload = (event) => {
      setFormData(prev => ({
        ...prev,
        imagens_adicionais: [...prev.imagens_adicionais, event.target.result]
      }));
    };

    if (files.length > 0) {
      reader.readAsDataURL(files[0]);
    }
  };

  const validarPagina1 = () => {
    if (!formData.nome) return 'Nome é obrigatório';
    if (!formData.garagem) return 'Garagem é obrigatória';
    if (!formData.prefixo || formData.prefixo.length < 4) return 'Prefixo deve ter 4-5 dígitos';
    if (!formData.id || formData.id.length !== 5) return 'ID deve ter 5 dígitos';
    if (!formData.tecnologia) return 'Tecnologia é obrigatória';
    if (!formData.foto_frente_onibus) return 'Foto da frente do ônibus é obrigatória';
    if (!formData.latitude || !formData.longitude) return 'Localização é obrigatória';
    return null;
  };

  const validarEnvio = () => {
    const erro = validarPagina1();
    if (erro) {
      setMensagem('❌ ' + erro);
      setEtapa('dados');
      return false;
    }

    // Validar páginas com seleções
    const paginas = [
      { key: 'ucp', problemas: formData.ucp_problemas, foto_antes: formData.ucp_foto_antes },
      { key: 'tdm', problemas: formData.tdm_problemas, foto_antes: formData.tdm_foto_antes },
      { key: 'switch', problemas: formData.switch_problemas, foto_antes: formData.switch_foto_antes },
      { key: 'antena', problemas: formData.antena_problemas, foto_antes: formData.antena_foto_antes }
    ];

    for (const pagina of paginas) {
      if (pagina.problemas.length > 0 && !pagina.foto_antes) {
        setMensagem(`❌ Foto obrigatória para ${pagina.key.toUpperCase()} (tem problema(s) selecionado(s))`);
        return false;
      }
    }

    return true;
  };

  const handleSalvar = () => {
    localStorage.setItem('manutencaoMarvel', JSON.stringify(formData));
    setMensagem('✅ Dados salvos localmente com sucesso!');
    setTimeout(() => setMensagem(''), 3000);
  };

  const handleEnviar = async () => {
    if (!validarEnvio()) return;

    setEnviando(true);
    setMensagem('📤 Enviando formulário...');

    try {
      const response = await axios.post(API_ENDPOINTS.ENVIAR_MANUTENCAO, formData);

      if (response.status === 200) {
        setMensagem('✅ Formulário enviado com sucesso!');
        localStorage.removeItem('manutencaoMarvel');
        setFormData({
          nome: '',
          data: new Date().toLocaleDateString('pt-BR'),
          hora: new Date().toLocaleTimeString('pt-BR'),
          garagem: '',
          prefixo: '',
          id: '',
          tecnologia: '',
          foto_frente_onibus: null,
          localizacao_completa: '',
          latitude: null,
          longitude: null,
          ucp_problemas: [],
          ucp_foto_antes: null,
          ucp_acoes: [],
          ucp_foto_depois: null,
          tdm_problemas: [],
          tdm_foto_antes: null,
          tdm_acoes: [],
          tdm_foto_depois: null,
          switch_problemas: [],
          switch_foto_antes: null,
          switch_acoes: [],
          switch_foto_depois: null,
          antena_problemas: [],
          antena_foto_antes: null,
          antena_acoes: [],
          antena_foto_depois: null,
          observacao: '',
          imagens_adicionais: []
        });
        setEtapa('dados');
      }
    } catch (error) {
      console.error('Erro ao enviar:', error);
      setMensagem(`❌ Erro ao enviar: ${error.message}`);
    } finally {
      setEnviando(false);
    }
  };

  const paginas = ['dados', 'ucp', 'tdm', 'switch', 'antena', 'observacao'];
  const nomesPaginas = ['Dados', 'UCP', 'TDM', 'Switch', 'Antena', 'Observação'];

  return (
    <div className="formulario-container">
      <div className="formulario-card">
        {/* Navegação entre páginas */}
        <div className="etapas">
          {nomesPaginas.map((nome, idx) => (
            <button
              key={idx}
              className={`etapa-item ${etapa === paginas[idx] ? 'ativa' : ''}`}
              onClick={() => setEtapa(paginas[idx])}
            >
              <span className="etapa-numero">{idx + 1}</span>
              <span className="etapa-label">{nome}</span>
            </button>
          ))}
        </div>

        {/* PÁGINA 1: DADOS */}
        {etapa === 'dados' && (
          <div className="etapa-conteudo">
            <h2>Manutenção Marvel</h2>

            <div className="form-grupo">
              <label>Nome do Técnico *</label>
              <input
                type="text"
                name="nome"
                value={formData.nome}
                onChange={handleInputChange}
                placeholder="Seu nome completo"
              />
            </div>

            <div className="form-grupo-linha">
              <div className="form-grupo">
                <label>Data *</label>
                <input type="text" value={formData.data} disabled />
              </div>
              <div className="form-grupo">
                <label>Hora *</label>
                <input type="text" value={formData.hora} disabled />
              </div>
            </div>

            <div className="form-grupo">
              <label>Garagem *</label>
              <select
                name="garagem"
                value={formData.garagem}
                onChange={handleInputChange}
              >
                <option value="">Selecione a garagem</option>
                {garagens.map(g => (
                  <option key={g} value={g}>{g}</option>
                ))}
              </select>
            </div>

            <div className="form-grupo-linha">
              <div className="form-grupo">
                <label>Prefixo *</label>
                <input
                  type="number"
                  name="prefixo"
                  value={formData.prefixo}
                  onChange={handleInputChange}
                  placeholder="Ex: 1234"
                />
              </div>
              <div className="form-grupo">
                <label>ID *</label>
                <input
                  type="number"
                  name="id"
                  value={formData.id}
                  onChange={handleInputChange}
                  placeholder="Ex: 12345"
                />
              </div>
            </div>

            <div className="form-grupo">
              <label>Tecnologia *</label>
              <select
                name="tecnologia"
                value={formData.tecnologia}
                onChange={handleInputChange}
              >
                <option value="">Selecione a tecnologia</option>
                {tecnologias.map(t => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>

            <div className="form-grupo">
              <label>Foto da Frente do Ônibus *</label>
              <ImageUploadButton 
                onFoto={(foto) => handleFoto(foto, 'foto_frente_onibus')} 
                geolocation={formData}
                label="Enviar Imagem"
              />
            </div>

            <GeolocationComponent onGeolocation={handleGeolocation} />

            {formData.latitude && formData.longitude && (
              <div className="info-localizado">
                <p>Localização: {formData.localizacao_completa}</p>
              </div>
            )}

            <div className="form-grupo botoes-grupo">
              <button 
                type="button" 
                className="btn btn-proximo"
                onClick={() => {
                  const erro = validarPagina1();
                  if (erro) {
                    setMensagem('❌ ' + erro);
                  } else {
                    setEtapa('ucp');
                  }
                }}
              >
                Próximo
              </button>
            </div>

            {autoSalvo && <p className="auto-salvo">Auto-salvo ✓</p>}
          </div>
        )}

        {/* PÁGINA 2: UCP */}
        {etapa === 'ucp' && (
          <div className="etapa-conteudo">
            <h2>UCP</h2>

            <div className="secao-equipamento">
              <h3>Problemas Detectados</h3>
              <div className="checkboxes-group">
                {ucpProblemas.map(problema => (
                  <label key={problema} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.ucp_problemas.includes(problema)}
                      onChange={() => handleCheckboxChange('ucp_problemas', problema)}
                    />
                    {problema}
                  </label>
                ))}
              </div>

              {formData.ucp_problemas.length > 0 && (
                <div className="form-grupo">
                  <label>Imagem Antes da Verificação (Obrigatória) *</label>
                  <ImageUploadButton 
                    onFoto={(foto) => handleFoto(foto, 'ucp_foto_antes')} 
                    geolocation={formData}
                    label="Enviar Imagem"
                  />
                </div>
              )}

              <h3>Ações Corretivas Realizadas</h3>
              <div className="checkboxes-group">
                {ucpAcoes.map(acao => (
                  <label key={acao} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.ucp_acoes.includes(acao)}
                      onChange={() => handleCheckboxChange('ucp_acoes', acao)}
                    />
                    {acao}
                  </label>
                ))}
              </div>

              {formData.ucp_acoes.length > 0 && (
                <div className="form-grupo">
                  <label>Imagem Após Ações Realizadas</label>
                  <ImageUploadButton 
                    onFoto={(foto) => handleFoto(foto, 'ucp_foto_depois')} 
                    geolocation={formData}
                    label="Enviar Imagem"
                  />
                </div>
              )}
            </div>

            <div className="form-acoes">
              <button type="button" className="btn btn-voltar" onClick={() => setEtapa('dados')}>
                Voltar
              </button>
              <button type="button" className="btn btn-proximo" onClick={() => setEtapa('tdm')}>
                Próximo
              </button>
            </div>
          </div>
        )}

        {/* PÁGINA 3: TDM */}
        {etapa === 'tdm' && (
          <div className="etapa-conteudo">
            <h2>TDM</h2>

            <div className="secao-equipamento">
              <h3>Problemas Identificados</h3>
              <div className="checkboxes-group">
                {tdmProblemas.map(problema => (
                  <label key={problema} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.tdm_problemas.includes(problema)}
                      onChange={() => handleCheckboxChange('tdm_problemas', problema)}
                    />
                    {problema}
                  </label>
                ))}
              </div>

              {formData.tdm_problemas.length > 0 && (
                <div className="form-grupo">
                  <label>Imagem Antes da Verificação (Obrigatória) *</label>
                  <ImageUploadButton 
                    onFoto={(foto) => handleFoto(foto, 'tdm_foto_antes')} 
                    geolocation={formData}
                    label="Enviar Imagem"
                  />
                </div>
              )}

              <h3>Ações Corretivas Realizadas</h3>
              <div className="checkboxes-group">
                {tdmAcoes.map(acao => (
                  <label key={acao} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.tdm_acoes.includes(acao)}
                      onChange={() => handleCheckboxChange('tdm_acoes', acao)}
                    />
                    {acao}
                  </label>
                ))}
              </div>

              {formData.tdm_acoes.length > 0 && (
                <div className="form-grupo">
                  <label>Imagem Após Ações Realizadas</label>
                  <ImageUploadButton 
                    onFoto={(foto) => handleFoto(foto, 'tdm_foto_depois')} 
                    geolocation={formData}
                    label="Enviar Imagem"
                  />
                </div>
              )}
            </div>

            <div className="form-acoes">
              <button type="button" className="btn btn-voltar" onClick={() => setEtapa('ucp')}>
                Voltar
              </button>
              <button type="button" className="btn btn-proximo" onClick={() => setEtapa('switch')}>
                Próximo
              </button>
            </div>
          </div>
        )}

        {/* PÁGINA 4: SWITCH */}
        {etapa === 'switch' && (
          <div className="etapa-conteudo">
            <h2>Switch</h2>

            <div className="secao-equipamento">
              <h3>Problemas Identificados</h3>
              <div className="checkboxes-group">
                {switchProblemas.map(problema => (
                  <label key={problema} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.switch_problemas.includes(problema)}
                      onChange={() => handleCheckboxChange('switch_problemas', problema)}
                    />
                    {problema}
                  </label>
                ))}
              </div>

              {formData.switch_problemas.length > 0 && (
                <div className="form-grupo">
                  <label>Imagem Antes da Verificação (Obrigatória) *</label>
                  <ImageUploadButton 
                    onFoto={(foto) => handleFoto(foto, 'switch_foto_antes')} 
                    geolocation={formData}
                    label="Enviar Imagem"
                  />
                </div>
              )}

              <h3>Ações Corretivas Realizadas</h3>
              <div className="checkboxes-group">
                {switchAcoes.map(acao => (
                  <label key={acao} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.switch_acoes.includes(acao)}
                      onChange={() => handleCheckboxChange('switch_acoes', acao)}
                    />
                    {acao}
                  </label>
                ))}
              </div>

              {formData.switch_acoes.length > 0 && (
                <div className="form-grupo">
                  <label>Imagem Após Ações Realizadas</label>
                  <ImageUploadButton 
                    onFoto={(foto) => handleFoto(foto, 'switch_foto_depois')} 
                    geolocation={formData}
                    label="Enviar Imagem"
                  />
                </div>
              )}
            </div>

            <div className="form-acoes">
              <button type="button" className="btn btn-voltar" onClick={() => setEtapa('tdm')}>
                Voltar
              </button>
              <button type="button" className="btn btn-proximo" onClick={() => setEtapa('antena')}>
                Próximo
              </button>
            </div>
          </div>
        )}

        {/* PÁGINA 5: ANTENA */}
        {etapa === 'antena' && (
          <div className="etapa-conteudo">
            <h2>Antena</h2>

            <div className="secao-equipamento">
              <h3>Problemas Detectados</h3>
              <div className="checkboxes-group">
                {antenaProblemas.map(problema => (
                  <label key={problema} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.antena_problemas.includes(problema)}
                      onChange={() => handleCheckboxChange('antena_problemas', problema)}
                    />
                    {problema}
                  </label>
                ))}
              </div>

              {formData.antena_problemas.length > 0 && (
                <div className="form-grupo">
                  <label>Imagem Antes da Verificação (Obrigatória) *</label>
                  <ImageUploadButton 
                    onFoto={(foto) => handleFoto(foto, 'antena_foto_antes')} 
                    geolocation={formData}
                    label="Enviar Imagem"
                  />
                </div>
              )}

              <h3>Ações Corretivas</h3>
              <div className="checkboxes-group">
                {antenaAcoes.map(acao => (
                  <label key={acao} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.antena_acoes.includes(acao)}
                      onChange={() => handleCheckboxChange('antena_acoes', acao)}
                    />
                    {acao}
                  </label>
                ))}
              </div>

              {formData.antena_acoes.length > 0 && (
                <div className="form-grupo">
                  <label>Imagem Após Ações Realizadas</label>
                  <ImageUploadButton 
                    onFoto={(foto) => handleFoto(foto, 'antena_foto_depois')} 
                    geolocation={formData}
                    label="Enviar Imagem"
                  />
                </div>
              )}
            </div>

            <div className="form-acoes">
              <button type="button" className="btn btn-voltar" onClick={() => setEtapa('switch')}>
                Voltar
              </button>
              <button type="button" className="btn btn-proximo" onClick={() => setEtapa('observacao')}>
                Próximo
              </button>
            </div>
          </div>
        )}

        {/* PÁGINA 6: OBSERVAÇÃO */}
        {etapa === 'observacao' && (
          <div className="etapa-conteudo">
            <h2>Observações</h2>

            <div className="form-grupo">
              <label>Observações Adicionais</label>
              <p className="sublabel">Digite aqui qualquer observação ou informação importante sobre a manutenção realizada</p>
              <textarea
                name="observacao"
                value={formData.observacao}
                onChange={handleInputChange}
                placeholder="Escreva suas observações aqui..."
                rows="6"
              />
            </div>

            <div className="form-grupo">
              <label>Imagens Adicionais</label>
              <p className="sublabel">Anexe imagens adicionais do seu telefone (falhas, antes/depois não mencionadas acima)</p>
              <input
                type="file"
                accept="image/*"
                onChange={handleImagemAdicional}
                multiple
              />
              {formData.imagens_adicionais.length > 0 && (
                <p className="sucesso">{formData.imagens_adicionais.length} imagem(ns) adicionada(s)</p>
              )}
            </div>

            <div className="form-acoes">
              <button type="button" className="btn btn-voltar" onClick={() => setEtapa('antena')}>
                Voltar
              </button>
              <button
                type="button"
                className="btn btn-enviar"
                onClick={handleEnviar}
                disabled={enviando}
              >
                {enviando ? 'Enviando...' : 'Enviar Formulário'}
              </button>
            </div>

            {autoSalvo && <p className="auto-salvo">Auto-salvo</p>}
          </div>
        )}

        {/* Mensagens */}
        {mensagem && (
          <div className={`mensagem ${mensagem.includes('✅') ? 'sucesso' : 'erro'}`}>
            {mensagem}
          </div>
        )}
      </div>
    </div>
  );
};

export default FormularioComponent;
