from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS
import datetime
import numpy as np


app = Flask(__name__)

# Define your SQLite database path
DB_PATH = 'op_data.db'

cors = CORS(app)

# Route for Latest Blocks
@app.route('/latest_blocks')
def latest_blocks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT B.blockHeight, B.timeStamp, T.transactionHash, B.miner, B.gasUsed, COUNT(T.transactionHash) AS transactionCount
        FROM Blocks B
        LEFT JOIN Transactions T ON B.blockHash = T.blockHash
        GROUP BY B.blockHeight
        ORDER BY B.blockHeight DESC
        LIMIT 5;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    json_results = [
        {
            "blockHeight": row[0],
            "timeStamp": row[1],
            "transactionHash": row[2],
            "miner": row[3],
            "gasUsed": row[4],
            "transactionCount": row[5]
        }
        for row in results
    ]

    return jsonify(json_results)

# Route for Latest Transactions
@app.route('/latest_transactions')
def latest_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT T.transactionHash, T.fromAddress, T.toAddress, T.value, B.blockHeight
        FROM Transactions T
        JOIN Blocks B ON T.blockHash = B.blockHash
        ORDER BY B.blockHeight DESC, T.transactionIndex DESC
        LIMIT 5;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    json_results = [
        {
            "transactionHash": row[0],
            "fromAddress": row[1],
            "toAddress": row[2],
            "value": row[3],
            "blockHeight": row[4]
        }
        for row in results
    ]

    return jsonify(json_results)

# Route for Key Metrics
@app.route('/key_metrics')
def key_metrics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Calculate Average Block Time
    avg_block_time_query = '''
        SELECT AVG(blockInterval) AS avgBlockTime
        FROM (
            SELECT timeStamp - LAG(timeStamp) OVER (ORDER BY blockHeight) AS blockInterval
            FROM Blocks
        );
    '''
    cursor.execute(avg_block_time_query)
    avg_block_time = cursor.fetchone()[0]

    # Calculate Transaction Volume
    transaction_volume_query = '''
        SELECT COUNT(*) AS transactionCount
        FROM Transactions;
    '''
    cursor.execute(transaction_volume_query)
    transaction_volume = cursor.fetchone()[0]

    # Get Latest Block Number
    latest_block_number_query = '''
        SELECT MAX(blockHeight) AS latestBlockNumber
        FROM Blocks;
    '''
    cursor.execute(latest_block_number_query)
    latest_block_number = cursor.fetchone()[0]

    # Calculate Block Volume (Number of Blocks)
    block_volume_query = '''
        SELECT COUNT(*) AS blockCount
        FROM Blocks;
    '''
    cursor.execute(block_volume_query)
    block_volume = cursor.fetchone()[0]

    conn.close()

    key_metrics_data = {
        "avgBlockTime": avg_block_time,
        "transactionVolume": transaction_volume,
        "latestBlockNumber": latest_block_number,
        "blockVolume": block_volume
    }

    return jsonify(key_metrics_data)

# Route for Gas Price Trends
@app.route('/gas_price_trends')
def gas_price_trends():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Group by 5-minute intervals and calculate average gas price and total transactions
    query = '''
        SELECT 
            STRFTIME('%Y-%m-%d %H:%M:%S', (B.timeStamp / 300) * 180, 'unixepoch') AS timeInterval,
            AVG(B.baseFeePerGas) AS avgGasPrice,
            COUNT(T.transactionHash) AS totalTransactionCount
        FROM Blocks AS B
        LEFT JOIN Transactions AS T ON B.blockHash = T.blockHash
        GROUP BY timeInterval
        ORDER BY timeInterval DESC
        LIMIT 50;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    json_results = [
        {
            "timeInterval": row[0],
            "avgGasPrice": row[1],
            "totalTransactionCount": row[2]
        }
        for row in results
    ]

    return jsonify(json_results)


# Route for Gas Efficiency Trends
@app.route('/gas_efficiency_trends')
def gas_efficiency_trends():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Group by 5-minute intervals and calculate average gas used and gas limit
    query = '''
        SELECT 
            STRFTIME('%Y-%m-%d %H:%M:%S', (B.timeStamp / 300) * 300, 'unixepoch') AS timeInterval,
            AVG(B.gasUsed) AS avgGasUsed,
            AVG(B.gasLimit) AS avgGasLimit
        FROM Blocks AS B
        GROUP BY timeInterval
        ORDER BY timeInterval DESC
        LIMIT 30;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    json_results = [
        {
            "timeInterval": row[0],
            "avgGasUsed": row[1],
            "avgGasLimit": row[2]
        }
        for row in results
    ]

    return jsonify(json_results)


# Route for Gas Efficiency vs. Value Transferred
@app.route('/gas_efficiency_value_transferred')
def gas_efficiency_value_transferred():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retrieve data for gas efficiency vs. value transferred
    query = '''
        SELECT 
            B.gasUsed,
            T.value,
            T.gasPrice
        FROM Transactions AS T
        JOIN Blocks AS B ON T.blockHash = B.blockHash
        WHERE T.value > 0
        LIMIT 1000;  -- Limit to the first 1000 records for example
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    json_results = [
        {
            "gasUsed": row[0],
            "valueTransferred": row[1],
            "gasPrice": row[2]
        }
        for row in results
    ]

    return jsonify(json_results)


# Route for Gas Price Heatmap
@app.route('/gas_price_heatmap')
def gas_price_heatmap():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retrieve data for gas price heatmap
    query = '''
        SELECT 
            STRFTIME('%w', B.timeStamp, 'unixepoch') AS dayOfWeek,
            STRFTIME('%H', B.timeStamp, 'unixepoch') AS hourOfDay,
            AVG(T.gasPrice) AS avgGasPrice
        FROM Transactions AS T
        JOIN Blocks AS B ON T.blockHash = B.blockHash
        GROUP BY dayOfWeek, hourOfDay
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    heatmap = np.zeros((7, 24))
    for row in results:
        day = int(row[0])
        hour = int(row[1])
        avg_gas_price = row[2]
        heatmap[day][hour] = avg_gas_price

    json_results = {
        "heatmap": heatmap.tolist(),
        "daysOfWeek": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "hoursOfDay": list(range(24))
    }

    return jsonify(json_results)


if __name__ == '__main__':
    app.run(debug=True)
