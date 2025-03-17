// frontend/src/components/ChartComponent.js
import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const ChartComponent = ({ results }) => {
  if (!results || results.length === 0) {
    return <p>Aucune donnée pour générer le graphique.</p>;
  }

  // Préparation des données pour le graphique
  const labels = results.map(result => result.driver.name);
  const dataPoints = results.map(result => result.points);

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Points',
        data: dataPoints,
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
  };

  return (
    <div>
      <Bar data={data} options={options} />
    </div>
  );
};

export default ChartComponent;