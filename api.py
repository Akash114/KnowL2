from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# SQLite database connection
db_connection = sqlite3.connect('op_data.db')
db_cursor = db_connection.cursor()

# Gas Usage Tracker
@app.route('/gas_usage', methods=['GET'])
def gas_usage_tracker():
    db_cursor.execute('SELECT blockHeight, gasUsed FROM Blocks ORDER BY blockHeight;')
    data = [{'blockHeight': row[0], 'gasUsed': row[1]} for row in db_cursor.fetchall()]
    return jsonify(data)

# Transaction Volume Tracker
@app.route('/transaction_volume', methods=['GET'])
def transaction_volume_tracker():
    db_cursor.execute('SELECT blockHeight, COUNT(*) AS transactionCount FROM Transactions GROUP BY blockHeight ORDER BY blockHeight;')
    data = [{'blockHeight': row[0], 'transactionCount': row[1]} for row in db_cursor.fetchall()]
    return jsonify(data)

# Gas Price Tracker
@app.route('/gas_price', methods=['GET'])
def gas_price_tracker():
    db_cursor.execute('SELECT blockHeight, baseFeePerGas FROM Blocks ORDER BY blockHeight;')
    data = [{'blockHeight': row[0], 'baseFeePerGas': row[1]} for row in db_cursor.fetchall()]
    return jsonify(data)

# Gas Efficiency Tracker
@app.route('/gas_efficiency', methods=['GET'])
def gas_efficiency_tracker():
    db_cursor.execute('SELECT t.blockHeight, t.transactionHash, t.gasUsed, t.value, (t.gasUsed * 1.0 / t.value) AS gasEfficiency FROM Transactions t JOIN Blocks b ON t.blockHash = b.blockHash ORDER BY t.blockHeight;')
    data = [{'blockHeight': row[0], 'transactionHash': row[1], 'gasUsed': row[2], 'value': row[3], 'gasEfficiency': row[4]} for row in db_cursor.fetchall()]
    return jsonify(data)

# Block Time Analysis
@app.route('/block_time', methods=['GET'])
def block_time_analysis():
    db_cursor.execute('SELECT b1.blockHeight, b1.timeStamp AS currentTime, b2.timeStamp AS previousTime, (b1.timeStamp - b2.timeStamp) AS blockTime FROM Blocks b1 LEFT JOIN Blocks b2 ON b1.blockHeight = b2.blockHeight + 1 ORDER BY b1.blockHeight;')
    data = [{'blockHeight': row[0], 'currentTime': row[1], 'previousTime': row[2], 'blockTime': row[3]} for row in db_cursor.fetchall()]
    return jsonify(data)

# Withdrawal Patterns Tracker
@app.route('/withdrawal_patterns', methods=['GET'])
def withdrawal_patterns_tracker():
    db_cursor.execute('SELECT address, COUNT(*) AS withdrawalCount, SUM(amount) AS totalWithdrawn FROM Withdrawals GROUP BY address ORDER BY totalWithdrawn DESC;')
    data = [{'address': row[0], 'withdrawalCount': row[1], 'totalWithdrawn': row[2]} for row in db_cursor.fetchall()]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
