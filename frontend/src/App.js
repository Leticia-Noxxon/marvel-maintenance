import React, { useState, useEffect } from 'react';
import FormularioComponent from './components/FormularioComponent';
import { API_ENDPOINTS } from './config/api';
import './App.css';

function App() {
  const [pwaInstallable, setPwaInstallable] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);

  useEffect(() => {
    const handler = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setPwaInstallable(true);
    };

    window.addEventListener('beforeinstallprompt', handler);

    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleDownloadExcel = async () => {
    try {
      const response = await fetch(API_ENDPOINTS.DOWNLOAD_EXCEL);
      
      if (!response.ok) {
        alert('Arquivo Excel não encontrado. Nenhum formulário foi enviado ainda.');
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Manutenções_Marvel.xlsx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Erro ao baixar Excel:', error);
      alert('Erro ao baixar arquivo Excel');
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Manutenção Marvel</h1>
        <div className="header-buttons">
          <button className="download-btn" onClick={handleDownloadExcel} title="Baixar relatório em Excel">
            Baixar Excel
          </button>
          {pwaInstallable && (
            <button className="install-btn" onClick={handleInstall}>
              Instalar App
            </button>
          )}
        </div>
      </header>
      <main className="app-main">
        <FormularioComponent />
      </main>
      <footer className="app-footer">
        <p>© 2025 Manutenção Marvel - Todos os direitos reservados</p>
      </footer>
    </div>
  );
}

export default App;
