from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Define your SQLite database path
DB_PATH = 'op_data.db'

# Route for Latest Blocks
@app.route('/latest_blocks')
def latest_blocks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT blockHeight, timeStamp, (SELECT COUNT(*) FROM Transactions WHERE Transactions.blockHash = Blocks.blockHash) AS transactionCount
        FROM Blocks
        ORDER BY blockHeight DESC
        LIMIT 10;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    json_results = [
        {
            "blockHeight": row[0],
            "timeStamp": row[1],
            "transactionCount": row[2]
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
        SELECT transactionHash, fromAddress, toAddress, value
        FROM Transactions
        ORDER BY blockHeight DESC, transactionIndex DESC
        LIMIT 10;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    json_results = [
        {
            "transactionHash": row[0],
            "fromAddress": row[1],
            "toAddress": row[2],
            "value": row[3]
        }
        for row in results
    ]

    return jsonify(json_results)

# Route for Transaction Volume
@app.route('/transaction_volume')
def transaction_volume():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT COUNT(*) AS transactionCount
        FROM Transactions;
    '''

    cursor.execute(query)
    result = cursor.fetchone()[0]

    conn.close()

    return jsonify({"transactionCount": result})

# Route for Gas Price Trends
@app.route('/gas_price_trends')
def gas_price_trends():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT timeStamp, baseFeePerGas
        FROM Blocks
        ORDER BY blockHeight DESC
        LIMIT 30;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    json_results = [
        {
            "timeStamp": row[0],
            "baseFeePerGas": row[1]
        }
        for row in results
    ]

    return jsonify(json_results)

# Route for Network Activity Chart
@app.route('/network_activity_chart')
def network_activity_chart():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT blockHeight, (SELECT COUNT(*) FROM Transactions WHERE Transactions.blockHash = Blocks.blockHash) AS transactionCount
        FROM Blocks
        ORDER BY blockHeight;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return jsonify(results)

# Route for Average Block Time
@app.route('/average_block_time')
def average_block_time():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT blockHeight, timeStamp, LAG(timeStamp) OVER (ORDER BY blockHeight) AS prevTimeStamp
        FROM Blocks
        ORDER BY blockHeight;
    '''

    cursor.execute(query)
    rows = cursor.fetchall()

    average_block_time = sum(rows[i][1] - rows[i][2] for i in range(1, len(rows))) / (len(rows) - 1)
    
    conn.close()
    return jsonify({'averageBlockTime': average_block_time})

# Route for Gas Efficiency Trends
@app.route('/gas_efficiency_trends')
def gas_efficiency_trends():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT blockHeight, gasEfficiency
        FROM GasEfficiencyTrends  -- Update with your actual table name
        ORDER BY blockHeight;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return jsonify(results)

# Route for Gas Used vs. Gas Limit
@app.route('/gas_used_vs_gas_limit')
def gas_used_vs_gas_limit():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT blockHeight, gasUsed, gasLimit
        FROM Blocks
        ORDER BY blockHeight;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
