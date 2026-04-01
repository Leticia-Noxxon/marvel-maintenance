import React, { useRef, useState } from 'react';
import './CameraComponent.css';

const CameraComponent = ({ onFoto, geolocation }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cameraAcionada, setCameraAcionada] = useState(false);
  const [fotoTirada, setFotoTirada] = useState(false);
  const [erro, setErro] = useState('');

  const iniciarCamera = async () => {
    try {
      setErro('');
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          facingMode: 'environment',
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play().catch(err => {
            console.error('Erro ao reproduzir vídeo:', err);
          });
        };
        setCameraAcionada(true);
      }
    } catch (err) {
      console.error('Erro ao acessar câmera:', err);
      setErro('Não foi possível acessar a câmera. Verifique as permissões.');
    }
  };

  const tirarFoto = () => {
    if (videoRef.current && canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      const video = videoRef.current;

      canvasRef.current.width = video.videoWidth;
      canvasRef.current.height = video.videoHeight;

      ctx.drawImage(video, 0, 0);

      // Adicionar informações de geolocalização na foto
      ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
      ctx.fillRect(10, canvasRef.current.height - 80, canvasRef.current.width - 20, 70);

      ctx.fillStyle = '#fff';
      ctx.font = 'bold 14px Arial';
      ctx.fillText(
        `${geolocation.localizacao || 'Localização'}`,
        20,
        canvasRef.current.height - 55
      );
      ctx.font = '12px Arial';
      ctx.fillText(
        `${geolocation.data} - ${geolocation.hora}`,
        20,
        canvasRef.current.height - 35
      );
      ctx.fillText(
        `Lat: ${geolocation.latitude?.toFixed(6)} | Lng: ${geolocation.longitude?.toFixed(6)}`,
        20,
        canvasRef.current.height - 15
      );

      const fotoUrl = canvasRef.current.toDataURL('image/jpeg', 0.9);
      onFoto(fotoUrl);
      setFotoTirada(true);

      // Parar a câmera
      const stream = video.srcObject;
      stream.getTracks().forEach(track => track.stop());
      setCameraAcionada(false);
    }
  };

  const novaFoto = () => {
    setFotoTirada(false);
    iniciarCamera();
  };

  return (
    <div className="camera-container">
      {!cameraAcionada && !fotoTirada && (
        <button className="btn-iniciar-camera" onClick={iniciarCamera}>
          Enviar Imagem
        </button>
      )}

      {cameraAcionada && (
        <div className="camera-view">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="video-preview"
          />
          <button className="btn-tirar-foto" onClick={tirarFoto}>
            Capturar
          </button>
        </div>
      )}

      {fotoTirada && (
        <div className="foto-capturada">
          <p className="sucesso">Foto capturada!</p>
          <button className="btn-nova-foto" onClick={novaFoto}>
            Nova Foto
          </button>
        </div>
      )}

      <canvas ref={canvasRef} style={{ display: 'none' }} />

      {erro && (
        <div className="erro-camera">
          {erro}
        </div>
      )}
    </div>
  );
};

export default CameraComponent;
