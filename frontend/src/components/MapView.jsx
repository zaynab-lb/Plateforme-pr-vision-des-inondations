import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import { predictRisk } from "../services/api";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

const moroccoPoints = [
  // Nord
  { name: "Tanger", latitude: 35.7595, longitude: -5.8340 },
  { name: "Tétouan", latitude: 35.5785, longitude: -5.3684 },
  { name: "Chefchaouen", latitude: 35.1714, longitude: -5.2697 },

  // Nord-Est
  { name: "Oujda", latitude: 34.6814, longitude: -1.9086 },
  { name: "Taza", latitude: 34.2133, longitude: -4.0083 },

  // Centre Nord
  { name: "Fès", latitude: 34.0331, longitude: -5.0003 },
  { name: "Meknès", latitude: 33.8935, longitude: -5.5473 },
  { name: "Kénitra", latitude: 34.2610, longitude: -6.5802 },
  { name: "Rabat", latitude: 34.0209, longitude: -6.8416 },

  // Centre Atlantique
  { name: "Casablanca", latitude: 33.5731, longitude: -7.5898 },
  { name: "Settat", latitude: 33.0017, longitude: -7.6167 },
  { name: "El Jadida", latitude: 33.2316, longitude: -8.5007 },
  { name: "Safi", latitude: 32.2994, longitude: -9.2372 },

  // Atlas et Centre
  { name: "Béni Mellal", latitude: 32.3373, longitude: -6.3498 },
  { name: "Béjaad", latitude: 32.7725, longitude: -6.3864 },
  { name: "Marrakech", latitude: 31.6295, longitude: -7.9811 },

  // Sud-Est
  { name: "Errachidia", latitude: 31.9314, longitude: -4.4266 },
  { name: "Ouarzazate", latitude: 30.9335, longitude: -6.9370 },

  // Souss
  { name: "Agadir", latitude: 30.4278, longitude: -9.5981 },
  { name: "Taroudant", latitude: 30.4703, longitude: -8.8769 },
  { name: "Tiznit", latitude: 29.6974, longitude: -9.7316 },

  // Sud
  { name: "Guelmim", latitude: 28.9869, longitude: -10.0574 },
  { name: "Tan-Tan", latitude: 28.4378, longitude: -11.1031 },

  // Sahara
  { name: "Laâyoune", latitude: 27.1253, longitude: -13.1625 },
  { name: "Smara", latitude: 26.7386, longitude: -11.6771 },
];

