import { useState, useEffect } from "react";
import "./App.css";

function App() {
  // Simulatie van tracks en laps (in toekomst fetch van backend)
  const [tracks, setTracks] = useState([
    { id: 1, name: "RedBull Track" },
    { id: 2, name: "MX Stadium" },
    { id: 3, name: "Forest Circuit" },
  ]);

  const [selectedTrack, setSelectedTrack] = useState(null);
  const [laps, setLaps] = useState([]);

  // Simulatie van ophalen van laps bij track selectie
  useEffect(() => {
    if (selectedTrack) {
      // Hier zou je fetch naar backend doen
      const fetchedLaps = [
        { username: "Coenen", lap_time: 65.747 },
        { username: "Cisse", lap_time: 66.2 },
        { username: "Jan", lap_time: 70.5 },
      ];

      // Bereken de snelste tijd
      const fastest = Math.min(...fetchedLaps.map((l) => l.lap_time));
      // Voeg gap toe
      const lapsWithGap = fetchedLaps.map((l) => ({
        ...l,
        gap: l.lap_time - fastest,
      }));
      setLaps(lapsWithGap);
    }
  }, [selectedTrack]);

  const formatLapTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    const msec = Math.floor((seconds - Math.floor(seconds)) * 1000);
    return `${minutes}:${sec.toString().padStart(2, "0")}.${msec
      .toString()
      .padStart(3, "0")}`;
  };

  return (
    <div className="App">
      <h1>MXBikes Lap Tracker</h1>

      {!selectedTrack && (
        <div className="track-grid">
          {tracks.map((track) => (
            <div
              key={track.id}
              className="track-card"
              onClick={() => setSelectedTrack(track)}
            >
              <h2>{track.name}</h2>
            </div>
          ))}
        </div>
      )}

      {selectedTrack && (
        <div>
          <button onClick={() => setSelectedTrack(null)}>
            ← Back to tracks
          </button>
          <h2>{selectedTrack.name} - Rondetijden</h2>
          <table>
            <thead>
              <tr>
                <th>Username</th>
                <th>Lap Time</th>
                <th>Gap</th>
              </tr>
            </thead>
            <tbody>
              {laps.map((lap, index) => (
                <tr key={index}>
                  <td>{lap.username}</td>
                  <td>{formatLapTime(lap.lap_time)}</td>
                  <td>{lap.gap.toFixed(3)}s</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
