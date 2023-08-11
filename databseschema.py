import sqlite3

DB_NAME = 'opdata.db'


# Connect to the SQLite database (create if not exists)
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


# Create the Blocks table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Blocks (
    blockHash TEXT PRIMARY KEY,
    parentHash TEXT,
    blockHeight INTEGER,
    timeStamp INTEGER,
    baseFeePerGas INTEGER,
    difficulty INTEGER,
    logsBloom TEXT,
    miner TEXT,
    mixHash TEXT,
    nonce TEXT,
    receiptsRoot TEXT,
    sha3Uncles TEXT,
    size INTEGER,
    stateRoot TEXT,
    totalDifficulty INTEGER,
    transactionsRoot TEXT,
    gasLimit INTEGER,
    gasUsed INTEGER,
    extraData TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Transactions (
    transactionHash TEXT PRIMARY KEY,
    blockHash TEXT,
    fromAddress TEXT,
    gas INTEGER,
    gasPrice INTEGER,
    input TEXT,
    nonce INTEGER,
    r TEXT,
    s TEXT,
    toAddress TEXT,
    transactionIndex INTEGER,
    transactionType INTEGER,
    v INTEGER,
    value INTEGER,
    classifiedType TEXT,  -- New field for classified transaction type
    FOREIGN KEY (blockHash) REFERENCES Blocks(blockHash)
);
''')
               
# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")

