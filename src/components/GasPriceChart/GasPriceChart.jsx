import React, { Component } from "react";
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-moment';
import { Line } from "react-chartjs-2";


class GasPriceChart extends Component {
  
  render() {
    Chart.register(...registerables);

    const { gasPriceData } = this.props;

    const labels = gasPriceData.map(entry => entry.timeStamp);
    const data = gasPriceData.map(entry => entry.baseFeePerGas);

    const chartData = {
      labels: labels,
      datasets: [
        {
          label: "Gas Price Trends",
          data: data,
          fill: false,
          borderColor: "rgba(29, 111, 165, 1)",
        },
      ],
    };

    const chartOptions = {
      scales: {
        x: {
          type: "time",
          time: {
            unit: "second",
            displayFormats: {
              second: "HH:mm:ss",
            },
          },
          title: {
            display: true,
            text: "Timestamp",
          },
        },
        y: {
          title: {
            display: true,
            text: "Base Fee Per Gas",
          },
        },
      },
    };

    return (
      <div>
        <Line data={chartData} options={chartOptions} />
      </div>
    );
  }
}

export default GasPriceChart;
