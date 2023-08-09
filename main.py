import asyncio
from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

rpcUrl = "https://eth-mainnet.g.alchemy.com/v2/" + API_KEY
outputFilePath = "blocks.json"


# Connect to the Ethereum node
provider = Web3(Web3.HTTPProvider(rpcUrl))


def classify_transaction(input_data, to_address, value):
    transaction_types = []

    try:
        to_address = Web3.to_checksum_address(to_address)
        contract = None

        if input_data == "0x" and value == 0:
            transaction_types.append("Native Token Transfer")
        else:
            # Try to decode input data to identify the function being called
            method_signature = input_data[:10].hex()

            # Create contract instances using contract ABIs
            erc20 = provider.eth.contract(address=to_address, abi=erc20_abi)
            erc721 = provider.eth.contract(address=to_address, abi=erc721_abi)
            erc1155 = provider.eth.contract(address=to_address, abi=erc1155_abi)

            if method_signature == erc20.functions.transfer.signature:
                transaction_types.append("ERC20 Transfer")
            elif method_signature == erc20.functions.mint.signature:
                transaction_types.append("ERC20 Mint")
            elif method_signature == erc721.functions.transferFrom.signature:
                transaction_types.append("ERC721 Transfer")
            elif method_signature == erc721.functions.mint.signature:
                transaction_types.append("ERC721 Mint")
            elif method_signature == erc1155.functions.safeTransferFrom.signature:
                transaction_types.append("ERC1155 Transfer")
            elif method_signature == erc1155.functions.safeMint.signature:
                transaction_types.append("ERC1155 Mint")
            else:
                transaction_types.append("Unknown")

    except Exception as e:
        print("Error classifying transaction:", e)

    return transaction_types


async def listen_to_blocks():
    # try:
    block = provider.eth.get_block(provider.eth.block_number)

    log = provider.eth.get_transaction_receipt(block['transactions'][2])
    processed_log = {
        'transactionHash': log['transactionHash'].hex(),
        "address": log['address'] if 'address' in log else None,
        'blockHash': log['blockHash'].hex(),
        'blockNumber': log['blockNumber'],
        "data": log['data'] if 'data' in log else None,
        "logIndex": log['logIndex'] if 'logIndex' in log else None,
        "removed": log['removed'] if 'removed' in log else None,
        'topics': [topic.hex() for topic in log['topics']] if 'topics' in log else None,
        'transactionIndex': log['transactionIndex']
    }
    print("===============================================================================")
    print(processed_log)

    print("=============================finished==================================================")
    
    alltx = block["transactions"]
    txDetails = []
    for txn_hash in alltx:
        txn_data = provider.eth.get_transaction(txn_hash)
        log_data = provider.eth.get_transaction_receipt(txn_hash)
        transaction_data = {
            "transactionHash": txn_hash.hex(),
            "blockHash": txn_data["blockHash"].hex(),
            "blockNumber": txn_data["blockNumber"],
            "chainId": txn_data['chainId'],
            "from": txn_data["from"],
            "gas": txn_data['gas'],
            "gasPrice": txn_data['gasPrice'],
            "hash": txn_data['hash'].hex(),
            "input": txn_data['input'].hex(),
            "maxFeePerGas": txn_data['maxFeePerGas'] if 'maxFeePerGas' in txn_data else None,
            "maxPriorityFeePerGas": txn_data['maxPriorityFeePerGas'] if 'maxPriorityFeePerGas' in txn_data else None,
            "nonce": txn_data['nonce'],
            "r": txn_data['r'].hex(),
            "s": txn_data['s'].hex(),
            "to": txn_data['to'],
            "transactionIndex": txn_data['transactionIndex'],
            "type": txn_data['type'],
            "v": txn_data['v'],
            "value": txn_data['value'], 
            "types": classify_transaction(txn_data['input'].hex(), txn_data['to'], txn_data['value'])
        }
        txDetails.append(transaction_data)
    
    


    withdrawals_list = []
    for withdrawal in block["withdrawals"]:
        withdrawal_data = {
            "address": withdrawal["address"],
            "amount": int(withdrawal["amount"]),
            "index": int(withdrawal["index"]),
            "validatorIndex": int(withdrawal["validatorIndex"]),
        }
        withdrawals_list.append(withdrawal_data)

    block_data = {
        "blockHash": block["hash"].hex(),
        "parentHash": block["parentHash"].hex(),
        "blockHeight": block["number"],
        "timeStamp": block["timestamp"],
        "baseFeePerGas": block['baseFeePerGas'],
        "difficulty": block['difficulty'],
        "logsBloom": block['logsBloom'].hex(),
        "miner": block["miner"],
        "mixHash": block['mixHash'].hex(),
        "nonce": block['nonce'].hex(),
        "receiptsRoot": block['receiptsRoot'].hex(),
        "sha3Uncles": block['sha3Uncles'].hex(),
        "size": block['size'],
        "stateRoot": block['stateRoot'].hex(),
        "totalDifficulty": block['totalDifficulty'],
        "transactionsRoot": block['transactionsRoot'].hex(),
        "uncles": block['uncles'],
        "withdrawals": withdrawals_list,
        "withdrawalsRoot": block['withdrawalsRoot'].hex(),
        "gasLimit": int(block["gasLimit"]),
        "gasUsed": int(block["gasUsed"]),
        "extraData": block["extraData"].hex(),
        "txDetails": txDetails,
    }

    print("---------------------------------------------------------------------------")
    print(block_data)

    existingData = []
    if os.path.exists(outputFilePath) and os.path.getsize(outputFilePath) > 0:
        with open(outputFilePath, "r") as file:
            existingData = json.load(file)

    existingData.append(block_data)

    with open(outputFilePath, "w") as file:
        json.dump(existingData, file, indent=2)

    # except Exception as e:
    #     print("Error:", e)

async def main():
    await listen_to_blocks()

if __name__ == "__main__":
    asyncio.run(main())