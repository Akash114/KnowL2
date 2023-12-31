import React, { Component } from "react";
import axios from "axios";
import "./eth-overview.css";
import { Card, Grid, Icon } from "semantic-ui-react";
import LatestBlocks from "../Latest-Blocks/index";
import LatestTxs from "../Latest-Txs/index";
import GasPriceChart from "../GasPriceChart/index"; // Update the path to your GasPriceChart component
import GasEfficiencyChart from "../GasEfficiencyChart/index"; // Update the path to your GasPriceChart component


class EthOverview extends Component {
  constructor() {
    super();
    this.state = {
      avgBlockTime: 0,
      blockVolume: 0,
      latestBlockNumber: 0,
      transactionVolume: 0,
      gasPriceData: [],
      gasEfficiencyData: [],
    };
  }

  async componentDidMount() {
    // Fetch key metrics data
    const keyMetrics = await axios.get("https://know-l2.vercel.app/key_metrics");
    const metricsData = keyMetrics.data;

    this.setState({
      avgBlockTime: metricsData.avgBlockTime,
      blockVolume: metricsData.blockVolume,
      latestBlockNumber: metricsData.latestBlockNumber,
      transactionVolume: metricsData.transactionVolume,
    });

    try {
      const response = await axios.get("https://know-l2.vercel.app/gas_price_trends");
      const gasPriceData = response.data;
      this.setState({ gasPriceData });
    } catch (error) {
      console.error("Error fetching gas price data:", error);
    }

    try {
      const response = await axios.get("https://know-l2.vercel.app/gas_efficiency_trends");
      const gasEfficiencyData = response.data;
      this.setState({ gasEfficiencyData });
    } catch (error) {
      console.error("Error fetching gas efficiency data:", error);
    }


  }

  render() {
    const {
      avgBlockTime,
      blockVolume,
      latestBlockNumber,
      transactionVolume,
      gasPriceData,
      gasEfficiencyData
    } = this.state;
    return (
      <div>
        <Grid>
          <Grid.Row>
            <Grid.Column width={4}>
              <Card>
                <Card.Content>
                  <Card.Header style={{ color: "#1d6fa5" }}>
                    <Icon name="ethereum"></Icon> TRANSACTION VOLUME
                  </Card.Header>
                  <Card.Description textAlign="left">
                    {transactionVolume}
                  </Card.Description>
                </Card.Content>
              </Card>
            </Grid.Column>
            <Grid.Column width={4}>
              <Card>
                <Card.Content>
                  <Card.Header style={{ color: "#1d6fa5" }}>
                    <Icon name="list alternate outline"></Icon> LATEST BLOCK
                  </Card.Header>
                  <Card.Description textAlign="left">
                    <Icon name="square"></Icon> {latestBlockNumber}
                  </Card.Description>
                </Card.Content>
              </Card>
            </Grid.Column>
            <Grid.Column width={4}>
              <Card>
                <Card.Content>
                  <Card.Header style={{ color: "#1d6fa5" }}>
                    <Icon name="setting"></Icon> AVG BLOCK TIME
                  </Card.Header>
                  <Card.Description textAlign="left">
                    {avgBlockTime} seconds
                  </Card.Description>
                </Card.Content>
              </Card>
            </Grid.Column>
            <Grid.Column width={4}>
              <Card>
                <Card.Content>
                  <Card.Header style={{ color: "#1d6fa5" }}>
                    <Icon name="world"></Icon> BLOCK VOLUME
                  </Card.Header>
                  <Card.Description textAlign="left">
                    {blockVolume} blocks
                  </Card.Description>
                </Card.Content>
              </Card>
            </Grid.Column>
          </Grid.Row>
        </Grid>

                <GasPriceChart gasPriceData={gasPriceData} />
                {/* <GasEfficiencyChart gasEfficiencyData={gasEfficiencyData} /> */}


        <Grid divided="vertically">
          <Grid.Row columns={2}>
            <Grid.Column>
              <LatestBlocks></LatestBlocks>
            </Grid.Column>
            <Grid.Column>
              <LatestTxs ></LatestTxs>
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </div>
    );
  }
}

export default EthOverview;
