import React, { useState } from "react";
import "./App.css";
import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix default marker icons in React Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function App() {
  const [transportMode, setTransportMode] = useState("cycle");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Bhubaneswar demo coordinates
  const startPoint = [20.2961, 85.8245]; // Master Canteen area
  const endPoint = [20.3176, 85.8191];   // KIIT side-ish sample

  // Different route shapes for each transport mode
  const routePaths = {
    walk: [
      [20.2961, 85.8245],
      [20.3000, 85.8230],
      [20.3055, 85.8210],
      [20.3110, 85.8200],
      [20.3176, 85.8191],
    ],
    cycle: [
      [20.2961, 85.8245],
      [20.3015, 85.8260],
      [20.3070, 85.8240],
      [20.3125, 85.8215],
      [20.3176, 85.8191],
    ],
    bus: [
      [20.2961, 85.8245],
      [20.2990, 85.8280],
      [20.3060, 85.8270],
      [20.3135, 85.8235],
      [20.3176, 85.8191],
    ],
    car: [
      [20.2961, 85.8245],
      [20.3030, 85.8290],
      [20.3100, 85.8265],
      [20.3150, 85.8220],
      [20.3176, 85.8191],
    ],
  };

  const routeColors = {
    walk: "#16a34a",
    cycle: "#2563eb",
    bus: "#f59e0b",
    car: "#ef4444",
  };

  const runSimulation = async () => {
    setLoading(true);
    setResult(null);

    try {
      await fetch("http://localhost:8000/reset", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const stepRes = await fetch("http://localhost:8000/step", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action: {
            transport_mode: transportMode,
            traffic_level: 3,
            distance_km: 10,
          },
        }),
      });

      const stepData = await stepRes.json();

      setResult({
        status: stepRes.status,
        ok: stepRes.ok,
        data: stepData,
      });
    } catch (error) {
      setResult({
        error: "Failed to fetch",
      });
    }

    setLoading(false);
  };

  const observation = result?.data?.observation;
  const currentRoute = routePaths[transportMode];
  const currentColor = routeColors[transportMode];

  const carEmission = 2.8; // demo comparison baseline
  const currentEmission = observation?.co2_emission ?? 0;
  const savedCO2 = Math.max(0, (carEmission - currentEmission)).toFixed(2);

  return (
    <div className="app">
      <div className="container">
        <h1>🌍 EcoRoute RL Agent</h1>
        <p className="subtitle">
          AI-powered eco-friendly route simulation with real map visualization
        </p>

        <div className="controls">
          <label>Select Transport Mode:</label>
          <select
            value={transportMode}
            onChange={(e) => setTransportMode(e.target.value)}
          >
            <option value="walk">Walk</option>
            <option value="cycle">Cycle</option>
            <option value="bus">Bus</option>
            <option value="car">Car</option>
          </select>

          <button onClick={runSimulation} disabled={loading}>
            {loading ? "Running..." : "Run Simulation"}
          </button>
        </div>

        {result?.error && (
          <div className="error-box">
            <h3>⚠ Error</h3>
            <p>{result.error}</p>
          </div>
        )}

        {/* Always show map for premium feel */}
        <div className="map-box">
          <div className="map-header">
            <h3>🗺 Live Route Visualization</h3>
            <span
              className="mode-badge"
              style={{ backgroundColor: currentColor }}
            >
              {transportMode.toUpperCase()}
            </span>
          </div>

          <MapContainer
            center={[20.3065, 85.8235]}
            zoom={13}
            scrollWheelZoom={true}
            className="leaflet-map"
          >
            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            <Marker position={startPoint}>
              <Popup>📍 Start Point</Popup>
            </Marker>

            <Marker position={endPoint}>
              <Popup>🏁 Destination</Popup>
            </Marker>

            <Polyline
              positions={currentRoute}
              pathOptions={{ color: currentColor, weight: 6 }}
            />
          </MapContainer>
        </div>

        {result && !result.error && observation && (
          <div className="result-box">
            <h2>📊 Simulation Result</h2>

            <div className="route-box">
              <h3>🛣 Suggested Route</h3>
              <p>{observation.suggested_route}</p>
            </div>

            <div className="insight-box">
              <h3>💡 Sustainability Insight</h3>
              <p>
                {transportMode === "car"
                  ? "Car mode provides convenience but has the highest environmental impact in this simulation."
                  : `${transportMode.toUpperCase()} saves approximately ${savedCO2} kg CO₂ compared to a typical car route.`}
              </p>
            </div>

            <div className="eco-score-section">
              <div className="eco-score-top">
                <span>⭐ Eco Score</span>
                <span>{observation.eco_score}/10</span>
              </div>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${observation.eco_score * 10}%` }}
                ></div>
              </div>
            </div>

            <div className="cards-grid">
              <div className="card">
                <h4>🚲 Transport Mode</h4>
                <p>{transportMode.toUpperCase()}</p>
              </div>

              <div className="card">
                <h4>⏱ Estimated Time</h4>
                <p>{observation.estimated_time} mins</p>
              </div>

              <div className="card">
                <h4>🌿 CO₂ Emission</h4>
                <p>{observation.co2_emission} kg</p>
              </div>

              <div className="card">
                <h4>🌫 Air Quality Exposure</h4>
                <p>{observation.air_quality_exposure}</p>
              </div>

              <div className="card">
                <h4>🎯 Reward</h4>
                <p>{result.data.reward}</p>
              </div>

              <div className="card">
                <h4>🏁 Status</h4>
                <p>{result.data.done ? "Completed" : "In Progress"}</p>
              </div>

              <div className="card">
                <h4>✅ API Status</h4>
                <p>{result.status} OK</p>
              </div>

              <div className="card">
                <h4>📍 Route Type</h4>
                <p>
                  {transportMode === "walk"
                    ? "Pedestrian"
                    : transportMode === "cycle"
                    ? "Cycle Lane"
                    : transportMode === "bus"
                    ? "Public Transit"
                    : "Road Traffic"}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;