import React, { Component } from "react";
import { Table, Label } from "semantic-ui-react";
import axios from "axios";

class LatestTxs extends Component {
  constructor(props) {
    super(props);
    this.state = {
      transactions: [],
    };
  }

  componentDidMount = () => {
    this.getTxs();
  };

  getTxs = async () => {
    try {
      const response = await axios.get("https://know-l2.vercel.app/latest_transactions");
      const transactions = response.data;

      const txsDetails = transactions.map((tx, index) => (
        <Table.Row key={index}>
          <Table.Cell>
            <Label color="blue">Tx</Label> {tx.transactionHash}
          </Table.Cell>
          <Table.Cell>
            From {tx.fromAddress} <br />
            To {tx.toAddress}
          </Table.Cell>
          <Table.Cell>
            {" "}
            <Label color="blue">Eth</Label> {tx.value / 10 ** 18}
          </Table.Cell>
        </Table.Row>
      ));

      this.setState({
        transactions: txsDetails,
      });
    } catch (error) {
      console.error("Error fetching transactions:", error);
    }
  };

  render() {
    return (
      <div>
        <Table fixed>
          <Table.Header>
            <Table.Row>
              <Table.Cell style={{ color: "#1d6fa5" }}>
                <h4> Latest Transactions</h4>
              </Table.Cell>
            </Table.Row>
          </Table.Header>

          <Table.Body>{this.state.transactions}</Table.Body>
        </Table>
      </div>
    );
  }
}

export default LatestTxs;
