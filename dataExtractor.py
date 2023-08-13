import asyncio
import sqlite3
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

rpcUrl = "https://opt-mainnet.g.alchemy.com/v2/" + API_KEY


# Connect to the Ethereum node
provider = Web3(Web3.HTTPProvider(rpcUrl))

def classify_transaction(input_data, to_address, value):
    # Check if the 'to' field is None or an Ethereum address (transfer)
    if to_address is None or to_address == "0x":
        if value > 0:  # Non-zero value indicates Ether transfer
            return "Ether Transfer"
        else:
            return "Unknown"  # No value indicates unknown transaction type

    # Convert input_data to bytes
    input_bytes = bytes.fromhex(input_data[2:])  # Remove the '0x' prefix

    # Check if the input data is non-empty (contract interaction)
    if input_bytes:
        # Token Transfers (ERC-20, ERC-721, ERC-1155)
        if input_bytes[:4] == b'\xa9\x05\x9c\xbb' or input_bytes[:4] == b'\x23\xb8\x72\xdd':
            return "Token Transfer"
        
        # Contract Deployment
        if to_address == "0x":
            return "Contract Deployment"
        
        # Token Approvals (ERC-20)
        if input_bytes[:10] == b'\x09\x5e\xa7\xb3':
            return "Token Approval"
        
        # Token Minting/Burning (Example prefixes, adjust as needed)
        if input_bytes[:4] == b'\x12\x34\x56\x78':
            return "Token Minting"
        if input_bytes[:4] == b'\x87\x65\x43\x21':
            return "Token Burning"
        
        # Contract Self-Destruction
        if input_bytes[:4] == b'\x30\xab\x71\x00':
            return "Contract Self-Destruction"

        # Other Contract Interactions
        return "Contract Interaction"
    
    return "Unknown"  # Default for unknown cases


# Create the SQLite database and tables
conn = sqlite3.connect('op_data.db')
cursor = conn.cursor()

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

conn.commit()

async def fetch_and_store_blocks(start_block, end_block):

    for block_number in range(start_block, end_block + 1):
        print("On block ------------", block_number - start_block)
        block = provider.eth.get_block(block_number)
        txDetails = []

        for txn_hash in block['transactions']:
            tx_data = provider.eth.get_transaction(txn_hash)
            classified_type = classify_transaction(tx_data.get('input', None).hex() if 'input' in tx_data else None, tx_data.get('to',None), tx_data.get('value',None))
            tx_details_with_type = {
                **tx_data,  # Copy all existing fields from tx_data
                'classifiedType': classified_type  # Add the classifiedType field
            }
            txDetails.append(tx_details_with_type)



        cursor.execute('''
        INSERT INTO Blocks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (
            block.get('hash', None).hex() if 'hash' in block else None,
            block.get('parentHash', None).hex() if 'parentHash' in block else None,
            block.get('number', None),
            block.get('timestamp', None),
            block.get('baseFeePerGas', None),
            block.get('difficulty', None),
            block.get('logsBloom', None).hex() if 'logsBloom' in block else None,
            block.get('miner', None),
            block.get('mixHash', None).hex() if 'mixHash' in block else None,
            block.get('receiptsRoot', None).hex() if 'receiptsRoot' in block else None,
            block.get('sha3Uncles', None).hex() if 'sha3Uncles' in block else None,
            block.get('size', None),
            block.get('stateRoot', None).hex() if 'stateRoot' in block else None,
            block.get('totalDifficulty', None),
            block.get('transactionsRoot', None).hex() if 'transactionsRoot' in block else None,
            block.get('gasLimit', None),
            block.get('gasUsed', None),
            block.get('extraData', None).hex() if 'extraData' in block else None
        ))

        for tx_data in txDetails:
            cursor.execute('''
            INSERT INTO Transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', (
                tx_data.get('hash', None).hex() if 'hash' in tx_data else None,
                tx_data.get('blockHash', None).hex() if 'blockHash' in tx_data else None,
                tx_data.get('from', None),
                tx_data.get('gas', None),
                tx_data.get('gasPrice', None),
                tx_data.get('input', None).hex() if 'input' in tx_data else None,
                tx_data.get('nonce', None),
                tx_data.get('r', None).hex() if 'r' in tx_data else None,
                tx_data.get('s', None).hex() if 's' in tx_data else None,
                tx_data.get('to', None),
                tx_data.get('transactionIndex', None),
                tx_data.get('type', None),
                tx_data.get('v', None),
                tx_data.get('value', None),
                tx_data.get('classifiedType', None)
            ))
            conn.commit()
        print(f"Stored block {block_number} data.")

async def main():
    latest_block_number = provider.eth.block_number
    start_block = max(0, latest_block_number - 50000)  # Fetch last 50000 blocks
    end_block = latest_block_number
    await fetch_and_store_blocks(107974753, 107974753 + 500000)

if __name__ == "__main__":
    asyncio.run(main())
    conn.close()
