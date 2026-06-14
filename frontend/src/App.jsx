import "./App.css";
import MapView from "./components/MapView";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Plateforme de prévision des inondations</h1>
        <p>Carte interactive des risques J+1, J+3 et J+7 au Maroc</p>
      </header>

      <main>
        <MapView />
      </main>
    </div>
  );
}

export default App;