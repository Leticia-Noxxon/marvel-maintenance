import React, { useRef, useState } from 'react';
import CameraComponent from './CameraComponent';
import './ImageUploadButton.css';

const ImageUploadButton = ({ onFoto, geolocation, label = 'Enviar Imagem' }) => {
  const fileInputRef = useRef(null);
  const [showMenuCamera, setShowMenuCamera] = useState(false);
  const [showCamera, setShowCamera] = useState(false);
  const [imagemCarregada, setImagemCarregada] = useState(false);

  const handleSelectFromFile = () => {
    fileInputRef.current?.click();
  };

  const handleFileSelect = (e) => {
    if (e.target.files[0]) {
      const reader = new FileReader();
      reader.onload = (event) => {
        onFoto(event.target.result);
        setImagemCarregada(true);
        setShowMenuCamera(false);
        setTimeout(() => setImagemCarregada(false), 2000);
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  };

  const handleFotoTirada = (foto) => {
    onFoto(foto);
    setShowCamera(false);
    setShowMenuCamera(false);
    setImagemCarregada(true);
    setTimeout(() => setImagemCarregada(false), 2000);
  };

  return (
    <div className="image-upload-wrapper">
      {showCamera ? (
        <div className="camera-container">
          <CameraComponent 
            onFoto={handleFotoTirada} 
            geolocation={geolocation}
          />
          <button 
            type="button"
            className="btn btn-cancelar-camera"
            onClick={() => setShowCamera(false)}
          >
            Cancelar
          </button>
        </div>
      ) : showMenuCamera ? (
        <div className="menu-overlay">
          <div className="menu-opcoes">
            <button 
              type="button"
              className="opcao-btn opcao-camera"
              onClick={() => setShowCamera(true)}
            >
              📷 Tirar Foto
            </button>
            <button 
              type="button"
              className="opcao-btn opcao-arquivo"
              onClick={handleSelectFromFile}
            >
              📁 Selecionar do Celular
            </button>
            <button 
              type="button"
              className="opcao-btn opcao-cancelar"
              onClick={() => setShowMenuCamera(false)}
            >
              ✕ Cancelar
            </button>
          </div>
        </div>
      ) : (
        <div>
          <button 
            type="button"
            className="btn btn-enviar-imagem"
            onClick={() => setShowMenuCamera(true)}
          >
            {label}
          </button>
          {imagemCarregada && <p className="sucesso">✅ Imagem capturada</p>}
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />
    </div>
  );
};

export default ImageUploadButton;
