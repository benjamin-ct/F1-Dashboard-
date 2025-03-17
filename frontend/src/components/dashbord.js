// frontend/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ChartComponent from './ChartComponent';

const Dashboard = () => {
  const [liveRace, setLiveRace] = useState(null);

  useEffect(() => {
    const fetchLiveRace = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/live');
        setLiveRace(response.data);
      } catch (error) {
        console.error("Erreur lors de la récupération des données live", error);
      }
    };

    fetchLiveRace();
    const intervalId = setInterval(fetchLiveRace, 60000); // Rafraîchissement toutes les minutes
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      {liveRace ? (
        <div>
          <h2>
            {liveRace.name} - {new Date(liveRace.date).toLocaleDateString()}
          </h2>
          <p>Circuit : {liveRace.circuit}</p>
          <ChartComponent results={liveRace.results} />
        </div>
      ) : (
        <p>Chargement des données en direct...</p>
      )}
    </div>
  );
};

export default Dashboard;