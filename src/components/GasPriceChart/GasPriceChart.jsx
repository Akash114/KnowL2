import React, { Component } from "react";
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-moment';
import { Line } from "react-chartjs-2";


class GasPriceChart extends Component {
  
  render() {
    Chart.register(...registerables);

    const { gasPriceData } = this.props;

    const labels = gasPriceData.map(entry => entry.timeInterval);
    const avgGasPrices = gasPriceData.map(entry => entry.avgGasPrice);
    const totalTransactionCounts = gasPriceData.map(entry => entry.totalTransactionCount);

    const chartData = {
      labels: labels,
      datasets: [
        {
          label: "Average Gas Price",
          data: avgGasPrices,
          fill: false,
          borderColor: "rgba(29, 111, 165, 1)",
          yAxisID: "y-axis-avg-gas",
        },
        {
          label: "Total Transaction Count",
          data: totalTransactionCounts,
          fill: false,
          borderColor: "rgba(255, 99, 132, 1)",
          yAxisID: "y-axis-total-transactions",
        },
      ],
    };

    const chartOptions = {
      scales: {
        x: {
          type: "time",
          time: {
            unit: "minute",
            displayFormats: {
              minute: "HH:mm",
            },
          },
          title: {
            display: true,
            text: "Time Interval",
          },
        },
        yAxes: [
          {
            id: "y-axis-avg-gas",
            type: "linear",
            position: "left",
            title: {
              display: true,
              text: "Average Gas Price",
            },
            ticks: {
              beginAtZero: true,
            },
          },
          {
            id: "y-axis-total-transactions",
            type: "linear",
            position: "right",
            title: {
              display: true,
              text: "Total Transaction Count",
            },
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
      tooltips: {
        mode: "index",
        intersect: false,
        callbacks: {
          label: function(context) {
            const labelIndex = context.dataIndex;
            const avgGasPrice = context.dataset.data[labelIndex];
            const totalTransactionCount = totalTransactionCounts[labelIndex];
            return [
              `Avg Gas Price: ${avgGasPrice.toFixed(2)}`,
              `Total Transactions: ${totalTransactionCount}`,
            ];
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
