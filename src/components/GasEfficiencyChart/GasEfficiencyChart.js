import React, { Component } from "react";
import { Line } from "react-chartjs-2";

class GasEfficiencyChart extends Component {
  render() {
    const { gasEfficiencyData } = this.props;

    const labels = gasEfficiencyData.map((entry) => entry.timeInterval);
    const gasEfficiencyValues = gasEfficiencyData.map((entry) => {
      const gasUsed = entry.gasUsed;
      const valueTransferred = entry.valueTransferred;
      return gasUsed / valueTransferred;
    });

    const chartData = {
      labels: labels,
      datasets: [
        {
          label: "Gas Efficiency (Gas Used per Value Transferred)",
          data: gasEfficiencyValues,
          borderColor: "rgba(29, 111, 165, 1)",
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
        y: {
          title: {
            display: true,
            text: "Gas Efficiency (Gas Used per Value Transferred)",
          },
          ticks: {
            callback: function (value, index, values) {
              return value.toExponential(2);
            },
          },
        },
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              const labelIndex = context.dataIndex;
              const gasEfficiencyValue = gasEfficiencyValues[labelIndex];
              return `Gas Efficiency: ${gasEfficiencyValue.toExponential(2)}`;
            },
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

export default GasEfficiencyChart;
