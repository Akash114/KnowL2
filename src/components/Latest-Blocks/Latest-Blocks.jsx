import React, { Component } from "react";
import { Table, Label } from "semantic-ui-react";
import axios from "axios";

class LatestBlocks extends Component {
  constructor(props) {
    super(props);
    this.state = {
      blocks: [],
    };
  }

  componentDidMount = () => {
    this.getBlocks();
  };

  getBlocks = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/latest_blocks");
      const blocks = response.data;

      const blockRows = blocks.map((block, index) => (
        <Table.Row key={index}>
          <Table.Cell>
            <Label color="blue">Bk</Label> {block.blockHeight}
          </Table.Cell>
          <Table.Cell>
            Miner {block.miner} <br />
            Txs {block.transactionCount}
          </Table.Cell>
          <Table.Cell>
            <Label color="blue">Gas </Label> {block.gasUsed}
          </Table.Cell>
        </Table.Row>
      ));

      this.setState({
        blocks: blockRows,
      });
    } catch (error) {
      console.error("Error fetching blocks:", error);
    }
  };

  render() {
    return (
      <Table fixed>
        <Table.Header>
          <Table.Row>
            <Table.Cell style={{ color: "#1d6fa5" }}>
              <h4>Latest Blocks</h4>
            </Table.Cell>
          </Table.Row>
        </Table.Header>

        <Table.Body>{this.state.blocks}</Table.Body>
      </Table>
    );
  }
}

export default LatestBlocks;