function MapClickHandler({ onMapClick }) {
  useMapEvents({
    click(e) {
      onMapClick(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

function getRiskColor(level) {
  if (level === "Élevé" || level === "Eleve") return "#ef4444";
  if (level === "Moyen") return "#f97316";
  return "#22c55e";
}

function getBadgeClass(level) {
  if (level === "Élevé" || level === "Eleve") return "risk-badge eleve";
  if (level === "Moyen") return "risk-badge moyen";
  return "risk-badge faible";
}

function createColorIcon(level) {
  const color = getRiskColor(level);
  return L.divIcon({
    className: "custom-risk-marker",
    html: `<div style="
      background:${color};
      width:16px;
      height:16px;
      border-radius:50%;
      border:2.5px solid white;
      box-shadow:0 0 0 2px ${color}55, 0 2px 8px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
  });
}

/* Reusable risk rows inside popup */
function RiskRows({ r1, l1, r3, l3, r7, l7 }) {
  return (
    <>
      {[
        { label: "J+1", risk: r1, level: l1 },
        { label: "J+3", risk: r3, level: l3 },
        { label: "J+7", risk: r7, level: l7 },
      ].map(({ label, risk, level }) => (
        <div className="risk-row" key={label}>
          <span className="risk-label">{label}</span>
          <span className="risk-pct">{(risk * 100).toFixed(2)} %</span>
          <span className={getBadgeClass(level)}>{level}</span>
        </div>
      ))}
    </>
  );
}

export default function MapView() {
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [prediction, setPrediction]       = useState(null);
  const [loading, setLoading]             = useState(false);
  const [errorMessage, setErrorMessage]   = useState("");
  const [autoPoints, setAutoPoints]       = useState([]);

  useEffect(() => {
    const loadAutomaticPoints = async () => {
      const results = await Promise.all(
        moroccoPoints.map(async (point) => {
          try {
            const pred = await predictRisk(point.latitude, point.longitude);
            return { ...point, ...pred };
          } catch {
            return null; // skip failed points silently
          }
        })
      );
      setAutoPoints(results.filter(Boolean));
    };

    loadAutomaticPoints();
  }, []);

  const handleMapClick = async (latitude, longitude) => {
    setSelectedPoint({ latitude, longitude });
    setPrediction(null);
    setErrorMessage("");
    setLoading(true);
    try {
      const data = await predictRisk(latitude, longitude);
      setPrediction(data);
    } catch {
      setErrorMessage("Impossible de récupérer la prédiction pour ce point.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="map-wrapper">
      <MapContainer
        center={[31.5, -7]}
        zoom={6}
        minZoom={6}
        maxZoom={12}
        maxBounds={[[20.8, -17.5], [36.5, -0.8]]}
        maxBoundsViscosity={1.0}
        style={{ height: "calc(100vh - 160px)", width: "100%" }}
      >
        <TileLayer
          attribution="Tiles © Esri"
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
        />

        <MapClickHandler onMapClick={handleMapClick} />

        {autoPoints.map((point) => (
          <Marker
            key={point.name}
            position={[point.latitude, point.longitude]}
            icon={createColorIcon(point.level_j1)}
          >
            <Popup maxWidth={260} minWidth={220} autoPan keepInView autoPanPadding={[80, 80]}>
              <div className="popup-content">
                <h3>{point.name}</h3>
                <p className="popup-coord">
                  <span>{point.latitude}° N</span>
                  <span>{Math.abs(point.longitude)}° W</span>
                </p>
                <hr />
                <RiskRows
                  r1={point.risk_j1} l1={point.level_j1}
                  r3={point.risk_j3} l3={point.level_j3}
                  r7={point.risk_j7} l7={point.level_j7}
                />
              </div>
            </Popup>
          </Marker>
        ))}

        {selectedPoint && (
          <Marker position={[selectedPoint.latitude, selectedPoint.longitude]}>
            <Popup maxWidth={260} minWidth={220} autoPan keepInView autoPanPadding={[80, 80]}>
              <div className="popup-content">
                <h3>Risque d'inondation</h3>
                <p className="popup-coord">
                  <span>{selectedPoint.latitude.toFixed(4)}° N</span>
                  <span>{Math.abs(selectedPoint.longitude).toFixed(4)}° W</span>
                </p>

                {loading && (
                  <div className="popup-loading">
                    <div className="spinner" />
                    Analyse en cours…
                  </div>
                )}

                {errorMessage && <p className="error">{errorMessage}</p>}

                {prediction && (
                  <>
                    <hr />
                    <RiskRows
                      r1={prediction.risk_j1} l1={prediction.level_j1}
                      r3={prediction.risk_j3} l3={prediction.level_j3}
                      r7={prediction.risk_j7} l7={prediction.level_j7}
                    />
                  </>
                )}
              </div>
            </Popup>
          </Marker>
        )}
      </MapContainer>

      {/* ── Bottom bar ── */}
      <div className="map-footer">
        <span style={{fontSize: '11px', color: 'var(--text-muted)'}}>
          Prévisions générées le : {new Date().toLocaleDateString('fr-FR')}
        </span>
        {autoPoints.length > 0 && (
            <span style={{fontSize: '11px', color: 'var(--text-muted)'}}>
              {autoPoints.length} villes surveillées
            </span>
          )}
        <div className="legend">
          <span className="legend-label">Risque J+1</span>
          {[
            { cls: "green",  label: "Faible" },
            { cls: "orange", label: "Moyen"  },
            { cls: "red",    label: "Élevé"  },
          ].map(({ cls, label }) => (
            <div className="legend-item" key={cls}>
              <span className={`legend-dot ${cls}`} />
              {label}
            </div>
          ))}
        </div>

        <p className="note">
          Scores estimés par un modèle XGBoost entraîné sur des données
          météorologiques, hydrologiques et géospatiales. Cliquez sur la carte
          pour analyser n'importe quel point.
        </p>
      </div>
    </div>
  );
}