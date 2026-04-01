import React, { useEffect } from 'react';
import L from 'leaflet';
import './MapComponent.css';

const MapComponent = ({ latitude, longitude }) => {
  useEffect(() => {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) return;

    // Limpar mapa anterior se existir
    mapContainer.innerHTML = '';

    const map = L.map('map').setView([latitude, longitude], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map);

    L.circleMarker([latitude, longitude], {
      radius: 15,
      fillColor: '#667eea',
      color: '#764ba2',
      weight: 3,
      opacity: 1,
      fillOpacity: 0.8,
    })
      .addTo(map)
      .bindPopup(`<b>Sua Localização</b><br>Lat: ${latitude.toFixed(6)}<br>Lng: ${longitude.toFixed(6)}`);

    // Adicionar círculo de acurácia
    L.circle([latitude, longitude], {
      color: '#667eea',
      fillColor: '#667eea',
      fillOpacity: 0.1,
      radius: 100,
      weight: 2,
    }).addTo(map);

  }, [latitude, longitude]);

  return <div id="map" className="map-container"></div>;
};

export default MapComponent;
