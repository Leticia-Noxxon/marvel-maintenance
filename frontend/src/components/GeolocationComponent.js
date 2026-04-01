import React, { useState, useEffect } from 'react';
import './GeolocationComponent.css';

const GeolocationComponent = ({ onGeolocation }) => {
  const [locationState, setLocationState] = useState({
    localizando: false,
    erro: '',
    sucesso: false
  });

  const obterLocalizacao = () => {
    setLocationState({ localizando: true, erro: '', sucesso: false });

    if (!navigator.geolocation) {
      setLocationState({
        localizando: false,
        erro: '❌ Geolocalização não é suportada neste navegador',
        sucesso: false
      });
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        const accuracy = position.coords.accuracy;

        // Obter endereço via reverse geocoding (usando OpenStreetMap)
        fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
        )
          .then(res => res.json())
          .then(data => {
            // Montar endereço completo
            const addr = data.address || {};
            const rua = addr.road || '';
            const numero = addr.house_number || '';
            const bairro = addr.neighbourhood || addr.suburb || '';
            const cidade = addr.city || addr.town || addr.village || '';
            const estado = addr.state || '';
            
            const enderecoCompleto = [rua, numero, bairro, cidade, estado]
              .filter(part => part.trim() !== '')
              .join(', ');

            onGeolocation({
              latitude,
              longitude,
              localizacao: cidade,
              localizacao_completa: enderecoCompleto || 'Localização capturada',
              accuracy
            });

            setLocationState({
              localizando: false,
              erro: '',
              sucesso: true
            });
          })
          .catch(err => {
            console.error('Erro ao obter endereço:', err);
            onGeolocation({ 
              latitude, 
              longitude, 
              localizacao: 'Localização capturada',
              localizacao_completa: 'Localização capturada',
              accuracy 
            });
            setLocationState({
              localizando: false,
              erro: '',
              sucesso: true
            });
          });
      },
      (error) => {
        console.error('Erro de geolocalização:', error);
        let mensagemErro = '❌ Erro ao obter localização';

        if (error.code === error.PERMISSION_DENIED) {
          mensagemErro = '❌ Permissão negada. Ative a localização nas configurações.';
        } else if (error.code === error.POSITION_UNAVAILABLE) {
          mensagemErro = '❌ Localização não disponível no momento.';
        } else if (error.code === error.TIMEOUT) {
          mensagemErro = '❌ Tempo limite excedido ao obter localização.';
        }

        setLocationState({
          localizando: false,
          erro: mensagemErro,
          sucesso: false
        });
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  };

  return (
    <div className="geolocation-container">
      <button
        type="button"
        className="btn-localizacao"
        onClick={obterLocalizacao}
        disabled={locationState.localizando}
      >
        {locationState.localizando ? 'Localizando...' : 'Compartilhar Localização'}
      </button>

      {locationState.erro && (
        <div className="mensagem-geo erro">
          {locationState.erro}
        </div>
      )}

      {locationState.sucesso && (
        <div className="mensagem-geo sucesso">
          ✅ Localização capturada com sucesso!
        </div>
      )}
    </div>
  );
};

export default GeolocationComponent;
