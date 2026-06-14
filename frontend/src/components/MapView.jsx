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
  { name: "Tanger", latitude: 35.7595, longitude: -5.8340 },
  { name: "Tétouan", latitude: 35.5785, longitude: -5.3684 },
  { name: "Chefchaouen", latitude: 35.1714, longitude: -5.2697 },

  { name: "Rabat", latitude: 34.0209, longitude: -6.8416 },
  { name: "Kénitra", latitude: 34.2610, longitude: -6.5802 },
  { name: "Casablanca", latitude: 33.5731, longitude: -7.5898 },
  { name: "El Jadida", latitude: 33.2316, longitude: -8.5007 },
  { name: "Safi", latitude: 32.2994, longitude: -9.2372 },

  { name: "Fès", latitude: 34.0331, longitude: -5.0003 },
  { name: "Meknès", latitude: 33.8935, longitude: -5.5473 },
  { name: "Oujda", latitude: 34.6814, longitude: -1.9086 },
  { name: "Taza", latitude: 34.2133, longitude: -4.0083 },

  { name: "Marrakech", latitude: 31.6295, longitude: -7.9811 },
  { name: "Béni Mellal", latitude: 32.3373, longitude: -6.3498 },
  { name: "Khénifra", latitude: 32.9391, longitude: -5.6686 },
  { name: "Ouarzazate", latitude: 30.9335, longitude: -6.9370 },
  { name: "Errachidia", latitude: 31.9314, longitude: -4.4266 },

  { name: "Agadir", latitude: 30.4278, longitude: -9.5981 },
  { name: "Taroudant", latitude: 30.4703, longitude: -8.8769 },
  { name: "Guelmim", latitude: 28.9869, longitude: -10.0574 },
  { name: "Laâyoune", latitude: 27.1253, longitude: -13.1625 },
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
  if (level === "Élevé" || level === "Eleve") return "red";
  if (level === "Moyen") return "orange";
  return "green";
}

function createColorIcon(level) {
  const color = getRiskColor(level);

  return L.divIcon({
    className: "custom-risk-marker",
    html: `<div style="
      background:${color};
      width:18px;
      height:18px;
      border-radius:50%;
      border:3px solid white;
      box-shadow:0 0 8px rgba(0,0,0,0.4);
    "></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });
}

export default function MapView() {
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [autoPoints, setAutoPoints] = useState([]);

  useEffect(() => {
    const loadAutomaticPoints = async () => {
      const results = [];

      for (const point of moroccoPoints) {
        try {
          const prediction = await predictRisk(point.latitude, point.longitude);
          results.push({ ...point, ...prediction });
        } catch (error) {
          console.error("Erreur point automatique :", point.name, error);
        }
      }

      setAutoPoints(results);
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
    } catch (error) {
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
        maxBounds={[
          [20.8, -17.5],
          [36.5, -0.8],
        ]}
        maxBoundsViscosity={1.0}
        style={{ height: "75vh", width: "100%" }}
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
            <Popup
              maxWidth={280}
              minWidth={230}
              autoPan={true}
              keepInView={true}
              autoPanPadding={[80, 80]}
            >
              <div className="popup-content">
                <h3>{point.name}</h3>
                <p>
                  <strong>Latitude :</strong> {point.latitude}
                </p>
                <p>
                  <strong>Longitude :</strong> {point.longitude}
                </p>
                <hr />
                <p>
                  <strong>J+1 :</strong> {(point.risk_j1 * 100).toFixed(2)} % -{" "}
                  {point.level_j1}
                </p>
                <p>
                  <strong>J+3 :</strong> {(point.risk_j3 * 100).toFixed(2)} % -{" "}
                  {point.level_j3}
                </p>
                <p>
                  <strong>J+7 :</strong> {(point.risk_j7 * 100).toFixed(2)} % -{" "}
                  {point.level_j7}
                </p>
              </div>
            </Popup>
          </Marker>
        ))}

        {selectedPoint && (
          <Marker position={[selectedPoint.latitude, selectedPoint.longitude]}>
            <Popup
              maxWidth={280}
              minWidth={230}
              autoPan={true}
              keepInView={true}
              autoPanPadding={[80, 80]}
            >
              <div className="popup-content">
                <h3>Risque d'inondation</h3>

                <p>
                  <strong>Latitude :</strong>{" "}
                  {selectedPoint.latitude.toFixed(4)}
                </p>
                <p>
                  <strong>Longitude :</strong>{" "}
                  {selectedPoint.longitude.toFixed(4)}
                </p>

                {loading && <p>Chargement...</p>}

                {errorMessage && <p className="error">{errorMessage}</p>}

                {prediction && (
                  <>
                    <hr />
                    <p>
                      <strong>J+1 :</strong>{" "}
                      {(prediction.risk_j1 * 100).toFixed(2)} % -{" "}
                      {prediction.level_j1}
                    </p>
                    <p>
                      <strong>J+3 :</strong>{" "}
                      {(prediction.risk_j3 * 100).toFixed(2)} % -{" "}
                      {prediction.level_j3}
                    </p>
                    <p>
                      <strong>J+7 :</strong>{" "}
                      {(prediction.risk_j7 * 100).toFixed(2)} % -{" "}
                      {prediction.level_j7}
                    </p>
                  </>
                )}
              </div>
            </Popup>
          </Marker>
        )}
      </MapContainer>

      <div className="legend">
        <span>🟢 Faible</span>
        <span>🟠 Moyen</span>
        <span>🔴 Élevé</span>
      </div>
    </div>
  );
}